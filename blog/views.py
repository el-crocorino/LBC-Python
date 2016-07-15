from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from datetime import datetime
from blog.models import Article
from django.core.urlresolvers import reverse

def home(request):
	articles = Article.objects.all()
	return render(request, 'blog/home.html', {'articles_list':articles})

def read(request, id):
	pass


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
	return render(request, 'blog/tpl.html', {'current_date' : datetime.now()})