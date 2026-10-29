init -5 python:
    def bank_transaction_tests():
        state = create_new_game_state()
        start = state.wallet.balance
        income = post_transaction(500, "income", "Тестовый доход", "work", source_event_id="bank:test:income", state=state)
        assert income.success and state.wallet.balance == start + 500
        duplicate = post_transaction(500, "income", "Дубликат", "work", source_event_id="bank:test:income", state=state)
        assert not duplicate.success and state.wallet.balance == start + 500
        expense = post_transaction(-300, "purchase", "Тестовая покупка", "shopping", state=state)
        assert expense.success and state.wallet.balance == start + 200
        state.wallet.balance = 0
        blocked = post_transaction(-1, "expense", "Недоступный расход", "expense", state=state)
        assert not blocked.success and len(state.wallet.history) == 2
        assert money_history(state)[0] is expense.transaction
        return True

    def bank_summary_tests():
        state = create_new_game_state()
        post_transaction(1200, "income", "Тестовая смена", "work", state=state)
        post_transaction(-400, "purchase", "Продукты", "food", state=state)
        assert take_loan("nika", 3000, state).success
        loan = active_loan("nika", state)
        assert repay_loan(loan.id, 1000, state).success
        income, expenses = money_period_totals(state)
        assert income == 1200 and expenses == 400
        assert state.wallet.balance == 12800
        return True

    def bank_loan_tests():
        state = create_new_game_state()
        start = state.wallet.balance
        result = take_loan("bank", 10000, state)
        assert result.success and state.wallet.balance == start + 10000
        loan = active_loan("bank", state)
        assert loan and loan.total_due == 10000 and loan.due_date == state.clock.date + datetime.timedelta(days=56)
        assert not take_loan("bank", 5000, state).success
        state.clock.advance(7 * 1440)
        process_bank_time(state)
        process_bank_time(state)
        assert loan.accrued_interest == 200 and loan.periods_accrued == 1
        assert loan_recommended_payment(loan) == 1450
        payment = repay_loan(loan.id, 1450, state)
        assert payment.success and loan.principal_remaining == 8750 and loan.accrued_interest == 0
        state.clock.advance(7 * 1440)
        process_bank_time(state)
        assert loan.accrued_interest == 175
        assert repay_loan(loan.id, state=state).success and loan.status == "paid"
        nika = take_loan("nika", 3000, state)
        assert nika.success and active_loan("nika", state).rate_bps == 0
        return True

    def bank_transfer_and_migration_tests():
        state = create_new_game_state()
        assert not transfer_money("nika", 100, "Тест", state=state).success
        assert register_transfer_recipient("nika", state)
        assert transfer_money("nika", 100, "Тестовый перевод", "bank:test:transfer", state).success
        assert not transfer_money("nika", 100, "Повтор", "bank:test:transfer", state).success
        legacy = create_new_game_state()
        legacy.schema_version = 9
        legacy.wallet.history = [("2026-08-29", "09:00", 250, "Старая операция")]
        del legacy.wallet.transaction_sequence
        del legacy.wallet.loans
        del legacy.wallet.transfer_recipients
        balance = legacy.wallet.balance
        ensure_current_schema(legacy)
        assert legacy.schema_version == SCHEMA_VERSION and legacy.wallet.balance == balance
        assert len(legacy.wallet.history) == 1 and legacy.wallet.history[0].amount == 250
        ensure_current_schema(legacy)
        assert len(legacy.wallet.history) == 1
        return True

    def bank_visual_prepare(tab):
        store.game_state = create_new_game_state()
        post_transaction(1200, "income", "Тестовая смена", "work", state=game_state)
        post_transaction(-400, "purchase", "Продукты", "food", state=game_state)
        if tab == "history_long":
            post_transaction(123456789, "income", "Очень длинное описание финансовой операции для проверки переноса текста и суммы", "work", state=game_state)
        if tab in ("loans", "loans_full", "loans_notice"):
            take_loan("bank", 5000, game_state)
        if tab == "loans_full":
            take_loan("nika", 10000, game_state)

    def bank_visual_select(tab):
        phone_open("bank")
        bank_open_tab("loans" if tab in ("loans_full", "loans_notice", "loans_offer") else "history" if tab == "history_long" else tab)
        if tab == "loans_notice":
            store.ui_bank_notice = "Деньги зачислены"
        if tab == "loans_offer":
            bank_select_offer("bank", 20000)

testsuite bank:
    testcase transactions:
        assert eval bank_transaction_tests()

    testcase summary:
        assert eval bank_summary_tests()
    testcase loans:
        assert eval bank_loan_tests()
    testcase transfers_and_migration:
        assert eval bank_transfer_and_migration_tests()
    testcase visual:
        parameter tab = ["overview", "history", "history_long", "loans", "loans_full", "loans_notice", "loans_offer", "transfers"]
        $ bank_visual_prepare(tab)
        run Show("phone_screen")
        pause 0.15
        run Function(bank_visual_select, tab)
        pause 0.2
        assert screen "phone_screen"
        screenshot ("bank_" + tab + ".png") crop (714, 60, 492, 960)
        run Hide("phone_screen")
    testcase navigation:
        $ store.game_state = create_new_game_state()
        run Show("phone_screen")
        pause 0.2
        run Function(phone_open)
        pause 0.1
        click id "phone_app_bank"
        assert eval (ui_phone_app == "bank")
        click "Кредиты"
        assert eval (ui_bank_tab == "loans")
        run Hide("phone_screen")
    testcase save_load:
        run Start("bank_save_fixture")
        pause 0.2
        $ renpy.session["bank_slot"] = "bank-" + str(__import__("uuid").uuid4())
        $ renpy.save(renpy.session["bank_slot"], include_screenshot=False)
        assert eval (len(renpy.get_save_data(renpy.session["bank_slot"])["game_state"].wallet.loans) == 1)
        $ game_state.wallet.history = []
        $ game_state.wallet.loans = []
        run Function(renpy.load, renpy.session["bank_slot"])
        pause 0.3
        assert eval (renpy.store.game_state.wallet.loans[0].principal_remaining == 5000)
        assert eval (renpy.store.game_state.wallet.history[-1].kind == "loan")
        $ renpy.unlink_save(renpy.session["bank_slot"])

label bank_save_fixture:
    $ game_state = create_new_game_state()
    $ take_loan("bank", 5000, game_state)
    $ renpy.block_rollback()
    jump bank_save_fixture_wait

label bank_save_fixture_wait:
    $ renpy.pause(hard=True)
    jump bank_save_fixture_wait
