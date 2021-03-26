from myapp import views
from django.contrib import admin 
from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
  
from .views import (Signup ,
                    Home, 
                    Loginview ,
                    Search ,
                    logout_request ,
                    update_data ,
                    upload_profile_pic ,
                    upload_cover_pic,friends ,
                    invites_received_view ,
                    profiles_list_view,
                    invite_profiles_list_view,
                    ProfileListView,
                    send_invatation,
                    remove_from_friends,
                    accept_invatation,
                    reject_invatation,
                

)

app_name = "myapp"   
  
urlpatterns = [ 
    path('', Signup, name="signup" ),
    path('home/',Home ,name="homepage"),
    path('login/',Loginview) ,
    path('search/',Search),
    path('logout', logout_request, name='logout'),
    # path('upload/', views.image_upload_view),
    path('updatedata/<int:id>/', update_data , name='updatedata'),
    path('uploaddp/<int:id>/', upload_profile_pic , name='uploadprofilepic'),
    path('uploadcover/<int:id>/', upload_cover_pic , name='uploadcoverpic'),
    path('friends/', friends , name ='friends'),
    path('my-invites/', invites_received_view , name ='my-invites-view'),
    path('all-profiles/', ProfileListView.as_view() , name ='all-profiles-view'),
    path('to-invite/', invite_profiles_list_view , name ='invite-profiles-view'),
    path('send-invite/', send_invatation , name ='send-invite'),
    path('remove-friend/', remove_from_friends , name ='remove-friend'),
    path('my-invites/accept/', accept_invatation , name ='accept-friend'),
    path('my-invites/reject/', reject_invatation , name ='reject-friend'),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

] 


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)


    
