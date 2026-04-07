# Reflection — Design Patterns Project

## Implemented Patterns

### 1. Singleton — Balance
Only one Balance instance exists across the entire application.
The `hasattr` check in `__init__` ensures initialization runs only once,
even though `__init__` is called on every `Balance.get_instance()` call.
Trade-off: Global state makes testing harder -- `reset()` is required in every test setUp.

### 2. Adapter — TransactionAdapter
ExternalFreelanceIncome uses different attribute names and no TransactionCategory.
The adapter translates the external format into a standard Transaction object.
The rest of the application never knows ExternalFreelanceIncome exists.
Trade-off: One adapter class per external format -- scales poorly with many sources.

### 3. Observer — LowBalanceAlertObserver, PrintObserver
Balance notifies all registered observers after every transaction.
LowBalanceAlertObserver triggers when balance drops below threshold and resets when it recovers.
Trade-off: Observers are notified even when balance did not cross the threshold.

### 4. Command — ApplyTransactionCommand (Student Choice)
Each transaction is wrapped in a command object with execute() and undo().
TransactionHistory caches the last command for single-step undo.
Chosen because financial applications fundamentally need undo capability.
Trade-off: Only one undo step -- a full stack would be needed for multi-step undo.