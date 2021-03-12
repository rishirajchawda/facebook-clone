from postapp import views
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path 
from .views import createpost, showpost

app_name = "postapp"   
  
urlpatterns = [ 
    path('createpost/',createpost ,name="createpost"),
    path('showpost/',showpost ,name="showpost"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)