from rest_framework import serializers
from rest_framework.decorators import action
from plugins.erp_base.business_api import BusinessViewSet, parameters
from plugins.erp_base.models import Employee
from . import models, services


class PurchaseViewSet(BusinessViewSet):
    @action(methods=['post'], detail=True)
    def confirm(self, request, pk=None):
        fields = {'employee': serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())} if self.queryset.model is models.PurchaseRequest else {}
        return self.performed(services.confirm, parameters(self, fields))
