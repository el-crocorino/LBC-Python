from django.db import models
from django.conf import settings

from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup	
import json

class Rummage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Creation date")
    updated_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Update date")
    
    def __str__( self):
        return self.title    
    
    def getAdsList( self):		
    
        adsList = {}		
    
        #import codecs
        #page = codecs.open('/media/Docs/DEV/LBC/Examples/liste.html', 'r', 'windows-1252').read()
    
        page = urlopen(self.url).read()
        soup = BeautifulSoup(page)
        soup.prettify()
    
        savedAdsIdList = Rummage_item.objects.values_list('lbc_id', flat = True).filter(rummage_id = self.id)
    
        for anchor in soup.findAll( 'a', href = True):
    
            anchorClass = anchor.get('class')
    
            if anchorClass != None and 'list_item' in anchorClass:
    
            # Todo : créer ici un objet rummage_item et le remplir, 
            # déplacer les méthodes getAdPrice etc.. dans le modèle Rummage_item. 
            # Implémenter une méthode toArray au model Rummage_item
    
                item = {}
    
                item['data_info'] = json.loads( anchor['data-info'])			
                item['price'] = self.getAdPrice( anchor)					
                item['type']= item['data_info'].get( 'ad_offres')
                item['img_src'] = self.getAdImageUrl( anchor)
                item['title'] = self.getAdTitle(anchor)		
                item['listId'] = item['data_info'].get( 'ad_listid')
                item['href'] = anchor['href']
    
                if( item['listId'] != None and int( item['listId']) not in savedAdsIdList):
                    adsList[item['listId']] = item
    
        return adsList
    
    def getSavedAdsList( self):
    
        rummageItemsList = Rummage_item.objects.filter(rummage_id = self.id)		
    
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
    
    
    def getQueryInformations( self) :
    
        urlparts = urlparse(self.url);
    
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
    
    def updateRummagesScores( self):
        
        rummage = get_object_or_404( Rummage, id = self.id)	
        rummageItems = Rummage_item.objects.filter( rummage_id = self.id)	
        criterias = Criteria.objects.filter( rummage_id = self.id)
    
        for rummageItem in rummageItems :
            rummageItem.score = rummageItem.getScore( criterias)
            rummageItem.updated_date = datetime.now()
            rummageItem.save()	
    
    def getAdImageUrl( self, anchor):
    
        itemImageContainer = anchor.find_all('span', class_='item_imagePic')[0].contents						
        adImageHref = 'https:'	
        itemImageContainer = list(filter(lambda x: x!= '\n', itemImageContainer))
    
        if (len(itemImageContainer) > 0 and itemImageContainer != ['\n']):
            if( itemImageContainer[0].name == 'img') :
                adImageHref += itemImageContainer[0].get('src')
            elif( itemImageContainer[0].name == 'span') : 
                adImageHref += itemImageContainer[0].get('data-imgsrc')
    
        return adImageHref
    
    def getAdPrice( self, anchor):
    
        itemPriceContainer = anchor.find_all('h3', 'item_price')
        itemPrice = 0
    
        if len(itemPriceContainer) > 0:
            itemPrice = itemPriceContainer[0].contents[0]	
    
        return itemPrice
    
    def getAdTitle( self, anchor):
    
        itemTitleContainer = anchor.find_all('p', 'item_title')
        itemTitle = ''
    
        if len(itemTitleContainer) > 0:		
            itemTitle = itemTitleContainer[0].contents[0]	
        else :
            itemTitle = anchor['title']
    
        return itemTitle

class Criteria(models.Model):
    rummage = models.ForeignKey('rummage', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    weight = models.FloatField()
    created_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Creation date")
    updated_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Update date")
    
    def __str__(self):
        return self.name    
    
class Rummage_item(models.Model):
    rummage = models.ForeignKey('rummage', on_delete=models.CASCADE)
    lbc_id = models.IntegerField(null = False, unique = True)    
    name = models.CharField(max_length=200)
    url = models.TextField()
    thumbnail_url = models.TextField(null=True)
    price = models.FloatField(null=True)
    infos = models.TextField(null=True)
    score = models.FloatField(null=False, default=0.0)
    created_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Creation date")
    updated_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Update date")
    
    def __str__( self):
        return self.name    
    
    def getNotesList( self):
    
        notes = Note.objects.filter(rummage_item_id = self.id)	
        notesList = {}
    
        for note  in notes:
            notesList[note.criteria_id] = note.note
    
        return notesList
    
    
    def getScore( self, criterias):
    
        notes = Note.objects.filter(rummage_item_id = self.id)	
        score = 0.00
    
        if( len(notes) >0):
            for note in notes:
                for criteria in criterias:
                    if (note.criteria_id == criteria.id):
                        score += float(note.note) * float(criteria.weight)
    
        return score    
        
    
class Note(models.Model):
    rummage_item = models.ForeignKey('rummage_item', on_delete=models.CASCADE)
    criteria = models.ForeignKey('criteria', on_delete=models.CASCADE)
    note = models.FloatField(null=False, default=0.0)
    created_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Creation date")
    updated_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Update date")
    
    def __str__(self):
        return self.note
    

