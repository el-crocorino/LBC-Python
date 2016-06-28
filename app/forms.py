#-*- coding: utf-8 -*-

from django import forms

class RummageAddForm (forms.Form):
    title = forms.CharField(max_length=100, label=u"Nom de votre recherche", required=True)
    url = forms.CharField(label=u"URL de votre recherche", help_text=u"Collez ici l'adresse de votre page de recherche", required=True)