from django.contrib import admin
from django.urls import path, include

<<<<<<< HEAD
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('myapp.urls')),
=======

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', include('myapp.urls')),
    
>>>>>>> d105de0 (Your commit message describing the changes)
]