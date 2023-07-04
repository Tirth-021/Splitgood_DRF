from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Group, Expense, ExpenseParticipant


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class ExpenseParticipantSerializer(serializers.ModelSerializer):
    # user = UserSerializer()
    class Meta:
        model = ExpenseParticipant
        fields = ['user', 'amount_owed', 'percentage']


class ExpenseSerializer(serializers.ModelSerializer):
    participants = ExpenseParticipantSerializer(many=True)

    class Meta:
        model = Expense
        fields = ['id', 'name', 'amount', 'payer', 'group', 'split_type', 'participants']

    def create(self, validated_data):
        participants_data = validated_data.pop('participants')
        expense = Expense.objects.create(**validated_data)
        for participant_data in participants_data:
            user_data = participant_data.get('user')
            user_percent = participant_data.get('percentage')
            if expense.split_type == 'EQUAL':
                amount_owed = expense.amount / len(participants_data)
            elif expense.split_type == 'PERCENTAGE':
                amount_owed = (expense.amount * user_percent) / 100
            elif expense.split_type == 'UNEQUAL':
                amount_owed = participant_data.get('amount_owed')
            participant = ExpenseParticipant.objects.create(expense=expense, user=user_data, amount_owed=amount_owed,
                                                            percentage=user_percent)
        return expense
