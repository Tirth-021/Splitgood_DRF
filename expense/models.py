import uuid as uuid
from django.contrib.auth.models import User
from django.db import models


class Group(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='custom_grp_created_by')
    group_name = models.CharField(max_length=30)
    group_description = models.TextField()
    users = models.ManyToManyField(User, related_name='group')
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(unique=True, null=True, default=uuid.uuid4)
    is_simplified = models.BooleanField(default=False)


class LiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class Expense(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_paid')
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='expenses')
    split_type = models.CharField(max_length=20, choices=[
        ('EQUAL', 'Equally'),
        ('PERCENTAGE', 'By Percentage'),
        ('UNEQUAL', 'Unequally'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)


class ExpenseParticipant(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name='participants')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_owed')
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2,null=True,blank=True)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='group')
    is_paid = models.BooleanField(default=False)
    owed_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses_owed_to')
