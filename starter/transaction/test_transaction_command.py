import unittest
from balance.balance import Balance
from transaction.transaction import Transaction
from transaction.transaction_category import TransactionCategory
from transaction.transaction_command import ApplyTransactionCommand, TransactionHistory


class TestTransactionCommand(unittest.TestCase):

    def setUp(self):
        self.balance = Balance.get_instance()
        self.balance.reset()
        self.history = TransactionHistory()

    def test_execute_income(self):
        cmd = ApplyTransactionCommand(self.balance, Transaction(100, TransactionCategory.INCOME))
        self.history.execute(cmd)
        self.assertEqual(self.balance.get_balance(), 100)

    def test_execute_expense(self):
        cmd = ApplyTransactionCommand(self.balance, Transaction(40, TransactionCategory.EXPENSE))
        self.history.execute(cmd)
        self.assertEqual(self.balance.get_balance(), -40)

    def test_undo_income(self):
        cmd = ApplyTransactionCommand(self.balance, Transaction(100, TransactionCategory.INCOME))
        self.history.execute(cmd)
        self.history.undo_last()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_undo_expense(self):
        cmd = ApplyTransactionCommand(self.balance, Transaction(40, TransactionCategory.EXPENSE))
        self.history.execute(cmd)
        self.history.undo_last()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_undo_without_command(self):
        # undo with no history -- should not crash
        self.history.undo_last()
        self.assertEqual(self.balance.get_balance(), 0)

    def test_undo_invalid_category(self):
        class FakeCategory:
            pass
        cmd = ApplyTransactionCommand(
            self.balance,
            Transaction(100, FakeCategory())
        )
        # execute fails due to unknown category
        with self.assertRaises(ValueError):
            cmd.undo()


if __name__ == "__main__":
    unittest.main()