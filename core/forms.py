from django import forms
from django.db import models
from core.models import *


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'


class CustomerOrdersForm(forms.ModelForm):
    class Meta:
        model = CustomerOrders
        fields = '__all__'


class CustomerOrderForm(forms.ModelForm):
    class Meta:
        model = CustomerOrders
        fields = ['status']

class OrderDeliveryStatusForm(forms.ModelForm):
    class Meta:
        model = OrderDeliveryStatus
        fields = '__all__'


class ClienteVehiculoForm(forms.ModelForm):
    class Meta:
        model = ClienteVehiculo
        fields = '__all__'
