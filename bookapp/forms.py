from django import forms
from .models import Student,Room

Room_type=[
    ('s','Single'),
    ('d','Double'),
    ('t','Triple'),
]

class RoomForm(forms.ModelForm):
    room_type=forms.ChoiceField(choices=Room_type,required=True)
    class Meta:
        model=Student
        fields = ['name', 'reg_no', 'email', 'room_type']
        

class SelectForm(forms.Form):
    room_no = forms.ChoiceField(choices=[])
    def __init__(self, room_choices=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if room_choices:
            self.fields['room_no'].choices = room_choices
            