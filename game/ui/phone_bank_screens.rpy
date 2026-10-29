default ui_bank_tab = "overview"
default ui_bank_offer = None
default ui_bank_notice = None

init -15 python:
    def bank_open_tab(tab):
        store.ui_bank_tab = tab
        store.ui_bank_offer = None
        store.ui_bank_notice = None

    def bank_select_offer(lender_id, amount):
        store.ui_bank_offer = (lender_id, int(amount))
        store.ui_bank_notice = None

    def bank_confirm_offer():
        if not store.ui_bank_offer:
            return
        lender_id, amount = store.ui_bank_offer
        result = take_loan(lender_id, amount)
        store.ui_bank_notice = "Деньги зачислены" if result.success else result.reason
        store.ui_bank_offer = None
        renpy.restart_interaction()

    def bank_repay_ui(loan_id, amount=None):
        result = repay_loan(loan_id, amount)
        store.ui_bank_notice = "Платеж выполнен" if result.success else result.reason
        renpy.restart_interaction()

    def bank_amount_text(amount):
        return ("+" if amount > 0 else "") + ("{:,}".format(int(amount)).replace(",", " ")) + " ₽"

    def bank_plain_amount(amount):
        return "{:,} ₽".format(int(amount)).replace(",", " ")

screen phone_bank():
    vbox:
        spacing 12
        xfill True
        hbox:
            spacing 3
            textbutton "Счет" action Function(bank_open_tab, "overview") style "phone_tab" selected (ui_bank_tab == "overview")
            textbutton "История" action Function(bank_open_tab, "history") style "phone_tab" selected (ui_bank_tab == "history")
            textbutton "Кредиты" action Function(bank_open_tab, "loans") style "phone_tab" selected (ui_bank_tab == "loans")
        if ui_bank_notice:
            frame:
                background Frame("ui/phone/accent.svg", 20, 20)
                padding (12, 9)
                xfill True
                text ui_bank_notice style "phone_small" xalign 0.5
        if ui_bank_tab == "overview":
            use phone_bank_overview
        elif ui_bank_tab == "history":
            use phone_bank_history
        elif ui_bank_tab == "loans":
            use phone_bank_loans
        else:
            use phone_bank_transfers

screen phone_bank_overview():
    $ income, expenses = money_period_totals()
    vbox:
        spacing 14
        xfill True
        frame:
            background Frame("ui/phone/accent.svg", 20, 20)
            padding (20, 18)
            xfill True
            vbox:
                spacing 6
                text "Доступно" style "phone_small"
                text bank_plain_amount(game_state.wallet.balance) style "phone_heading" size 38 color NS_COLOR["amber"]
        hbox:
            spacing 10
            frame:
                background Frame("ui/phone/glass.svg", 20, 20)
                padding (14, 12)
                xsize 205
                vbox:
                    text "Доходы" style "phone_small"
                    text bank_amount_text(income) style "phone_text" color NS_COLOR["green"]
            frame:
                background Frame("ui/phone/glass.svg", 20, 20)
                padding (14, 12)
                xsize 205
                vbox:
                    text "Расходы" style "phone_small"
                    text bank_amount_text(-expenses) style "phone_text" color NS_COLOR["coral"]
        textbutton "Переводы" action Function(bank_open_tab, "transfers") style "phone_row"
        text "Получатели открываются сюжетными событиями. Сейчас доступных переводов нет." style "phone_small" xsize 410

screen phone_bank_transaction_row(transaction):
    frame:
        background Frame("ui/phone/glass.svg", 20, 20)
        padding (14, 10)
        xfill True
        hbox:
            spacing 8
            vbox:
                xsize 282
                text transaction.reason style "phone_text" size 17 substitute False
                text "[transaction.date] · [transaction.display_time]" style "phone_small" size 13
            text bank_amount_text(transaction.amount) style "phone_text" color (NS_COLOR["green"] if transaction.amount > 0 else NS_COLOR["coral"]) xalign 1.0

