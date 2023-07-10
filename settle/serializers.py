from rest_framework import serializers
from expense.models import ExpenseParticipant


class ViewExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseParticipant
        fields = '__all__'

