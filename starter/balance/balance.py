from transaction.transaction_category import TransactionCategory

class Balance:
    """Singleton to track the balance."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def get_instance(cls):
        """Return the single instance of Balance."""
        return cls()

    def __init__(self):
        # hasattr check ensures init runs only once
        # __init__ is called on every cls() -- even if __new__ returns existing instance
        if not hasattr(self, '_balance'):
            self._balance = 0.0
            self._observers = []

    def reset(self):
        """Reset the net balance to zero."""
        self._balance = 0.0

    def add_income(self, amount):
        """Add income to the balance."""
        self._balance += amount

    def add_expense(self, amount):
        """Subtract expense from the balance."""
        self._balance -= amount

    def apply_transaction(self, transaction):
        """Apply a Transaction object to update the balance."""
        if transaction.category == TransactionCategory.INCOME:
            self.add_income(transaction.amount)
        elif transaction.category == TransactionCategory.EXPENSE:
            self.add_expense(transaction.amount)
        else:
            raise ValueError(f"Unknown category: {transaction.category}")
        self._notify_observers(transaction)

    def get_balance(self):
        """Get the current net balance."""
        return self._balance

    def summary(self):
        """Return a summary string of the net balance."""
        return f"Current balance: ${self._balance}"

    def register_observer(self, observer):
        """Register an observer."""
        self._observers.append(observer)

    def _notify_observers(self, transaction):
        """Notify all registered observers."""
        for observer in self._observers:
            observer.update(self._balance, transaction)