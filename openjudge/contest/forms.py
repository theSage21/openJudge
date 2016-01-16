from django.forms import Form, CharField, PasswordInput, ModelChoiceField
from django.contrib.auth.models import User
from django.forms import ModelForm
from contest import models


class RegistrationForm(Form):
    username = CharField(label='Username: ', max_length=50)
    password = CharField(widget=PasswordInput)
    def is_valid(self):
        valid = super (Form, self).is_valid()
        if not valid:
            return valid
        uname = self.cleaned_data['username']
        users = User.objects.filter(username=uname).count()
        if users > 0:
            self._errors['Validation_Error'] = 'The username is taken. Pick a new one'
            return False
        else:
            return True


class AttemptForm(ModelForm):
    class Meta:
        model = models.Attempt
        exclude = ['profile', 'question', 'stamp', '_correct', 'remarks']


class ProfileForm(ModelForm):
    class Meta:
        model = models.Profile
        exclude = ['user', 'allowed']
