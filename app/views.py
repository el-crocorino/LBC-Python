from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, Http404
from django.contrib.auth.models import User
from datetime import datetime
from app.models import Rummage, Criteria, Rummage_item
from urllib.parse import urlparse

def home(request):	
	rummages = Rummage.objects.all()
	context = {
	        'rummages_list':rummages
	}
	
	return render(request, 'app/index.html', context)

def rummage(request, rummage_id):		
	
	rummage = get_object_or_404(Rummage, id = rummage_id)
	criterias = Criteria.objects.filter(rummage_id = rummage.id)	
	query = getRummageQueryInformations(rummage)
	savedAdsList = getSavedAdsList(rummage)
	ads_list = getAdsList(rummage)
	
	context = {
	        'rummage':rummage, 
	        'criterias':criterias,
	        'query': query,	 
	        'savedAdsList' : savedAdsList,
	        'ads_list' : ads_list,
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

def rummage_delete(request, rummage_id):
	
	rummage = get_object_or_404(Rummage, id=rummage_id)
	rummage_items = Rummage_item.objects.filter(rummage_id=rummage.id)
	criterias = Criteria.objects.filter(rummage_id=rummage.id)
	
	for rummage_item in rummage_items:
		rummage_item.delete();
	for criteria in criterias:
		criteria.delete();
		
	rummage.delete();
	
	return redirect('app:rummage_list', user_id=1)	

def rummage_update(request, rummage_id):
	
	rummage = get_object_or_404(Rummage, id=rummage_id)
	
	if request.method == 'POST':

		form = RummageAddForm(request.POST)
		
		if( form.is_valid()):
			
			user_id = int(form.cleaned_data['user_id'])
			title = form.cleaned_data['title']
			url = form.cleaned_data['url']
						
			rummage.title = title
			rummage.url = url
			rummage.updated_date = datetime.now()		
			rummage.save()
			
			send = True
			
	else :
		form = RummageAddForm({
		      'user_id': rummage.user_id,
		      'title': rummage.title,
		      'url': rummage.url,
		})
		
	return render(request, 'app/rummage_update.html', locals())
	

def rummage_list(request, user_id):
	
	rummages = Rummage.objects.all()
	context = {
	        'rummages_list':rummages
	}
	
	return render(request, 'app/index.html', context)


def criteria(request, criteria_id):	

	criteria = get_object_or_404(Criteria, id=criteria_id)

	context = {
	        'criteria':criteria,       
	}

	return render(request, 'app/criteria.html', context)

from app.forms import CriteriaAddForm

def criteria_add(request, rummage_id):
	
	rummage = get_object_or_404(Rummage, id=rummage_id)

	if request.method == 'POST':

		form = CriteriaAddForm(request.POST)

		if( form.is_valid()):

			name = form.cleaned_data['name']
			weight = float(form.cleaned_data['weight'])

			criteria = Criteria()
			criteria.rummage = rummage
			criteria.name = name
			criteria.weight = weight
			criteria.save()

			send = True

	else :
		form = CriteriaAddForm()

	return render(request, 'app/criteria_add.html', locals())

def criteria_delete(request, criteria_id):

	criteria = get_object_or_404(Criteria, id=criteria_id)
	rummage_id = criteria.rummage_id
	#notes = Notes.objects.filter(criteria_id=criteria.id)

	#for criteria_item in criteria_items:
		#criteria_item.delete();
	# for note in notes:
	# 	note.delete();

	criteria.delete();
	
	#return redirect('app:rummage_list', user_id=1)	
	#return redirect('app:criteria_list', rummage_id=rummage_id)
	return redirect('app:rummage', rummage_id=rummage_id)	

def criteria_update(request, criteria_id):

	criteria = get_object_or_404(Criteria, id=criteria_id)
	rummage = Rummage.objects.get(id=criteria.rummage_id)
	#rummage_id = criteria.rummage_id

	if request.method == 'POST':

		form = CriteriaAddForm(request.POST)

		if( form.is_valid()):
			
			name = form.cleaned_data['name']
			weight = form.cleaned_data['weight']
			
			criteria.name = name
			criteria.weight = weight
			criteria.updated_date = datetime.now()
			criteria.save()

			send = True


	else :
		form = CriteriaAddForm({
		        'name': criteria.name,
		        'weight': criteria.weight,
		})

	return render(request, 'app/criteria_update.html', locals())
	

def criteria_list(request, user_id):
	criterias = Criteria.objects.all()
	context = {
	        'criterias_list':criterias
	}

	return render(request, 'app:criteria_list', context)

def rummage_item(request, rummageItemId):
	
	rummageItem = get_object_or_404(Rummage_item, id = rummageItemId)
	rummage = Rummage.objects.filter(id = rummageItem.rummage_id)
	criterias = Criteria.objects.filter(rummage_id = rummageItem.rummage_id)
	context = {
	        'rummageItem':rummageItem, 
	        'rummage' : rummage,
	        'criterias':criterias,
	}
	
	return render(request, 'app/rummage_item.html', context)

from app.forms import Rummage_itemAddForm

def rummage_item_add(request, rummage_id):
	
	if request.method == 'POST':
	
		form = Rummage_itemAddForm(request.POST)
		price = float(form.data['price'][:-2])
		price *= 10
		print(price)
		print(price * 10)
		
		if( form.is_valid()):	
					
			rummage = get_object_or_404(Rummage, id = form.data['rummage_id'])
			
			rummage_item = Rummage_item()
			rummage_item.rummage = rummage
			rummage_item.lbc_id = form.data['lbc_id']
			rummage_item.name = form.data['name']
			rummage_item.url = form.data['url']
			rummage_item.thumbnail_url = form.data['thumbnail_url']
			rummage_item.price = form.data['price'][:2] 
			rummage_item.infos = form.data['infos']
			
			rummage_item.save()
			
			send = True
			
	else :
		form = RummageAddForm()
	
	criterias = Criteria.objects.filter( rummage_id = rummage.id)	
	query = getRummageQueryInformations( rummage)	
	savedAdsList = getSavedAdsList(rummage)	
	ads_list = getAdsList( rummage)
	
	context = {
	        'rummage':rummage, 
	        'criterias':criterias,
	        'query': query,	  
	        'savedAdsList' : savedAdsList,
	        'ads_list' : ads_list,
	}
	
	return render(request, 'app/rummage.html', context)

def rummage_item_delete(request, rummageItemId):
	
	rummageItem = get_object_or_404(Rummage_item, id = rummageItemId)
	#notes = Rummage_item.objects.filter(rummage_item_id = rummageItemId)
	rummageId = rummageItem.rummage_id
	
	#for note in notes:
		#note.delete()
		
	rummageItem.delete()
	
	rummage = get_object_or_404(Rummage, id = rummageId)
	criterias = Criteria.objects.filter( rummage_id = rummage.id)	
	query = getRummageQueryInformations( rummage)
	savedAdsList = getSavedAdsList(rummage)	
	ads_list = getAdsList( rummage)
	
	context = {
	        'rummage':rummage, 
	        'criterias':criterias,
	        'query': query,	  
	        'savedAdsList' : savedAdsList,	        
	        'ads_list' : ads_list,
	}
	
	return render(request, 'app/rummage.html', context)	

def rummage_item_update(request, rummage_id):
	
	rummage = get_object_or_404(Rummage, id=rummage_id)
	if request.method == 'POST':

		form = RummageAddForm(request.POST)
		
		if( form.is_valid()):
			
			user_id = int(form.cleaned_data['user_id'])
			title = form.cleaned_data['title']
			url = form.cleaned_data['url']
						
			rummage.title = title
			rummage.url = url
			rummage.updated_date = datetime.now()		
			rummage.save()
			
			send = True
			
	else :
		form = RummageAddForm({
		      'user_id': rummage.user_id,
		      'title': rummage.title,
		      'url': rummage.url,
		})
		
	return render(request, 'app/rummage_update.html', locals())
	

def rummage_item_list(request, user_id):
	
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


def getAdsList(rummage):

	from urllib.request import urlopen
	from bs4 import BeautifulSoup	
	import json		

	ads_list = {}		

	#import codecs
	#page = codecs.open('/media/Docs/DEV/LBC/Examples/liste.html', 'r', 'windows-1252').read()

	page = urlopen(rummage.url).read()
	soup = BeautifulSoup(page)
	soup.prettify()
	
	savedAdsIdList = Rummage_item.objects.values_list('lbc_id', flat = True).filter(rummage_id = rummage.id)
	
	for anchor in soup.findAll('a', href=True):

		anchor_class = anchor.get('class')

		if anchor_class != None and 'list_item' in anchor_class:

			item_price = anchor.find_all('h3', 'item_price')[0].contents[0];

			item_image_container = anchor.find_all('span', class_='item_imagePic')[0].contents
			ad_image_href = 'https:' + item_image_container[1].get('data-imgsrc')			

			item_infos = json.loads(anchor['data-info'])

			adlist_id = item_infos.get('ad_listid')
			
			if( adlist_id != None and int(adlist_id) not in savedAdsIdList):
								
				ads_list[adlist_id] = {
					'title' : anchor['title'],
					'href' : anchor['href'],
					'data_info' : anchor['data-info'],
					'price' : item_price,
					'img_src' : ad_image_href,
				}

	return ads_list

def getSavedAdsList(rummage):
	
	rummageItemsList = Rummage_item.objects.filter(rummage_id = rummage.id)		
	
	savedAdsList = {}
	
	for item in rummageItemsList:
		savedAdsList[str(item.lbc_id)] = {
		        'id' : item.id,
		        'name' : item.name,
		        'url' : item.url,
		        'infos' : item.infos,
		        'price' : item.price,
		        'thumbnail_url' : item.thumbnail_url,
		        'updated_date' : item.updated_date,
		}	
		
	return savedAdsList


def getRummageQueryInformations(rummage) :
	
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
	        'text' : query_text,	       
	}

	if( 3 in path_components):
		query['city'] = path_components[3]
		
	return query