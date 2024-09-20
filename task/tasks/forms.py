from django import forms
from django.contrib.auth import get_user_model
from .models import UserInfo, Task
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model() #User
        fields = ['username', 'email', 'password1', 'password2']

        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        # }

class XYZ_DateInput(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        # kwargs["format"] = "%d-%m-%Y"
        super().__init__(**kwargs)
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'performance', 'content', 'parity', 'chose']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-control'}),
            'performance': XYZ_DateInput(format=["%Y-%m-%d"], ),

        }

class EditForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'performance', 'content', 'parity', 'chose', 'made']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5, 'class': 'form-control'}),
            'performance': XYZ_DateInput(format=["%Y-%m-%d"], ),

        }

class EditUserForm(forms.ModelForm):
    # Пробовала сделать отбор через перечисления но не смогла в форму не связанную с моделью заносить данные
    # по заданному отбора, чтобы они стояли на нужных значениях.

    # SORT = [(0, 'Срок, срочность'), (1, 'Срочность, срок')]
    # PARITY = [(0, 'Все'), (1, 'Срочно'), (2, 'Несрочно')]
    # MADES = [(0, 'Все'), (1, 'Невыполнено'), (2, 'Выполнено')]
    # CHOSE = [(0, 'Все'), (1, 'Избрано'), (2, 'Неизбрано')]
    # SELECTE = [(0, 'Все'), (1, 'Текст'), (2, 'Дата')]
    #
    # sorted=forms.ChoiceField(choices=SORT,label='сортировка')
    # made = forms.ChoiceField(choices=MADES,label='выполнено')
    # parity = forms.ChoiceField(choices=PARITY,label='срочно')
    # chose = forms.ChoiceField(choices=CHOSE,label='избрано')
    # selection = forms.ChoiceField(choices=SELECTE,label='отбор')
    # selection_key = forms.CharField(label='отбор по тексту', widget=forms.TextInput(attrs={'class': 'form-control'}))
    # selection_date= XYZ_DateInput(format=["%Y-%m-%d"])
    #
    # # def __init__(self, **kwargs):
    # #     inform = get_user_model().pk
    # #     info= UserInfo.objects.get(user=inform)
    # #     self.sorted=info.sorted
    # #     self.made = info.made
    # #     self.parity = info.parity
    # #     self.chose = info.chose
    # #     self.selection = info.selection
    # #     self.selection_key=info.selection_key
    # #     self.selection_date=info.selection_date
    # #     super().__init__(**kwargs)

    # sorted=forms.BooleanField(label='сортировка по сроку', widget=forms.BooleanField())
    # made = forms.BooleanField(label='выполнено', widget=forms.BooleanField())
    # parity = forms.BooleanField(label='срочно', widget=forms.BooleanField())
    # chose = forms.BooleanField(label='избрано', widget=forms.BooleanField())
    # selection = forms.BooleanField(label='отбор', widget=forms.BooleanField())
    # selection_key = forms.CharField(label='по ключу', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = UserInfo
        fields = ['sorted', 'parity', 'chose', 'made', 'selection',  'selection_key']
        # fields = ['sorted', 'parity', 'chose', 'made','selection','selection_date','selection_key']
        # widgets = {
        #     'selection_date': XYZ_DateInput(format=["%Y-%m-%d"], ),
        # }

