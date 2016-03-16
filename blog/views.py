from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	text = """<h1>Bienvenue sur le blog</h1><p>J'aime bien chercher des annonces et les comparer</p>"""

	return HttpResponse(text)

def article_view(request, article_id):
	"""Displays article with given id"""
	text = """Vous avez demandé l'article # {0}.""".format(article_id)
	
	return HttpResponse(text)