screen phone_bank_history():
    viewport:
        ysize 650
        mousewheel True
        draggable True
        vbox:
            spacing 8
            xsize 410
            if money_history():
                for transaction in money_history():
                    use phone_bank_transaction_row(transaction)
            else:
                text "Операций пока нет" style "phone_small" xalign 0.5

screen phone_bank_transfers():
    vbox:
        spacing 16
        xfill True
        text "Переводы" style "phone_heading"
        if game_state.wallet.transfer_recipients:
            for recipient_id in sorted(game_state.wallet.transfer_recipients):
                frame:
                    background Frame("ui/phone/glass.svg", 20, 20)
                    padding (14, 12)
                    xfill True
                    text NPCS[recipient_id]["name"] style "phone_text" substitute False
            text "Сумма и назначение перевода задаются доступным сюжетным действием." style "phone_small" xsize 410
        else:
            text "Нет доступных получателей" style "phone_heading" xalign 0.5
            text "Получатели появляются после соответствующих сюжетных событий. Свободный ввод реквизитов не используется." style "phone_small" xsize 410 text_align 0.5
        textbutton "Вернуться к счету" action Function(bank_open_tab, "overview") style "phone_row"

screen phone_bank_loans():
    $ nika_loan = active_loan("nika")
    $ bank_loan = active_loan("bank")
    viewport:
        xsize 420
        ysize 650
        mousewheel True
        draggable True
        vbox:
            spacing 14
            xsize 420
            $ active_loans = [loan for loan in game_state.wallet.loans if loan.status == "active"]
            if active_loans:
                text "Активные долги" style "phone_heading"
                for loan in active_loans:
                    frame:
                        background Frame("ui/phone/glass.svg", 20, 20)
                        padding (14, 12)
                        xfill True
                        vbox:
                            spacing 7
                            text ("Ника" if loan.lender_id == "nika" else "Банковский кредит") style "phone_heading"
                            text "Остаток: [bank_plain_amount(loan.total_due)]" style "phone_text"
                            text "Срок: [loan.due_date.strftime('%d.%m.%Y')]" style "phone_small"
                            if loan.lender_id == "bank":
                                text "Начислено процентов: [bank_plain_amount(loan.accrued_interest)]" style "phone_small"
                            textbutton "Рекомендуемый платеж · [bank_plain_amount(loan_recommended_payment(loan))]" action Function(bank_repay_ui, loan.id, loan_recommended_payment(loan)) style "phone_row" xsize 370
                            textbutton "Погасить полностью" action Function(bank_repay_ui, loan.id) style "phone_row" xsize 370
            if not nika_loan or not bank_loan:
                text "Новый займ" style "phone_heading"
                if not nika_loan:
                    text "Ника · без процентов · 30 дней" style "phone_small"
                    hbox:
                        spacing 6
                        for amount in NIKA_LOAN_AMOUNTS:
                            textbutton bank_plain_amount(amount) action Function(bank_select_offer, "nika", amount) style "phone_tab" xsize 136
                if not bank_loan:
                    text "Банк · 2% каждые 7 дней · 56 дней" style "phone_small"
                    hbox:
                        spacing 6
                        for amount in BANK_LOAN_AMOUNTS:
                            textbutton bank_plain_amount(amount) action Function(bank_select_offer, "bank", amount) style "phone_tab" xsize 136
                if ui_bank_offer:
                    $ lender_id, offer_amount = ui_bank_offer
                    frame:
                        background Frame("ui/phone/accent.svg", 20, 20)
                        padding (14, 12)
                        xfill True
                        vbox:
                            spacing 8
                            text "Подтвердить [bank_plain_amount(offer_amount)]?" style "phone_heading"
                            text ("Без процентов, вернуть в течение 30 дней." if lender_id == "nika" else "2% на остаток каждые 7 дней, срок 56 дней.") style "phone_small"
                            hbox:
                                spacing 8
                                textbutton "Подтвердить" action Function(bank_confirm_offer) style "phone_row" xsize 181
                                textbutton "Отмена" action SetVariable("ui_bank_offer", None) style "phone_row" xsize 181
