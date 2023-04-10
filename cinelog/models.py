from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=8,blank=True,null=True)
    def __str__(self):
        return str(self.name)




class MyModel(models.Model):
    title = models.CharField(max_length=100)
    number = models.IntegerField(blank=True,null=True)
    image = models.ImageField(upload_to='images/',blank=True,null=True)
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE,blank=True,null=True)
    tags = models.ManyToManyField(Tag,blank=True)


    def __str__(self):
        return str(self.title)

class MyList(models.Model):
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE,blank=True,null=True)
    movie = models.ForeignKey(MyModel,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)

    
class Review(models.Model):
    cinema = models.ForeignKey(MyModel, on_delete=models.CASCADE)
    review = models.TextField(max_length=10000)
    datetime = models.DateTimeField(default=timezone.now,blank=True,null=True)
    user = models.ForeignKey('auth.User',on_delete=models.CASCADE,blank=True,null=True)

    
 
    def __str__(self):
        return str(self.cinema)


