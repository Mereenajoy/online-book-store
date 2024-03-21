from django import forms
from . models import *


class  checkoutform(forms.ModelForm):
    class Meta:
        model=Orders
        fields=["address","mobile"]
        
class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['order_status']

