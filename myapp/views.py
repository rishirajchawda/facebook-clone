from pdb import set_trace
from django.shortcuts import render ,redirect
from django.views.generic import View
from .forms import Fbform ,ExtendForm ,UpdateForm ,UploadDP ,UploadBanner
from django.contrib.auth import authenticate , login ,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Profile
from django.db.models import Q
from django.contrib import messages
from postapp.models import Post ,Like
from postapp.forms import Postform 

 
def Signup(request):
    if request.method == "POST":
        form = Fbform(request.POST)
        form2 = ExtendForm(request.POST)
        if form.is_valid() and form2.is_valid :
            user2 = form2.save(commit=False)
            user = form.save()
            user.user=user2
            user = form.save()
            user.refresh_from_db()
            user.profile.first_name = form.cleaned_data.get('first_name')
            user.profile.last_name = form.cleaned_data.get('last_name')
            user.profile.email = form.cleaned_data.get('email')
            user.profile.gender = form2.cleaned_data.get('gender')
            # user.profile.birth_date = form2.cleaned_data.get('birth_date')
            user.save()
            
            return render(request, 'register.html', {'form' : Fbform(),'form2' : ExtendForm()},)
        else:
            return render(request, 'register.html', {'form' : Fbform(request.POST),'form2' : ExtendForm(request.POST)})
    else:
        form = Fbform()
        form2=ExtendForm()
        return render(request, 'register.html', {'form': form ,'form2': form2})         


@login_required
def Home(request):

    fm=Postform()
    fm2 = UpdateForm()
    fm3 = UploadDP()
    fm4 = UploadBanner()
    # fm5 = CommentForm()
    user = request.user
    likepost = Like.objects.all()


    profile=Profile.objects.get(user=request.user) 
    posts = Post.objects.all()

    return render(request,'home.html',{'profile':profile,'post':posts ,
    'form':fm , 'form2':fm2 ,'form3':fm3 ,'form4':fm4 ,'user':user , 'likepost':likepost})


def Loginview(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request ,username = username , password = password)

        if user is not None:
            login(request , user)
            return redirect('/home/')
        
        else:
            return HttpResponse("Username and password is invalid")


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("/")


def Search(request):
    
    query = request.GET['query']
    allUser = Profile.objects.filter(Q(user__first_name__icontains = query)
     | Q(user__last_name__icontains = query))   
    params = {'allUser': allUser ,'query':query }
    return render(request, 'search.html', params)


# def image_upload_view(request):
    
#     if request.method == 'POST':
#         form = ImageForm(request.POST, request.FILES)

#         if form.is_valid():
#             form.save(request.user)

#             img_obj=Profile.objects.get(user=request.user)
#             return render(request, 'home.html', {'form': form, 'img_obj': img_obj})
#     else:
#         form = ImageForm()
#     return render(request, 'home.html', {'form': form})


@login_required
def update_data(request ,id):
    if request.method == "POST":
        model_data = Profile.objects.get(pk=id)
        fm = UpdateForm(request.POST,instance=model_data)
        if fm.is_valid:
            fm.save()
            return redirect('/home/')
    else:
        model_data = Profile.objects.get(pk=id)
        fm = UpdateForm(instance = model_data)
    return render(request ,'updatedata.html' , {'form':fm})


@login_required
def upload_profile_pic(request ,id):
    if request.method == "POST":
        model_data = Profile.objects.get(pk=id)
        fm3 = UploadDP(request.POST , request.FILES ,instance=model_data)
        if fm3.is_valid():
            fm3.save()
            return redirect("/home/")

    else:
        model_data = Profile.objects.get(pk=id)
        fm3 = UploadDP(instance = model_data)
    return render(request ,'upload_dp.html' , {'form3':fm3})   


@login_required
def upload_cover_pic(request ,id):
    if request.method == "POST":
        model_data = Profile.objects.get(pk=id)
        fm4 = UploadBanner(request.POST , request.FILES ,instance=model_data)
        if fm4.is_valid():
            fm4.save()
            return redirect("/home/")

    else:
        model_data = Profile.objects.get(pk=id)
        fm4 = UploadBanner(instance = model_data)
    return render(request ,'uploadcover.html' , {'form4':fm4})      
