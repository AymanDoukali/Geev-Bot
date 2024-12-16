from .utils import setup_logger

# Initialize logger
logger = setup_logger("notifier")

class NotifierBase:
    """Base class for all notifiers."""
    def send(self, *args):
        raise NotImplementedError("Send method must be implemented by subclasses")


class EmailNotifier(NotifierBase):
    """Notifier class for sending emails."""
    def __init__(self):
        # Your code here
        pass

    def send(self, *args): # You can decide which arguments you need to send an email
        """Sends an email notification."""
        try:
            # Your code here
            logger.info("Email sent successfully.")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")


# When everything is going well, implement PushNotifier, SMSNotifier...

class NotifierManager:
    """Manages and delegates notifications."""
    def __init__(self):
        self.notifiers = {}

    def register_notifier(self, name, notifier):
        """Registers a notifier."""
        self.notifiers[name] = notifier

    def notify(self, notifier_name, *args, **kwargs):
        """Sends a notification using the specified notifier."""
        notifier = self.notifiers.get(notifier_name, None)
        if not notifier:
            logger.error(f"Notifier '{notifier_name}' not found.")
            return
        notifier.send(*args, **kwargs)

    def notify_all(self, *args, **kwargs):
        for notifier in self.notifiers.values():
            notifier.send(*args, **kwargs)
