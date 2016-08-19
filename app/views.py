from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, render_to_response
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect

from datetime import datetime
from urllib.parse import urlparse
from app.models import Rummage, Criteria, Rummage_item, Note
from app.forms import RegistrationForm, RummageAddForm, CriteriaAddForm, Rummage_itemAddForm, NoteAddForm

@login_required
def home(request):	
	return redirect('app:rummage_list')

def login(request):	
	
	if request.method == 'POST':
	
		#form = RummageAddForm(request.POST)
			
		#if( form.is_valid()):
			logged_in = False
			userUsername = request.POST['inputUsername']
			password = request.POST['inputPassword']
			user = authenticate(username = userUsername, password = password)
			
			msg = []			
				
			if user is not None:
			
				if user.is_active:
					auth_login(request, user)
					logged = True	
					msg.append({'alert-success' : "Login successful"})
					#return redirect('app:rummage_list', {'errors': msg})
					return redirect('app:rummage_list')			
					# Redirect to a success page.
				else:
					print("Inactive User")
					msg.append({'alert-error' : "Inactive User"})	
					# Return a 'disabled account' error message
					return render(request, 'app/login.html', {'errors': msg})
			
			else:
				print("No User")
				msg.append({'alert-error' : "No User"})
				# Return an 'invalid login' error message.
				return render(request, 'app/login.html', {'errors': msg})	
				
				
		#else :
			#form = RummageAddForm()
			
	else : 
		if request.user.is_authenticated():
			return redirect('app:rummage_list', request.user.id)			
		else :
			return render(request, 'app/login.html')

def logout(request):	
	auth_logout(request)
	return redirect('app:home')


@csrf_protect
def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
			        username=form.cleaned_data['username'],
			        password=form.cleaned_data['password1'],
			        email=form.cleaned_data['email']
			)
			return HttpResponseRedirect('/accounts/register/success/')
	else:
		form = RegistrationForm()

	variables = RequestContext(request, {
	        'form': form
	})

	return render_to_response(
	        'registration/register.html',
	        variables,
	)

def register_success(request):
	return render_to_response(
	        'registration/register_success.html',
	)

@login_required
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


@login_required
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


@login_required
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


@login_required
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
	

@login_required
def rummage_list(request):
		
	current_user = request.user
	rummages = Rummage.objects.filter(user_id = current_user.id)	
	
	context = {
                'rummages_list':rummages
        }		

	return render(request, 'app/index.html', context)


@login_required
def criteria(request, criteria_id):	

	criteria = get_object_or_404(Criteria, id=criteria_id)

	context = {
	        'criteria':criteria,       
	}

	return render(request, 'app/criteria.html', context)


@login_required
def criteria_add(request, rummage_id):
	
	rummage = get_object_or_404(Rummage, id=rummage_id)

	if request.method == 'POST':

		form = CriteriaAddForm(request.POST, initial={"id_rummage": rummage_id})

		if( form.is_valid()):

			name = form.cleaned_data['name']
			weight = float(form.cleaned_data['weight'])

			criteria = Criteria()
			criteria.rummage = rummage
			criteria.name = name
			criteria.weight = weight
			criteria.save()
			
			updateRummagesScores(criteria.rummage_id)			

			send = True

	else :
		form = CriteriaAddForm(initial={"id_rummage": rummage_id})

	return render(request, 'app/criteria_add.html', locals())


@login_required
def criteria_delete(request, criteria_id):

	criteria = get_object_or_404(Criteria, id = criteria_id)
	rummage_id = criteria.rummage_id
	notes = Note.objects.filter(criteria_id = criteria.id)

	for note in notes:
	 	note.delete();

	criteria.delete();
	updateRummagesScores(criteria.rummage_id)
	
	return redirect('app:rummage', rummage_id=rummage_id)	


@login_required
def criteria_update(request, criteria_id):

	criteria = get_object_or_404(Criteria, id = criteria_id)
	rummage = Rummage.objects.get(id = criteria.rummage_id)
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
			
			updateRummagesScores(criteria.rummage_id)

			send = True


	else :
		form = CriteriaAddForm({
		        'name': criteria.name,
		        'weight': criteria.weight,
		})

	return render(request, 'app/criteria_update.html', locals())
	

@login_required
def criteria_list(request, user_id):
	criterias = Criteria.objects.all()
	context = {
	        'criterias_list':criterias
	}

	return render(request, 'app:criteria_list', context)


