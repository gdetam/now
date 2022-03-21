from django import forms

from captcha.fields import CaptchaField

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from now.models import CustomUser, Event


class RegisterUserForm(UserCreationForm):
    """class RegisterUserForm using for registration users."""

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-input'}))

    class Meta:
        model = CustomUser

        fields = (
            'username',
            'email'
        )


class UpdateUserForm(UserChangeForm):
    """class UpdateUserForm using for update user`s information."""

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.CharField(label='Электронная почта', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    photo = forms.ImageField(label='Фото', widget=forms.FileInput(attrs={'class': 'form-input'}))
    location = forms.CharField(label='Город', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password_conf = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = CustomUser

        fields = (
            'username',
            'email',
            'photo',
            'bio',
            'location',
            'password',
            'password_conf'
        )
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'bio': forms.Textarea(attrs={'cols': 40, 'rows': 5}),
            'password': forms.TextInput(attrs={'class': 'form-input'}),
            'password_conf': forms.TextInput(attrs={'class': 'form-input'})
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username) > 200:
            raise ValidationError('Длина имени превышает 200 символов')

        return username


class LoginUserForm(AuthenticationForm):
    """class LoginUserForm using for login users."""

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class AddEventForm(forms.ModelForm):
    """class AddEventForm using for create event."""

    captcha = CaptchaField(label='Проверочный код', error_messages={'invalid': 'Ошибка проверки кода'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Event

        fields = [
                  'title',
                  'content',
                  'photo',
                  'category'
        ]
        widgets = {
                   'title': forms.TextInput(attrs={'class': 'form-input'}),
                   'content': forms.Textarea(attrs={'cols': 40, 'rows': 5})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина названия превышает 200 символов')

        return title


class UpdateEventForm(forms.ModelForm):
    """class UpdateEventForm using for update event`s info."""

    captcha = CaptchaField(label='Проверочный код', error_messages={'invalid': 'Ошибка проверки кода'})
    photo = forms.ImageField(label='Фото', widget=forms.FileInput(attrs={'class': 'form-input'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Event

        fields = [
                  'title',
                  'content',
                  'photo',
                  'category'
        ]
        widgets = {
                   'title': forms.TextInput(attrs={'class': 'form-input'}),
                   'content': forms.Textarea(attrs={'cols': 40, 'rows': 5})
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина названия превышает 200 символов')

        return title
