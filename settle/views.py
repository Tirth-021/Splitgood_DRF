from django.db.models import Sum, F
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from expense.models import ExpenseParticipant
from settle.serializers import ViewExpenseSerializer



class SettleViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ExpenseParticipant.objects.all()
    serializer_class = ViewExpenseSerializer

    def list(self, request):
        group = self.request.query_params.get('group_id')
        queryset = ExpenseParticipant.objects.filter(group_id=group, is_paid=False, user=request.user.id).exclude(
            owed_to=F("user")).annotate(
            total=Sum('amount_owed')).values('owed_to__username', 'total')
        return Response(queryset)

    @action(detail=False, methods=['post'])
    def settle_expense(self, request):
        group = request.query_params.get('group_id')

        ExpenseParticipant.objects.filter(group_id=group, is_paid=False, user=request.user.id).exclude(
            owed_to=F("user")).update(is_paid=True)

        return Response({'message': 'Expenses settled successfully.'})