@login_required
def rummage_item(request, rummageItemId):
	
	rummageItem = get_object_or_404(Rummage_item, id = rummageItemId)
	rummage = Rummage.objects.filter(id = rummageItem.rummage_id)[0]
	criterias = Criteria.objects.filter(rummage_id = rummageItem.rummage_id)	
	notes_list = getNotesList(rummageItemId)

	context = {
	        'rummageItem':rummageItem, 
	        'rummage' : rummage,
	        'criterias':criterias,
	        'notes_list' : notes_list,
	}
	
	return render(request, 'app/rummage_item.html', context)


@login_required
def rummage_item_add(request, rummage_id):
			
	rummage = get_object_or_404(Rummage, id = rummage_id)
	
	if request.method == 'POST':
	
		form = Rummage_itemAddForm(request.POST)
		price = float(form.data['price'][:-2])
		price *= 10
		
		if( form.is_valid()):						
			
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


@login_required
def rummage_item_delete(request, rummageItemId):
	
	rummageItem = get_object_or_404(Rummage_item, id = rummageItemId)
	notes = Note.objects.filter(rummage_item_id = rummageItemId)
	rummageId = rummageItem.rummage_id
	
	for note in notes:
		note.delete()
		
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


@login_required
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
	

@login_required
def rummage_item_list(request, user_id):
	
	rummages = Rummage.objects.all()
	context = {
	        'rummages_list':rummages
	}
	
	return render(request, 'app/index.html', context)


@login_required
def note_add(request, rummageItemId):
	
	rummageItem = get_object_or_404(Rummage_item, id = rummageItemId)

	if request.method == 'POST':

		form = NoteAddForm(request.POST, initial={"rummage_item_id": rummageItemId})
	
		#if( form.is_valid()):
		for key, value in form.data.items():
			
			if( key != 'csrfmiddlewaretoken'):
				
				noteQuery = Note.objects.filter(rummage_item_id = rummageItemId).filter(criteria_id = key)				
				
				if( len(noteQuery) != 0 ): 
					note = noteQuery[0]
				else:
					note = Note();
					note.created_date = datetime.now()
				
				note.criteria_id = int(key)
				note.rummage_item_id = rummageItemId
				note.note = float(value)				
				note.updated_date = datetime.now()
				
				note.save()	
								
	rummage = Rummage.objects.get(id = rummageItem.rummage_id)
	criterias = Criteria.objects.filter(rummage_id = rummageItem.rummage_id)
	
	rummageItem.score = getScore(rummage, criterias, rummageItem)
	rummageItem.updated_date = datetime.now()
	rummageItem.save()
		
	context = {
	        'rummageItemId':rummageItemId,
	        'rummageItem':rummageItem,
	        'rummage' : rummage,
	        'criterias' : criterias,
	        'notes_list' : getNotesList(rummageItemId),        
	}
		
	return render(request, 'app/rummage_item.html', context)	

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

			item_price = anchor.find_all('h3', 'item_price')[0].contents[0]
			item_image_container = anchor.find_all('span', class_='item_imagePic')[0].contents						
			ad_image_href = 'https:'
			
			if (item_image_container != ['\n']): 
				ad_image_href += item_image_container[1].get('data-imgsrc')			
				
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
		        'score' : item.score,
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

def getNotesList(rummageItemId):
	
	notes = Note.objects.filter(rummage_item_id = rummageItemId)	
	notesList = {}
	
	for note  in notes:
		notesList[note.criteria_id] = note.note

	return notesList

def getScore(rummage, criterias, rummageItem):
		
	notes = Note.objects.filter(rummage_item_id = rummageItem.id)	
	score = 0.00
	
	if( len(notes) >0):
		for note in notes:
			for criteria in criterias:
				if (note.criteria_id == criteria.id):
					score += float(note.note) * float(criteria.weight)
	
	return score
	
def updateRummagesScores(rummageId):
		
	rummage = get_object_or_404(Rummage, id = rummageId)	
	rummageItems = Rummage_item.objects.filter(rummage_id = rummageId)	
	criterias = Criteria.objects.filter(rummage_id = rummageId)
	
	for rummageItem in rummageItems:
		rummageItem.score = getScore(rummage, criterias, rummageItem)
		rummageItem.updated_date = datetime.now()
		rummageItem.save()	
		
	
	
		