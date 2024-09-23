from django.db import models

class Users(models.Model):
    """
    A model representing a user with a username and balance.
    """

    username = models.CharField(max_length=50, unique=True)
    balance = models.FloatField()

    def __str__(self):
        """
        Return the username as the string representation of the user.
        """
        return self.username


class Stocks(models.Model):
    """
    A model representing a stock with ticker, price, and name.
    """

    ticker = models.CharField(max_length=70, unique=True)
    stock_price = models.FloatField()
    stock_name = models.CharField(max_length=40)

    def __str__(self):
        """
        Return the ticker symbol as the string representation of the stock.
        """
        return self.ticker


class Transaction(models.Model):
    """
    A model representing a stock transaction.
    """

    TRANSACTION_TYPE_CHOICES = [
        ('BUY', 'Buy'),
        ('SELL', 'Sell')
    ]

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    ticker = models.ForeignKey(Stocks, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPE_CHOICES, default='BUY')
    transaction_volume = models.FloatField()
    transaction_price = models.FloatField()
    created_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a string representation showing the user, stock ticker, and transaction type.
        """
        return f"{self.user.username} - {self.ticker.ticker} - {self.transaction_type}"
