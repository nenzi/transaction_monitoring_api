from datetime import datetime, timedelta
from django.core.mail import send_mail
from .models import Transaction, User


#Transaction amount exceeds the amount for a given tier.
def evaluate_policy_5(transaction):
    tier_amounts = {
        "bronze": 1000,
        "silver": 5000,
        "gold": 10000,
    }
    
    user_tier = transaction.user.tier
    if transaction.amount > tier_amounts.get(user_tier, 0):
        return True
    return False


#Transaction is happening between a regular user and previously flagged user.
def evaluate_policy_4(transaction):
    regular_user = User.objects.get(id=transaction.user_id)
    flagged_users = User.objects.filter(flagged=True)

    if regular_user in flagged_users:
        return True
    return False

# Transaction is attributed to a new user.
def evaluate_policy_3(transaction):
    user_transactions = Transaction.objects.filter(user=transaction.user)
    if user_transactions.count() == 1:
        return True
    return False

# Transaction from a particular user occurs within a timing window of less than 1 minute.
def evaluate_policy_2(transaction):
    prev_transaction = Transaction.objects.filter(
        user=transaction.user,
        timestamp__gt=transaction.timestamp - timedelta(minutes=1),
        timestamp__lt=transaction.timestamp,
    ).exclude(id=transaction.id).first()

    if prev_transaction:
        return True
    return False

# The transaction amount is greater than 5,000,000.
def evaluate_policy(transaction):
    if transaction.amount < 5000000:
        return True
    return False

# send email
def send_notification_email(transaction):
    subject = "Transaction Alert"
    message = f"A transaction of amount ${transaction.amount} requires attention."
    from_email = "noreply@example.com"
    recipient_list = ["admin@example.com"]

    send_mail(subject, message, from_email, recipient_list)

#process transaction
def process_transaction(transaction_id):
    try:
        transaction = Transaction.objects.get(id=transaction_id)
        policies = [
            evaluate_policy,
            evaluate_policy_2,
            evaluate_policy_3,
            evaluate_policy_4,
            evaluate_policy_5,
        ]
        
        should_notify = any(policy(transaction) for policy in policies)
        if should_notify:
            send_notification_email(transaction)
    except Transaction.DoesNotExist:
        pass
