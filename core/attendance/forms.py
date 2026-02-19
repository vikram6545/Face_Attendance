from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile, Semester


class StudentSignupForm(forms.ModelForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Username'
        })
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Email'
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Password'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })
    )
    semester = forms.ModelChoiceField(
        queryset=Semester.objects.filter(is_active=True),
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = StudentProfile
        fields = ['roll_no', 'semester', 'face_baseline']

        widgets = {
            'roll_no': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Roll Number'
            }),
            'face_baseline': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }


from .models import StudentQuery

class QueryForm(forms.ModelForm):
    class Meta:
        model = StudentQuery
        fields = ['name', 'roll_no', 'email', 'reason']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Aapka Naam'}),
            'roll_no': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Roll Number'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email ID'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Apni samasya likhein...'}),
        }