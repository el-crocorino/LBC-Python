#-*- coding: utf-8 -*-

from django import forms

class RummageAddForm (forms.Form):
    user_id = forms.CharField(max_length=10, label=u"Id utilisateur", required=True)
    title = forms.CharField(max_length=100, label=u"Nom :", required=True)
    url = forms.CharField(label=u"URL : ", help_text=u"Collez ici l'adresse de votre page de recherche", required=True)