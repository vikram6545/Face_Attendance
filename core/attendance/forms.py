from django import forms
from django.contrib.auth.models import User
from .models import StudentProfile
from .models import StudentQuery,Course, Year, Semester

class StudentSignupForm(forms.ModelForm):

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

    class Meta:
        model = User
        fields = ['username', 'email']   # 🔥 ONLY USER FIELDS

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match ❌")

        return cleaned_data
    
class StudentProfileForm(forms.ModelForm):
    course = forms.ModelChoiceField(
        queryset=Course.objects.all(),
        empty_label="Select Course",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    year = forms.ModelChoiceField(
        queryset=Year.objects.all(),
        empty_label="Select Year",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    semester = forms.ModelChoiceField(
        queryset=Semester.objects.all(),
        empty_label="Select Semester",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    
    class Meta:
        model = StudentProfile
        fields = ['roll_no','course','year', 'semester', 'face_baseline']

        widgets = {
            'roll_no': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Roll Number'
            }),
            'face_baseline': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),
        }    

class QueryForm(forms.ModelForm):
    class Meta:
        model = StudentQuery
        fields = ['name', 'email', 'roll_no', 'reason']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'roll_no': forms.TextInput(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control'}),
        }