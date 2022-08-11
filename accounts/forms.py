from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms


class EditProfileForm(forms.ModelForm):
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Jméno", max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Příjmení", max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',)

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)

        # CSS styling
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = 'Uživatelské jméno'
        self.fields['username'].help_text = ""


class SignUpForm(UserCreationForm):  # with bootstrap 5 styling(widgets, form-control)
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label="Jméno",max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label="Příjmení", max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        # CSS styling
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].label = 'Uživatelské jméno'
        self.fields['username'].help_text = ""
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].label = 'Heslo'
        self.fields['password1'].help_text = '<ul class="form-text text-muted"><small>' \
                                             '<li>Nesmí být podobné Vašemu uživatelskému jménu</li>' \
                                             '<li>Musí být alespoň 8 znaků dlouhé</li>' \
                                             '<li>Nesmí se skládat pouze z čísel' \
                                             '</small></ul>'
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].label = 'Heslo znovu'
        self.fields['password2'].help_text = ""


class ChangePasswordForm(PasswordChangeForm):

    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)

        #CSS styling
        self.fields['old_password'].widget.attrs['class'] = 'form-control'
        self.fields['old_password'].label = 'Současné heslo'
        self.fields['old_password'].help_text = ""
        self.fields['new_password1'].widget.attrs['class'] = 'form-control'
        self.fields['new_password1'].label = 'Nové Heslo'
        self.fields['new_password1'].help_text = '<ul class="form-text text-muted"><small>' \
                                             '<li>Nesmí být podobné Vašemu uživatelskému jménu</li>' \
                                             '<li>Musí být alespoň 8 znaků dlouhé</li>' \
                                             '<li>Nesmí se skládat pouze z čísel' \
                                             '</small></ul>'
        self.fields['new_password2'].widget.attrs['class'] = 'form-control'
        self.fields['new_password2'].label = 'Nové heslo znovu'
        self.fields['new_password2'].help_text = ""
