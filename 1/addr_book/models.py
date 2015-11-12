from django.db import models
# Create your models here.

class Author(models.Model):
    Author_ID = models.CharField(max_length=30)
    Country = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    sex = models.BooleanField(default=True)
    Age = models.CharField(max_length=10)
    def _unicode_(self):
        return self.name
class Book(models.Model):
    ISBN = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(Author,related_name="arthor_book")
    price = models.CharField(max_length=10)
    pub_house = models.CharField(max_length=30)
    pub_date = models.CharField(max_length=30)
    def _unicode_(self):
        return self.name