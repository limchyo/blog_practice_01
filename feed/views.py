from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Article, Comment, HashTag

# Create your views here.
def index(request):
    category = request.GET.get("category")
    hashtag = request.GET.get("hashtag")

    if not category and not hashtag:
        article_list = Article.objects.all()
    elif category:
        article_list = Article.objects.filter(category=category)
    else:
        article_list = Article.objects.filter(hashtag__name=hashtag)

    hashtag_list = HashTag.objects.all()
    category_list = set([
        (article.category, article.get_category_display())
        for article in article_list
    ])

    ctx = {
        "article_list" : article_list,
        "category_list" : category_list,
        "hashtag_list" : hashtag_list,
    }
    return render(request, "index.html", ctx)

def detail(request, article_id):
    article = Article.objects.get(id=article_id)
    # comment_list = Article.article_comments.all()

    ctx = {
        "article" : article,
        # "comment_list" : comment_list,
    }

    if request.method == "GET":
        pass
    elif request.method == "POST":
        username = request.POST.get("username")
        content = request.POST.get("content")
        Comment.objects.create(
            article=article,
            username=username,
            content=content,
            approved_comment=False
        )
        return HttpResponseRedirect("/{}/".format(article_id))

    return render(request, "detail.html", ctx)
