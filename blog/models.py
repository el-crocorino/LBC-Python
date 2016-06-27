from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=42)
    content = models.TextField(null=True)
    creation_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Publication date")
    update_date = models.DateTimeField(auto_now_add=True, auto_now= False, verbose_name="Publication date")

    def __unicode__(self):
        return u"%s" % self.title
