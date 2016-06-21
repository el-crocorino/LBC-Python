from django.db import models

class Rummage(models.Model):
    title = models.CharField(max_length=200)
    created_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Creation date")
    updated_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Update date")
    
    def __str__(self):
        return self.title    

class Criteria(models.Model):
    rummage = models.ForeignKey('rummage', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    pound = models.IntegerField()
    created_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Creation date")
    updated_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Update date")
    
    def __str__(self):
        return self.name    
    
class Rummage_item(models.Model):
    rummage = models.ForeignKey('rummage', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    link = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Creation date")
    updated_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Update date")
    
    def __str__(self):
        return self.name    
    
class Note(models.Model):
    rummage_item = models.ForeignKey('rummage_item', on_delete=models.CASCADE)
    criteria = models.ForeignKey('criteria', on_delete=models.CASCADE)
    note = models.TextField(null=True)
    created_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Creation date")
    updated_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Update date")
    
    def __str__(self):
        return self.note
    

