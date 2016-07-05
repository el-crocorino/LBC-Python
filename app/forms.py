#-*- coding: utf-8 -*-

from django import forms

class RummageAddForm (forms.Form):
    user_id = forms.CharField(max_length=10, label=u"Id utilisateur", required=True)
    title = forms.CharField(max_length=100, label=u"Nom :", required=True)
    url = forms.CharField(label=u"URL : ", help_text=u"Collez ici l'adresse de votre page de recherche", required=True)
    
class CriteriaAddForm (forms.Form):
    #rummage_id = forms.IntegerField(max_length=10, label=u"Id recherche", required=True)
    name = forms.CharField(max_length=100, label=u"Nom :", required=True)
    weight = forms.FloatField(label=u"Poids (0,1; 0,3; ...) : ", help_text=u"La somme de l'ensemble des critères doit être égale à 1", min_value=0.0, max_value=1.0, required=True)
