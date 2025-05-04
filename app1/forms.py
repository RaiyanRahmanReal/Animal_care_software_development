from django import forms
from .models import Petadd  #Petadd modelfrom 
from .models import DaycareRequest
from django.core.exceptions import ValidationError
class PetForm(forms.ModelForm):
    class Meta:
        model = Petadd 
        fields = ['name', 'age', 'breed', 'identifying_marks', 'price', 'image']  
class PaymentForm(forms.Form):
    name_on_card = forms.CharField(label='Name on Card', max_length=100)
    card_number = forms.CharField(label='Card Number', max_length=16, min_length=16)
    expiry_date = forms.CharField(label='Expiry Date (MM/YY)', max_length=5)
    cvv = forms.CharField(label='CVV', max_length=4, min_length=3)



class AdoptionForm(forms.ModelForm):
    class Meta:
        model = Petadd
        fields = ['name', 'age', 'breed', 'identifying_marks', 'image']  


class DaycareRequestForm(forms.ModelForm):
    class Meta:
        model = DaycareRequest
        fields = ['pet_name', 'breed', 'age', 'identifying_marks', 'start_date', 'end_date', 'pet_photo']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

    pet_photo = forms.ImageField(required=True)

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            # Check if end date is earlier than start date
            if end_date < start_date:
                raise ValidationError('End date cannot be earlier than start date.')

        return cleaned_data

        


