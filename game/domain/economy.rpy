init -110 python:
    import math

    NIKA_LOAN_AMOUNTS = (3000, 5000, 10000)
    BANK_LOAN_AMOUNTS = (5000, 10000, 20000)
    NIKA_LOAN_TERM_DAYS = 30
    BANK_LOAN_TERM_DAYS = 56
    BANK_LOAN_PERIOD_DAYS = 7
    BANK_LOAN_PERIODS = 8
    BANK_LOAN_WEEKLY_RATE_BPS = 200

    class MoneyTransaction(object):
        def __init__(self, transaction_id, sequence, date, display_time, amount, kind,
                     category_id, reason, counterparty_id=None, reference_id=None,
                     source_event_id=None, metadata=None):
            self.id = transaction_id
            self.sequence = int(sequence)
            self.date = date
            self.display_time = display_time
            self.amount = int(amount)
            self.kind = kind
            self.category_id = category_id
            self.reason = reason
            self.counterparty_id = counterparty_id
            self.reference_id = reference_id
            self.source_event_id = source_event_id
            self.metadata = dict(metadata or {})

    class MoneyOperationResult(object):
        def __init__(self, success, balance, reason=None, transaction=None):
            self.success = bool(success)
            self.balance = int(balance)
            self.reason = reason
            self.transaction = transaction

    class LoanState(object):
        def __init__(self, loan_id, lender_id, principal, taken_date, due_date,
                     rate_bps=0, period_days=None, installment_count=None):
            self.id = loan_id
            self.lender_id = lender_id
            self.principal_initial = int(principal)
            self.principal_remaining = int(principal)
            self.accrued_interest = 0
            self.taken_date = taken_date
            self.due_date = due_date
            self.rate_bps = int(rate_bps)
            self.period_days = period_days
            self.installment_count = installment_count
            self.periods_accrued = 0
            self.next_accrual_date = (taken_date + datetime.timedelta(days=period_days)) if period_days else None
            self.status = "active"

        @property
        def total_due(self):
            return self.principal_remaining + self.accrued_interest

    def _money_source_exists(wallet, source_event_id):
        return bool(source_event_id) and any(row.source_event_id == source_event_id for row in wallet.history)

    def post_transaction(amount, kind, reason, category_id, counterparty_id=None,
                         reference_id=None, source_event_id=None, metadata=None, state=None):
        state = _state(state)
        amount = int(amount)
        if amount == 0:
            return MoneyOperationResult(False, state.wallet.balance, "Сумма должна быть больше нуля")
        if _money_source_exists(state.wallet, source_event_id):
            return MoneyOperationResult(False, state.wallet.balance, "Операция уже выполнена")
        if amount < 0 and state.wallet.balance < -amount:
            return MoneyOperationResult(False, state.wallet.balance, "Недостаточно денег")
        state.wallet.transaction_sequence += 1
        transaction = MoneyTransaction(
            "money_%06d" % state.wallet.transaction_sequence,
            state.wallet.transaction_sequence,
            state.clock.date.isoformat(), state.clock.display_time, amount, kind,
            category_id, reason, counterparty_id, reference_id, source_event_id, metadata,
        )
        state.wallet.balance += amount
        state.wallet.history.append(transaction)
        dispatch_game_event("money_changed", state, False, amount=amount, reason=reason,
                            kind=kind, transaction_id=transaction.id)
        return MoneyOperationResult(True, state.wallet.balance, transaction=transaction)

    def active_loan(lender_id, state=None):
        for loan in _state(state).wallet.loans:
            if loan.lender_id == lender_id and loan.status == "active":
                return loan
        return None

    def take_loan(lender_id, amount, state=None):
        state = _state(state)
        amount = int(amount)
        allowed = NIKA_LOAN_AMOUNTS if lender_id == "nika" else BANK_LOAN_AMOUNTS if lender_id == "bank" else ()
        if amount not in allowed:
            return MoneyOperationResult(False, state.wallet.balance, "Недоступная сумма займа")
        if active_loan(lender_id, state):
            return MoneyOperationResult(False, state.wallet.balance, "Сначала погасите действующий долг")
        wallet = state.wallet
        loan_id = "loan_%s_%06d" % (lender_id, wallet.transaction_sequence + 1)
        if lender_id == "nika":
            loan = LoanState(loan_id, lender_id, amount, state.clock.date,
                             state.clock.date + datetime.timedelta(days=NIKA_LOAN_TERM_DAYS))
            reason = "Займ от Ники"
        else:
            loan = LoanState(loan_id, lender_id, amount, state.clock.date,
                             state.clock.date + datetime.timedelta(days=BANK_LOAN_TERM_DAYS),
                             BANK_LOAN_WEEKLY_RATE_BPS, BANK_LOAN_PERIOD_DAYS, BANK_LOAN_PERIODS)
            reason = "Банковский кредит"
        wallet.loans.append(loan)
        result = post_transaction(amount, "loan", reason, "loan", lender_id, loan_id,
                                  "loan_issue:" + loan_id, state=state)
        if not result.success:
            wallet.loans.remove(loan)
        return result

    def process_bank_time(state=None):
        state = _state(state)
        today = state.clock.date
        for loan in state.wallet.loans:
            if loan.status != "active" or loan.lender_id != "bank":
                continue
            while loan.next_accrual_date and loan.next_accrual_date <= today and loan.periods_accrued < loan.installment_count:
                interest = int(math.ceil(loan.principal_remaining * loan.rate_bps / 10000.0))
                loan.accrued_interest += interest
                loan.periods_accrued += 1
                loan.next_accrual_date += datetime.timedelta(days=loan.period_days)
                dispatch_game_event("loan_interest_accrued", state, False, loan_id=loan.id, amount=interest)

    def loan_recommended_payment(loan):
        if loan.lender_id == "nika":
            return loan.total_due
        periods_left = max(1, loan.installment_count - loan.periods_accrued + 1)
        return min(loan.total_due, int(math.ceil(loan.principal_remaining / float(periods_left))) + loan.accrued_interest)

    def repay_loan(loan_id, amount=None, state=None):
        state = _state(state)
        loan = next((row for row in state.wallet.loans if row.id == loan_id and row.status == "active"), None)
        if loan is None:
            return MoneyOperationResult(False, state.wallet.balance, "Долг не найден")
        amount = loan.total_due if amount is None else int(amount)
        if amount <= 0:
            return MoneyOperationResult(False, state.wallet.balance, "Сумма должна быть больше нуля")
        amount = min(amount, loan.total_due)
        interest_paid = min(amount, loan.accrued_interest)
        principal_paid = amount - interest_paid
        result = post_transaction(-amount, "loan_payment", "Погашение долга", "loan_payment",
                                  loan.lender_id, loan.id, state=state)
        if not result.success:
            return result
        loan.accrued_interest -= interest_paid
        loan.principal_remaining -= principal_paid
        if loan.total_due == 0:
            loan.status = "paid"
            dispatch_game_event("loan_repaid", state, True, loan_id=loan.id, lender_id=loan.lender_id)
        return result

    def register_transfer_recipient(recipient_id, state=None):
        state = _state(state)
        if recipient_id not in NPCS:
            return False
        state.wallet.transfer_recipients.add(recipient_id)
        return True

    def transfer_money(recipient_id, amount, reason, source_event_id=None, state=None):
        state = _state(state)
        if recipient_id not in state.wallet.transfer_recipients:
            return MoneyOperationResult(False, state.wallet.balance, "Получатель пока недоступен")
        return post_transaction(-int(amount), "transfer", reason, "transfer", recipient_id,
                                source_event_id=source_event_id, state=state)

    def money_history(state=None, kind=None):
        rows = list(reversed(_state(state).wallet.history))
        return [row for row in rows if kind is None or row.kind == kind]

    def money_period_totals(state=None):
        rows = _state(state).wallet.history
        # Выдача займа не является доходом, а возврат основного долга — расходом.
        # Оба движения остаются в полной истории и меняют доступный баланс.
        excluded = ("loan", "loan_payment")
        return (sum(row.amount for row in rows if row.amount > 0 and row.kind not in excluded),
                -sum(row.amount for row in rows if row.amount < 0 and row.kind not in excluded))
