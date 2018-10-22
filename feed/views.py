from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Article, Comment, HashTag

# Create your views here.
# 함수 if while 클래스 등을 구현하고 내부를 구현하지 않으면 syntax 에러를 일으킨다.
# 따라서 이를 사전에 방지하고자 pass를 사용한다.
def index(request):
    # get은 원하는 정보를 서버에서 가져와달라고 요청하는 메소드이다. 가공되지 않은 형태로 보낸다.
    # post는 서버에 데이터를 저장하거나 변경, 로그인 일치 여부 등 서버에 특정 작업을 추가 요구.
    # "category"라는 이름으로 딕셔너리 키를 설정한다. 키를 호출하면 값을 변수에 지정
    # 키와 값을 url에 입력하면 그에 맞는 페이지를 서버에서 가져와 출력한다.
    category = request.GET.get("category")
    # 주소창에서 ?category=dv, ?category=ps 형태로 GET 처리
    hashtag = request.GET.get("hashtag")

    hashtag_list = HashTag.objects.all()
    # 해시태그는 어떤 상황에서든 전부 노출되도록 설정
    if not category and not hashtag:
        article_list = Article.objects.all()
    # 카테고리와 해시태그가 없다면 게시글 전부 노출
    elif category:
        article_list = Article.objects.filter(category=category)
    # 카테고리가 있다면 해당 카테고리 게시글 노출
    else:
        article_list = Article.objects.filter(hashtag__name=hashtag)
    # 해시태그가 있다면 해당 해시태그를 가진 게시글 노출
    # hashtag 필드는 HashTag 클래스의 name 필드와 연결되어 있으므로
    # 해시태그를 검색하기 위해서는 언더바 2개를 이용해 name 필드를 연결해야한다.

    # category_list = set([])
    # for article in article_list:
        # category_list.add(article.get_category_display())
    # category_list = set([
    #     article.get_category_display()
    #     for article in article_list
    # ])
    category_list = set([
        (article.category, article.get_category_display())
        for article in article_list
    ])

    ctx = {
        "article_list" : article_list,
        "hashtag_list" : hashtag_list,
        "category_list" : category_list,
    }
    return render(request, "index.html", ctx)

def detail(request, article_id):
    article = Article.objects.get(id=article_id)
    # article_list = Article.objects.all()
    # comment_list = Comment.objects.filter(article__id=article_id)
    # comment_list = article.article_comments.all()
    hashtag_list = HashTag.objects.all()
    # category_list = set([
    #     (article.category, article.get_category_display())
    #     for article in article_list
    # ])
    ctx = {
        "article" : article,
        # "comment_list" : comment_list,
        "hashtag_list" : hashtag_list,
        # "category_list" : category_list,
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
        )

        return HttpResponseRedirect("/{}/".format(article_id))

    return render(request, "detail.html", ctx)
