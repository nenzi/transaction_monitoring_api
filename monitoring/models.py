from django.db import models

# Create your models here

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    tier = models.CharField(
        max_length=10,
        choices=[
            ('bronze', 'Bronze'),
            ('silver', 'Silver'),
            ('gold', 'Gold'),
        ],
        default='bronze'
    )
    flagged = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Transaction(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return f"Transaction {self.id} - {self.amount}"
