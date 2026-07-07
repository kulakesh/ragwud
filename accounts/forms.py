from django import forms
from .models import CustomUser
from django.contrib.auth import authenticate


class UserForm(forms.ModelForm):
    
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'name']

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['password'].required = False
    def clean_password(self):
        password = self.cleaned_data.get(
            'password'
        )

        if not password and self.instance.pk:

            return password
        
        if not password and not self.instance.pk:

            raise forms.ValidationError(
                "Password is required"
            )

        return password
    def clean_username(self):

        username = self.cleaned_data.get(
            'username'
        )

        qs = CustomUser.objects.filter(
            username=username
        )

        if self.instance.pk:

            qs = qs.exclude(
                pk=self.instance.pk
            )

        if qs.exists():

            raise forms.ValidationError(
                "Username already exists"
            )

        return username
    def save( self, commit=True ):

        user = super().save(
            commit=False
        )

        password = self.cleaned_data.get( 'password' )

        # NEW PASSWORD ENTERED
        if password:
            user.set_password(
                password
            )

        # KEEP OLD PASSWORD
        elif not password and self.instance.pk:

            old_user = CustomUser.objects.get( pk=self.instance.pk )

            user.password = old_user.password


        if commit:

            user.save()

        return user
class LoginForm(forms.Form):

    username = forms.CharField()

    password = forms.CharField( widget=forms.PasswordInput() )

    def clean(self):

        cleaned_data = super().clean()

        username = cleaned_data.get( 'username' )

        password = cleaned_data.get( 'password' )

        user = authenticate(
            username=username,
            password=password
        )
        
        if not user:

            raise forms.ValidationError(
                "Invalid username or password"
            )

        self.user = user

        return cleaned_data