from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group

User = get_user_model()

#customuserchange


#userform
class UserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ['username','email','city','contact','address','password','role']
        # excludes = ['']
        widgets = {
        'password': forms.PasswordInput(),
        }
        label = {
            'password': 'Password'
        }

    # def __init__(self, *args, **kwargs):
    #     if kwargs.get('instance'):
    #         # We get the 'initial' keyword argument or initialize it
    #         # as a dict if it didn't exist.                
    #         initial = kwargs.setdefault('initial', {})
    #         # The widget for a ModelMultipleChoiceField expects
    #         # a list of primary key for the selected data.
    #         if kwargs['instance'].groups.all():
    #             initial['role'] = kwargs['instance'].groups.all()[0]
    #         else:
    #             initial['role'] = None

    #     forms.ModelForm.__init__(self, *args, **kwargs)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user    
    # def save(self):
    #     password = self.cleaned_data.pop('password')
    #     # role = self.cleaned_data.pop('role')
    #     u = super().save()

    #     u.set_password(password)
    #     u.save()
    #     return u

    