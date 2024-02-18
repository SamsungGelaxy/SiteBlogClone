from django.http import HttpResponse, Http404, HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.template.loader import render_to_string
from django.db.models import Count
from .forms import CommentForm

# Create your views here.
from .models import Post, PostPoint, Comment
from django.views.generic import ListView

from taggit.models import Tag


class PostList(ListView):
    queryset = Post.public.all()
    context_object_name = "list"
    paginate_by = 3
    template_name = "blog/post/list.html"

    #extra_context = {"post": 11}


def post_list(r, tag_slug=None):

    #posts=Post.objects.all()
    public_posts=Post.public.all()
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

    return render(r, 'blog/post/list.html', {"list": posts, "tag": tag})

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





