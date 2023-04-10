from django.contrib import admin
from .models import MyModel,Review,MyList,Tag
# Register your models here.
admin.site.register(MyModel)
admin.site.register(Review)
admin.site.register(MyList)
admin.site.register(Tag)
