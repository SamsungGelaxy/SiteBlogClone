from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.defaultfilters import add
from django.template.loader import render_to_string
from django.db.models import Count
from .forms import CommentForm, LoginForm, PostForm, PostPointForm, RegistrationForm, UserEditForm, SearchForm
from django.http import HttpResponse
# Create your views here.
from .models import Post, PostPoint, Comment
from django.views.generic import ListView
from django.contrib.auth import authenticate, login
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
@login_required
def editProfile(r):
    user_edit_form=UserEditForm(instance=r.user)
    if r.method=="POST":
        user_edit_form = UserEditForm(r.POST, instance=r.user)
        if user_edit_form.is_valid():
            user_edit_form.save()
            return redirect("blog:profile")
    return render(r, "blog/account/edit_profile.html", {"form": user_edit_form})
def sign_up(r):
    form=RegistrationForm()
    if r.method=="POST":
        form=RegistrationForm(r.POST)
        if form.is_valid():
            nuser=User.objects.create_user(**form.cleaned_data)
            nuser.save()
            login(r, authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"]))

            return redirect("blog:post_list")
    return render(r, "registration/sign_up.html", {"user_form":form})

@login_required
def edit_post_point(request, id):
    p = get_object_or_404(PostPoint, id=id)

    edit_form = PostPointForm(instance=p)
    if request.method == 'POST':
        edit_form = PostPointForm(request.POST, instance=p)
        if edit_form.is_valid():
            edit_form.save()
    return render(request,
                  'blog/account/post_point_edit.html',
                  {'form': edit_form,
                   'p': p,})

@login_required
def del_post_point(request, id):
    try:
        pp = PostPoint.objects.get(id=id)
        pp.delete()
        return redirect("blog:post_point_list", pp.post.id)
    except PostPoint.DoesNotExist:
        return redirect("blog:profile")

@login_required
def post_point_add(r, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostPointForm()

    if r.method == 'POST':
        form = PostPointForm(r.POST,
                             r.FILES)
        if form.is_valid():
            post_point = form.save(commit=False)
            post_point.post = post
            post_point.save()

    return render(r, 'blog/account/post_point_add.html', {'form': form, 'post': post})

@login_required
def post_point_list(r, post_id):
    post = get_object_or_404(Post, id=post_id)
    pp_list=PostPoint.objects.filter(post__id=post_id)
    return render(r, 'blog/account/post_point.html', {'post_points': pp_list, "post":post})

@login_required
def del_post(request, post_id):
    try:
        post = get_object_or_404(Post, id=post_id)
        post.delete()
        return redirect("blog:profile")
    except Post.DoesNotExist:
        return redirect("blog:profile")


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post_edit_form = PostForm(instance=post)
    if request.method == 'POST':
        post_edit_form = PostForm(request.POST,instance=post)
        if post_edit_form.is_valid():
            post_edit_form.save()
    return render(request,
                  'blog/account/post_edit.html',
                  {'form': post_edit_form,
                   'post': post})

@login_required
def add_post(request):
    user=request.user
    if request.method=='POST':
        form=PostForm(request.POST,request.FILES)
        if form.is_valid():
            post=form.save(commit=False)
            post.author=user
            print(post)
            post.save()
            for tag in form.cleaned_data["tag"]: post.tag.add(tag)
    else:
        form=PostForm()

    return render(request, 'blog/account/post_add.html',{'form':form})

@login_required
def profile(r):
    user=r.user
    posts_public=Post.public.filter(author=user)
    posts_draft=Post.objects.filter(author=user, status="draft")
    print(posts_public)
    return render(r, 'blog/account/profile.html', {"posts_pub":posts_public, "posts_draft": posts_draft})



# class PostList(ListView):
#     queryset = Post.public.all()
#     context_object_name = "list"
#     paginate_by = 3
#     template_name = "blog/post/list.html"
#
#     #extra_context = {"post": 11}

@login_required
def post_list(r, tag_slug=None):

    #posts=Post.objects.all()
    public_posts=Post.public.all()

    form=SearchForm()
    query=None
    if "query" in r.GET:
        form=SearchForm(r.GET)
        if form.is_valid():
            query=form.cleaned_data["query"]
            try:
                public_posts=Post.public.filter(title__contains=query)
            except:
                public_posts=[]
        else:
            public_posts = Post.public.all()



    tag=None
    if tag_slug:
        tag=get_object_or_404(Tag, slug=tag_slug)
        public_posts=public_posts.filter(tag__in=[tag])
    p=Paginator(public_posts, 3)
    page=r.GET.get("page")
    try:
        posts=p.page(page)
    except PageNotAnInteger:

        posts=p.page(1)
    except EmptyPage:

        posts=p.page(p.num_pages)

    return render(r, 'blog/post/list.html', {"list": posts, "tag": tag, "range": range(1, p.num_pages+1), "form": form})

def post_detail(r, year, month, day, post):

    p_ob=get_object_or_404(Post, slug=post, status="published", publish__month=month, publish__day=day, publish__year=year)
    points=PostPoint.objects.filter(post=p_ob)
    comments=p_ob.comments.filter(active=1)
    if len(points)<1:
        raise Http404()

    new_comment = None
    if r.method == 'POST':
        print(r.POST)
        comment_form = CommentForm(data=r.POST)
        if comment_form.is_valid():
            cd = comment_form.cleaned_data
            print(cd)
            new_comment = Comment(post=p_ob, name=cd['name'], emeil=cd['emeil'], text=cd['text'])
            new_comment.save()
    else:
        comment_form = CommentForm()

    print(p_ob.tag)
    pt_ids=p_ob.tag.values_list("id", flat=True)
    sposts=Post.objects.filter(tag__in=pt_ids, status="published").exclude(id=p_ob.id)
    sposts=sposts.annotate(same_tags=Count("tag")).order_by("-same_tags", "-publish")

    return render(r, 'blog/post/detail.html', {'post': p_ob,
                                                     'points': points,
                                                     'comments': comments,
                                                     'new_comment': new_comment,
                                                     'comment_form': comment_form,
                                                     'sposts': sposts,
                                                     })

def error404(request, exception):

    return render(request, 'blog/base.html')





