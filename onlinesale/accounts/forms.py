from django import forms
from django.forms import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model

User=get_user_model()

#djangoformfields
class SignInForm(forms.Form):
    email = forms.EmailField(label="",widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email'}))
    pwd = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))

class RegisterForm(forms.Form):
    email = forms.EmailField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Email'}))
    fullname = forms.CharField(label="",widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Full Name'}))
    mobile = forms.IntegerField(label="",widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'mobile'}))
    pwd = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Password'}))
    cpwd = forms.CharField(label="",widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Confirm Password'}))

    def clean(self):
        if self.cleaned_data.get('pwd') != self.cleaned_data.get('cpwd'):
            raise ValidationError("Mismatch Password")
        return self.cleaned_data

    def clean_email(self):
        if User.objects.filter(email__exact = self.cleaned_data.get('email')).exists():
            raise ValidationError("Email already exists")
        return self.cleaned_data.get("email")
class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'mobile')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin', 'full_name', 'mobile','staff')
    
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]