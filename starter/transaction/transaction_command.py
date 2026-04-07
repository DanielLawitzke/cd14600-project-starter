from abc import ABC, abstractmethod

from transaction.transaction_category import TransactionCategory


class TransactionCommand(ABC):
    """Abstract command interface -- every command must support execute and undo."""

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass


class ApplyTransactionCommand(TransactionCommand):
    """Encapsulates a transaction as a command -- supports undo."""

    def __init__(self, balance, transaction):
        self.balance = balance        # receiver
        self.transaction = transaction  # data

    def execute(self):
        # apply transaction to balance
        self.balance.apply_transaction(self.transaction)

    def undo(self):
        if self.transaction.category == TransactionCategory.INCOME:
            # income was added -- subtract it back
            self.balance.add_expense(self.transaction.amount)
        elif self.transaction.category == TransactionCategory.EXPENSE:
            # expense was subtracted -- add it back
            self.balance.add_income(self.transaction.amount)
        else:
            # unknown category -- should never happen
            raise ValueError(f"Unknown category: {self.transaction.category}")


class TransactionHistory:
    """Invoker -- stores executed commands, enables undo."""

    def __init__(self):
        self._last = None  # cache last command only

    def execute(self, command: TransactionCommand):
        command.execute()
        self._last = command  # store for undo

    def undo_last(self):
        if self._last:
            self._last.undo()
            self._last = None