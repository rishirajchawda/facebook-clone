from postapp import views
from django.conf import settings
from django.conf.urls.static import static

from django.urls import path 
from .views import createpost, showpost ,detailpost,commentview,reply,like_posts

app_name = "postapp"   
  
urlpatterns = [ 
    path('createpost/',createpost ,name="create_post"),
    path('showpost/',showpost ,name="showpost"),
    path('comment/',commentview ,name="comment"),
    path('detail/<int:id>/',detailpost ,name="detail"),
    path('reply/',reply ,name="reply"),
    path('like/',like_posts ,name="like-posts"),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)