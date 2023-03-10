from secrets import choice
from django.db import models
from authentication.models import User
# Create your models here.


class Expense(models.Model):
    CATEGORY_OPTIONS = [
        ('ONLINE_SERVICES', 'ONLINE_SERVICES'),
        ('TRAVEL', 'TRAVEL'),
        ('RENTE', 'RENTE'),
        ('OTHERS', 'OTHERS')
    ]
    category = models.CharField(choices=CATEGORY_OPTIONS, max_length=50)
    amount_of_money = models.DecimalField(max_digits=10, decimal_places=2)
    describtion = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self) -> str:
        return f'{self.owner} expense'
