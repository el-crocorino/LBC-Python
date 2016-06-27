from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from datetime import datetime

def home(request):
	text = """<h1>Bienvenue sur le blog</h1><p>J'aime bien chercher des annonces et les comparer</p>"""

	return HttpResponse(text)

def article_view(request, article_id):
	"""Displays article with given id"""
	
	if int(article_id) > 100:
		raise Http404
	text = """Vous avez demandé l'article # {0}.""".format(article_id)
	
	return HttpResponse(text)

def article_list(request, year, month):
	"""Lists articles of given year & month"""
	
	if  int(year) < 2014 :
		return redirect(redirection_view)
	
	text = """Vous avez demandé les articles parus en {0}/{1}""".format(month, year)
	return HttpResponse(text)

def redirection_view(request):
	return HttpResponse('Vous avez été redirigé.')

def tpl(request):
	return render(request, 'app/tpl.html', {'current_date' : datetime.now()})