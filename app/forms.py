#-*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm
from app.models import Rummage, Criteria, Rummage_item

class RummageAddForm (forms.Form):
    user_id = forms.CharField(max_length=10, label=u"Id utilisateur", required=True)
    title = forms.CharField(max_length=100, label=u"Nom :", required=True)
    url = forms.CharField(label=u"URL : ", help_text=u"Collez ici l'adresse de votre page de recherche", required=True)   
    
class CriteriaAddForm (ModelForm):
#class CriteriaAddForm (forms.Form):
    #rummage_id = forms.IntegerField(label=u"Id recherche", required=True, widget=forms.HiddenInput())
    #name = forms.CharField(max_length=100, label=u"Nom :", required=True)
    #weight = forms.FloatField(label=u"Poids (0,1; 0,3; ...) : ", help_text=u"La somme de l'ensemble des critères doit être égale à 1", min_value=0.0, max_value=1.0, required=True)

    class Meta:
        model = Criteria
        exclude = ('id', 'rummage_id', 'created_date','updated_date') 
    
class Rummage_itemAddForm (forms.Form):    
    #rummage_id = forms.IntegerField(max_length=10, label=u"Id recherche", required=True)
    selected = forms.BooleanField()
    lbc_id = forms.IntegerField()    
    name = forms.CharField(max_length=200)
    #url = forms.CharField()
    #thumbnail_url = forms.CharField()
    price = forms.CharField()
    #infos = forms.CharField()
