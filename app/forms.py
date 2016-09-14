#-*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm, widgets
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from app.models import Rummage, Criteria, Rummage_item, Note

class RummageAddForm (forms.Form):
    title = forms.CharField(max_length=100, label=u"Nom :", required=True)
    url = forms.CharField(label=u"URL : ", help_text=u"Collez ici l'adresse de votre page de recherche", required=True)     
    
class CriteriaAddForm (ModelForm):
    
    id_rummage = forms.CharField(widget = forms.HiddenInput())
    criteriaId = forms.CharField(required = False, widget = forms.HiddenInput())    

    class Meta:
        model = Criteria
        exclude = ( 'rummage', 'created_date','updated_date')  
        labels = {
            "name": "Nom :",
            "weight": "Poids (0,1; 0,3; ...) :"
        }        
        widgets = {
            'weight': widgets.NumberInput( attrs = {
                'step' : '0.01',
                'min' : '0.0',
                'max' : '1.0',
            }), 
        }    
    
    def clean(self):
        
        cleaned_data = super(CriteriaAddForm, self).clean()
        criterias = Criteria.objects.filter(rummage_id = cleaned_data.get('id_rummage'))

        criteriaWeightSum = 0;

        for criteria in criterias:

            if( criteria.id != int(cleaned_data.get('criteriaId'))):
                criteriaWeightSum += criteria.weight
        
        criteriaWeightSum += int(cleaned_data.get('weight'))
        
        if( criteriaWeightSum > 1):
            raise forms.ValidationError(
                _('La somme des poids de tous les critères ne doit pas être supérieur à 1: %(value)s'),
                code='invalid',
                params={'value': "{0:.2f}".format( round( criteriaWeightSum, 2))},
            )

  
class Rummage_itemAddForm (forms.Form):    
    rummage_id = forms.IntegerField(label=u"Id recherche", required=True)
    selected = forms.BooleanField()
    lbc_id = forms.IntegerField()    
    name = forms.CharField(max_length=200)
    url = forms.CharField()
    thumbnail_url = forms.CharField()
    price = forms.CharField()
    infos = forms.CharField()   

class NoteAddForm (ModelForm):

    class Meta:
        model = Note
        fields = ['note'] 
        labels = {
                    "note": "Note :",
                }        
        widgets = {
            'note': widgets.NumberInput( attrs = {
                'step' : '0.01',
                'min' : '0.0',
                'max' : '5.0',
            })
        }         
        
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
        
class RegistrationForm(forms.Form):
        
    username = forms.RegexField(regex=r'^\w+$', widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=u"Nom d'utilisateur", error_messages={ 'invalid': u"Votre nom d'utilisateur ne doit contenir que des chiffres, des lettres ou des tirets bas" })
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(required=True, max_length=30)), label=u"Email")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=u"Mot de passe")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=dict(required=True, max_length=30, render_value=False)), label=u"Vérification")
        
    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except User.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(u"Ce nom d'utilisateur existe déjà. Essayez-en un autre")
        
    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(u"Les deux mots de passe ne correspondent pas.")
        return self.cleaned_data        