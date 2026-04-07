# balance_observer.py

class IBalanceObserver:
    def update(self, balance, transaction):
        """Handle balance updates."""
        raise NotImplementedError("Subclasses must implement update method.")


class PrintObserver(IBalanceObserver):
    def update(self, balance, transaction):
        """Print balance update message."""
        print(f"Balance updated: ${balance} after applying {transaction}")


class LowBalanceAlertObserver(IBalanceObserver):
    def __init__(self, threshold):
        self.threshold = threshold
        # track wether alert is currently active
        self.alert_triggered = False

    def update(self, balance, transaction):
        """Alert if balance drops below threshold."""
        if balance < self.threshold:
            self.alert_triggered = True
            print(f"Alert: Balance ${balance} dropped below threshold ${self.threshold}")
        else:
            # reset alert if balance goes back above threshold
            self.alert_triggered = False
