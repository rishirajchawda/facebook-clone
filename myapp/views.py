from pdb import set_trace
from django.dispatch.dispatcher import receiver
from django.shortcuts import get_object_or_404, render ,redirect
from django.views.generic import View ,ListView
from .forms import Fbform ,ExtendForm ,UpdateForm ,UploadDP ,UploadBanner
from django.contrib.auth import authenticate , login ,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Profile , Relationship
from django.db.models import Q
from django.contrib import messages
from postapp.models import Post ,Like ,Comment
from postapp.forms import Postform 
from django.contrib.auth.models import User

 
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

            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/home/')
            
            # return render(request, 'register.html', {'form' : Fbform(),'form2' : ExtendForm()},)
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

    datas = Post.objects.order_by('-date_posted')
    comments=Comment.objects.all()

    
  

    posts = Post.objects.all()

    return render(request,'home.html',{'profile':profile,'post':posts ,
    'form':fm , 'form2':fm2 ,'form3':fm3 ,'form4':fm4 
    ,'user':user , 'likepost':likepost ,'comments':comments,'datas': datas,
    })

def friends(request):
    profile=Profile.objects.get(user=request.user)  
    return render(request,'friends.html',{'profile':profile,})


def Loginview(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request ,username = username , password = password)

        if user is not None:
            login(request , user)
            return redirect('/home/')
        
        else:
            messages.error(request,'username or password not correct')
            return redirect('/')

    else:
        return render(request, 'register.html',)


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

def invites_received_view(request):
    profile = Profile.objects.get(user=request.user) 
    qs = Relationship.objects.invatations_received(profile)
    results = list(map(lambda x: x.sender,qs))
    is_empty = False
    if len(results) == 0:
        is_empty = True


    context = { 'qs':results,'is_empty':is_empty }

    return render(request ,'my_invites.html' ,context)

def accept_invatation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)

        rel = get_object_or_404(Relationship , sender=sender , receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'

            rel.save()
    return redirect('myapp:my-invites-view')


def reject_invatation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)

        rel = get_object_or_404(Relationship , sender=sender , receiver=receiver)
        rel.delete()
    return redirect('myapp:my-invites-view')
 
def invite_profiles_list_view(request):
    user=request.user 
    qs = Profile.objects.get_all_profile_to_invite(user)

    context = { 'qs':qs }

    return render(request ,'to_invite_list.html' ,context) 


def profiles_list_view(request):
    user=request.user 
    qs = Profile.objects.get_all_profiles(user)

    context = { 'qs':qs }

    return render(request ,'profile_list.html' ,context) 


class ProfileListView(ListView):
    model = Profile
    template_name = 'profile_list.html'
    # context_object_name = 'qs'

    def get_queryset(self):
        qs = Profile.objects.get_all_profiles(self.request.user)
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact = self.request.user)
        profile = Profile.objects.get(user = user)
        rel_r = Relationship.objects.filter(sender = profile)
        rel_s = Relationship.objects.filter(receiver = profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)

        for item in rel_s:
            rel_sender.append(item.sender.user)

        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['is_empty'] = False

        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context


def send_invatation(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('myapp:home')

def remove_from_friends(request):
    if request.method == "POST":
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.get((Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender) ))
        rel.delete()

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('myapp:home')       

