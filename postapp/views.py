from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from .models import UserPost
from .forms import Postform
from django.contrib.auth.decorators import login_required


def createpost(request):
    if request.method == 'POST':
        fm = Postform(request.POST,request.FILES)

        if fm.is_valid():
            post = fm.save()
            post.user = request.user
            post.save()
            # fm = Postform()
            return redirect("/home/")
    else:
        fm = Postform()
    
    return render(request, 'post.html', { 'form':fm })


@login_required
def showpost(request):

    posts = UserPost.objects.all()

    return render(request,'show.html',{'post':posts})