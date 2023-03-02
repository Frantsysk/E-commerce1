from django import forms
from .models import Review, PaymentMethod, Product
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
    attachments = MultiMediaField(media_type='image', min_num=1, max_num=5, max_file_size=1024 * 1024 * 5)

    class Meta:
        model = Product
        fields = ['name', 'price', 'image', 'description', 'brand', 'category', 'seller', 'quantity', 'video']
        # widgets = {
        #     'more_images': forms.ClearableFileInput(attrs={'multiple': True}),
        # }

#
# class AttachmentForm(forms.Form):
#     attachments = MultiImageField(min_num=1, max_num=5, max_file_size=1024*1024*5)