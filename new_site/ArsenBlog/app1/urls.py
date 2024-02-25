


from django.urls import path, register_converter
from . import views as v

app_name="blog"



urlpatterns = [
    path('tag/<slug:tag_slug>/', v.post_list, name="tag"),

    path('', v.post_list, name="post_list"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', v.post_detail, name="post_detail"),
    path('login/', v.user_login, name="login"),
]
