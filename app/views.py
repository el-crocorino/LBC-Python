from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from datetime import datetime
from app.models import Rummage, Criteria
from urllib.parse import urlparse

def home(request):	
	rummages = Rummage.objects.all()
	context = {
	        'rummages_list':rummages
	}
	
	return render(request, 'app/index.html', context)

def rummage(request, rummage_id):	
	
	rummage = get_object_or_404(Rummage, id=rummage_id)
	criterias = Criteria.objects.filter(rummage_id=rummage.id)
	
	urlparts = urlparse(rummage.url);

	path_components = urlparts.path.strip('/').split('/')	
	query_components = urlparts.query.split('&')
	
	query_text = ''
	
	i = 0
	for component in path_components:
		path_components[i] = component.replace('_', ' ').capitalize()
		i += 1
	
	for component in query_components:
		if( 'q=' in component):
			query_text = component[2:].replace('%20', ' ')
	
	query = {
	       'category' : path_components[0],
	       'region' : path_components[2],
	       'city' : path_components[3],
	       'text' : query_text,	       
	}
	
	print(query)
	
	
	context = {
	        'rummage':rummage, 
	        'criterias':criterias,
	        'query': query,	        
	}
	
	return render(request, 'app/rummage.html', context)

from app.forms import RummageAddForm

def rummage_add(request):
	
	if request.method == 'POST':

		form = RummageAddForm(request.POST)
		
		if( form.is_valid()):
			
			user_id = int(form.cleaned_data['user_id'])
			title = form.cleaned_data['title']
			url = form.cleaned_data['url']
						
			rummage = Rummage()
			rummage.user = User.objects.get(id=user_id)
			rummage.title = title
			rummage.url = url
			rummage.save()
			
			send = True
			
			
	else :
		form = RummageAddForm()
		
	return render(request, 'app/rummage_add.html', locals())
	

def rummage_list(request, user_id):
	rummages = Rummage.objects.all()
	context = {
	        'rummages_list':rummages
	}
	
	return render(request, 'app/index.html', context)

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
	context = {
	        'current_date' : datetime.now()
	}
	
	return render(request, 'app/tpl.html', context)