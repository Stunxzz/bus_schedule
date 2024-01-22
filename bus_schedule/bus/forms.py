from django import forms

from bus_schedule.bus.models import ScheduleModel


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label='Име')
    password = forms.CharField(widget=forms.PasswordInput, label='Парола')


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = ScheduleModel
        fields = "__all__"

