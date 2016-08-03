#-*- coding: utf-8 -*-

from django import forms
from django.forms import ModelForm, widgets
from app.models import Rummage, Criteria, Rummage_item

class RummageAddForm (forms.Form):
    user_id = forms.CharField(max_length=10, label=u"Id utilisateur", required=True)
    title = forms.CharField(max_length=100, label=u"Nom :", required=True)
    url = forms.CharField(label=u"URL : ", help_text=u"Collez ici l'adresse de votre page de recherche", required=True)   
    
    
    
class CriteriaAddForm (ModelForm):

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
            })
        }        
    
#class Rummage_itemAddForm (ModelForm):    
class Rummage_itemAddForm (forms.Form):    
    rummage_id = forms.IntegerField(label=u"Id recherche", required=True)
    selected = forms.BooleanField()
    lbc_id = forms.IntegerField()    
    name = forms.CharField(max_length=200)
    url = forms.CharField()
    thumbnail_url = forms.CharField()
    price = forms.CharField()
    infos = forms.CharField()   
    
    #class Meta:
        #model = Rummage_item
        #exclude = ('rummage', 'created_date','updated_date')  
        #labels = {
            #"name": "Nom :",
            #"price": "Prix:"
        #}        
        #widgets = {
            #'weight': widgets.NumberInput( attrs = {
                #'step' : '0.01',
                #'min' : '0.0',
                #'max' : '1.0',
            #})
        #}  
        
class ConfForm(forms.Form):
    """
    Formulaire de configuration du module
    """
    format_x = forms.IntegerField( label="Largeur", required=True, min_value=0, widget=forms.TextInput(attrs={'placeholder':'mm','class':'form-control input-sm'}) )
    format_y = forms.IntegerField( label="Hauteur", required=True, min_value=0, widget=forms.TextInput(attrs={'placeholder':'mm','class':'form-control input-sm'}) )
    
class SorteForm(forms.Form):

    #Champs multiples
    designation = forms.CharField( label="Désignation", required=True, widget=forms.TextInput(attrs={'placeholder':'','class':'form-control input-sm'}) )
    quantite = forms.IntegerField( label="Quantité", required=True, min_value=0, widget=forms.TextInput(attrs={'placeholder':'','class':'form-control input-sm'}) )
    rectoverso = forms.ChoiceField(label='',choices = [(False,'Recto Seul'),(True,'Recto Verso')],required=True,widget=forms.Select( attrs={'class':'form-control input-sm'}))