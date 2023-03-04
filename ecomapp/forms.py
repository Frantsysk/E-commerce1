from django import forms
from .models import Review, PaymentMethod, Product, Customer
from multiupload.fields import MultiImageField, MultiMediaField


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'rating': forms.Select(choices=Review.RATING_CHOICES, attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class PaymentMethodForm(forms.ModelForm):
    class Meta:
        model = PaymentMethod
        fields = [
            'name',
            'card_number',
            'expiry_month',
            'expiry_year',
            'cvv',
            'billing_address',
            'billing_city',
            'billing_state',
            'billing_zip_code',
            'billing_country'
        ]
        labels = {
            'name': 'Name on Card',
            'card_number': 'Card Number',
            'expiry_month': 'Expiration Month',
            'expiry_year': 'Expiration Year',
            'cvv': 'CVV',
            'billing_address': 'Billing Address',
            'billing_city': 'Billing City',
            'billing_state': 'Billing State',
            'billing_zip_code': 'Billing Zip Code',
            'billing_country': 'Billing Country'
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control'}),
            'expiry_month': forms.TextInput(attrs={'class': 'form-control'}),
            'expiry_year': forms.TextInput(attrs={'class': 'form-control'}),
            'cvv': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_address': forms.Textarea(attrs={'class': 'form-control'}),
            'billing_city': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_state': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_zip_code': forms.TextInput(attrs={'class': 'form-control'}),
            'billing_country': forms.TextInput(attrs={'class': 'form-control'})
        }


class ProductForm(forms.ModelForm):
    attachments = MultiMediaField(media_type='image', min_num=0, max_num=5, max_file_size=1024 * 1024 * 5)

    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'description', 'brand', 'category', 'seller', 'quantity', 'video']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'brand': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'seller': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'video': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }


class ProductFilterForm(forms.Form):
    product_name = forms.CharField(max_length=100, required=False, label='Product Name')

    def __init__(self, *args, **kwargs):
        seller = kwargs.pop('seller')
        super().__init__(*args, **kwargs)
        self.fields['product_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['product_name'].queryset = Product.objects.filter(seller=seller)

    def clean(self):
        cleaned_data = super().clean()
        product_name = cleaned_data.get('product_name')
        if product_name:
            # Update the queryset to filter by the entered product name
            self.fields['product_name'].queryset = self.fields['product_name'].queryset.filter(name__icontains=product_name)
        return cleaned_data


class CustomerFilterForm(forms.Form):
    customer_name = forms.CharField(max_length=100, required=False, label='Customer Name')

    def __init__(self, *args, **kwargs):
        seller = kwargs.pop('seller')
        super().__init__(*args, **kwargs)
        self.fields['customer_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['customer_name'].queryset = Customer.objects.filter(orders__products__seller=seller).distinct()

    def clean(self):
        cleaned_data = super().clean()
        customer_name = cleaned_data.get('customer_name')
        if customer_name:
            # Update the queryset to filter by the entered customer name
            self.fields['customer_name'].queryset = self.fields['customer_name'].queryset.filter(user__username__icontains=customer_name)
        return cleaned_data


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False, label='')
