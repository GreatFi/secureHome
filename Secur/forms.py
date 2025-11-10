from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms
from .models import signup, Addproperty
from django import forms
from .models import Addproperty

GENDER_CHOICES= [
    ('male', 'Male'),
    ('female', 'Female')
]

        
class Createaccount1(UserCreationForm):

    username=forms.CharField(
        label="username",
        required=True,
        max_length=50,

        widget=forms.TextInput(attrs={
            'placeholder' : 'Enter your first name',
            'class' : 'firstname-input'
        })
    ) 
    first_name=forms.CharField(
        label="FirstName",
        required=True,
        max_length=50,

        widget=forms.TextInput(attrs={
            'placeholder' : 'Enter your first name',
            'class' : 'firstname-input'
        })
    )
    last_name=forms.CharField(
        label="LastName",
        required=True,
        max_length=50,

        widget=forms.TextInput(attrs={
            'placeholder' : 'Enter your last name',
            'class' : 'lastname-input'
        })

    )
    email=forms.EmailField(
        label="Email",
        required=True,
        max_length=50,

        widget=forms.EmailInput(attrs={
            'placeholder' : 'Enter your Email',
            'class' : 'emailaddy-input'
        })

    )

    dob=forms.DateField(
        label="Date of Birth",
        required=True,

        widget=forms.DateInput(attrs={
            'type': 'date',
            'placeholder' : 'Enter your Date of Birth',
            'class' : 'date-input'
        })

    )

    gender=forms.ChoiceField(
        label="Gender",
        required=True,
        choices=[('', "Select gender")] + GENDER_CHOICES,
        widget=forms.Select(attrs={
            'placeholder' : 'Select an option ',
            'class' : ''
        })

    )

    phone=forms.IntegerField(
        label="Phone",
        required=True,

        widget=forms.NumberInput(attrs={
            'placeholder' : 'Enter your phone number',
            'class' : 'phone-input'
        })

    )

    password1=forms.CharField(
        label="Password",
        required=True,

        widget=forms.PasswordInput(attrs={
            'placeholder' : 'Enter your password',
            'class' : 'pass-cont-input'
        })

    )
    password2=forms.CharField(
        label="Confirm Password",
        required=True,

        widget=forms.PasswordInput(attrs={
            'placeholder' : 'Enter your password',
            'class' : 'conpass-input'
        })

    )


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'gender', 'password1', 'password2', 'dob']  

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists")
        return username
    def clean_email(self):
        email = self.cleaned_data.get("email")

        if User.objects.filter(email=email):
            raise ValidationError("This Email is already in use")
        return email
    def clean_dob(self):
        dob = self.cleaned_data.get("dob")     
        if User.objects.check(dob=dob).exists():
            raise ValidationError("Must be above 18 to signup")
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get("first_name")
        user.last_name = self.cleaned_data.get("last_name")

        if commit:
            user.save()
            signup.objects.create(
                user=user, 
                dob=self.cleaned_data.get("dob"),
                gender=self.cleaned_data.get("gender"),   
                phone = self.cleaned_data.get("phone") 
            )
        return user    

class LoginForm(AuthenticationForm):

    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'placeholder' : 'Enter your username',
            'class' : 'email-input'
        })
    )
    
    password = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder' : 'Enter your password',
            'class' : 'password-input'
        })
    )

