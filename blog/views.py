from django.shortcuts import render
from django.http import HttpResponse

def home(request):
	text = """<h1>Bienvenue sur le blog</h1><p>J'aime bien chercher des annonces et les comparer</p>"""

	return HttpResponse(text)
