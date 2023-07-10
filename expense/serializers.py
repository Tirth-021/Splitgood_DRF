from rest_framework import serializers
from .models import Group, Expense, ExpenseParticipant


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class ExpenseParticipantSerializer(serializers.ModelSerializer):
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
        breakpoint()
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
                                                            percentage=user_percent, group=expense.group,
                                                            owed_to=expense.payer)
        return expense
