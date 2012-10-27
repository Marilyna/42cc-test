from django import forms
from django.contrib.auth import authenticate

from contacts.models import Contact
from contacts.widgets import CalendarWidget


class LoginForm(forms.Form):
    login = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        user = authenticate(username=self.cleaned_data.get('login'),
                            password=self.cleaned_data.get('password'))
        if user is None:
            raise forms.ValidationError("Wrong login or password")
        if not user.is_active:
            raise forms.ValidationError("Your account is disabled")
        self.user = user
        return self.cleaned_data


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ('name', 'last_name', 'birth_date', 'email', 'jabber',
                  'skype', 'other_contacts', 'bio', 'photo')
        widgets = {
            'other_contacts': forms.Textarea(attrs={'rows': 4}),
            'bio': forms.Textarea(attrs={'rows': 4}),
            'birth_date': CalendarWidget(),
        }
