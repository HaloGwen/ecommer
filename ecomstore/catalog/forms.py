from django import forms
from django.contrib import admin
from .models import Category, Product


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if price <= 0:
            raise forms.ValidationError("Price must be greater than 0")
        return price


class ProductAddToCartForm(forms.Form):
    quantity = forms.IntegerField(
        widget=forms.TextInput(
            attrs={"size": "2", "value": "1", "class": "quantity", "maxlength": "5"}
        ),
        error_messages={
            "invalid": "Please enter a valid quantity.",
        },
        min_value=1,
    )
    product_slug = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        super(ProductAddToCartForm, self).__init__(*args, **kwargs)

    def clean(self):
        if self.request:
            if not self.request.session.test_cookie_worked():
                raise forms.ValidationError("Cookies must be enabled")
        return self.cleaned_data