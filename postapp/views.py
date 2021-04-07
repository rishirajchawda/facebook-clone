from django.shortcuts import redirect, render, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Post
from .forms import Postform
from django.contrib.auth.decorators import login_required
from .models import Comment, Like
from django.http import JsonResponse


def createpost(request):
    if request.method == 'POST':
        fm = Postform(request.POST, request.FILES)

        if fm.is_valid():
            post = fm.save()
            post.user = request.user
            post.save()
            # fm = Postform()
            return redirect("/home/")
    else:
        fm = Postform()

    return render(request, 'post.html', {'form': fm})


def delete_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('del_id')
        model_data = Post.objects.get(pk=post_id)
        model_data.delete()

    return JsonResponse({'': ""})


@login_required
def showpost(request):
    posts = Post.objects.all()
    user = request.user

    return render(request, 'home.html', {'post': posts, 'user': user})


# def post_detailview(request):

#   if request.method == 'POST': 
#     cf = CommentForm(request.POST or None) 
#     import pdb;pdb.set_trace()
#     if cf.is_valid(): 
#       content = request.POST.get('content') 
#       comment = Comments.objects.create(user = request.user, content = content) 
#       comment.save() 
#       return redirect("/home/")  
#   else: 
#     cf = CommentForm() 

#     context ={ 
#       'comment_form':cf, 
#       } 
#     return render(request, 'comments.html', context)


def detailpost(request, id):
    post = Post.objects.get(id=id)
    comments = Comment.objects.filter(post=post, parent=None)

    return render(request, "detail.html", {'post': post, 'comments': comments})


def commentview(request):
    if request.method == "GET":
        content = request.GET.get('content')
        postid = request.GET.get('postid')
        post = Post.objects.get(id=postid)
        # import pdb; pdb.set_trace()
        Comment.objects.create(post=post, user=request.user, content=content)

        return HttpResponseRedirect('/detail/' + str(postid))


@login_required
def reply(request):
    if request.method == "GET":
        content = request.GET.get('content')
        postid = request.GET.get('postid')
        commentid = request.GET.get('commentid')

        post = Post.objects.get(id=postid)
        comment = Comment.objects.get(id=commentid)

        Comment.objects.create(post=post, user=request.user, content=content, parent=comment)

        return HttpResponseRedirect('/detail/' + str(postid))


def like_posts(request):
    user = request.user
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)

        if user in post_obj.likes.all():
            post_obj.likes.remove(user)

        else:
            post_obj.likes.add(user)

            like, created = Like.objects.get_or_create(user=user, post_id=post_id)

            if not created:
                if like.value == 'Like':
                    like.value == 'Unlike'
                else:
                    like.value == 'Like'
            else:
                like.value = 'like'

                post_obj.save()
                like.save()

            data = {
                'value': like.value,
                'likes': post_obj.likes.all().count()
            }
            return JsonResponse(data, safe=False)
    return redirect("/home/")
