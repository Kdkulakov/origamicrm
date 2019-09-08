from django import forms
from django.forms import DateInput, TextInput, Textarea, Select, CharField
from .models import Material, MaterialInstance


class MaterialrModelForm(forms.ModelForm):

    class Meta:
        model = Material
        fields = ['name', 'category', 'short_desc', 'detail', 'count', 'count_full', 'units']
        widgets = {
            'category': Select(attrs={'class': 'form-control'}),
            'name': TextInput(attrs={'class': 'form-control'}),
            'short_desc': TextInput(attrs={'class': 'form-control'}),
            'detail': Textarea(attrs={'class': 'form-control'}),
            'count': TextInput(attrs={'class': 'form-control col-xs-2'}),
            'count_full': TextInput(attrs={'class': 'form-control'}),
            'units': Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(MaterialrModelForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.id:
            self.fields['count'].required = False
            self.fields['count'].widget.attrs['disabled'] = 'disabled'


class MaterialModelFormCount(forms.ModelForm):

    class Meta:
        model = Material
        fields = ['count']
        widgets = {
            'count': TextInput(attrs={'class': 'form-control'}),
        }


class MaterialInstanceForm(forms.ModelForm):

    class Meta:
        model = MaterialInstance
        fields = ['material']
        widgets = {
            'material': Select(attrs={'class': 'form-control'}),
        }
