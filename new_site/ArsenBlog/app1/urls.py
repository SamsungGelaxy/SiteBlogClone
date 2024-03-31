


from django.urls import path, register_converter
from . import views as v
from django.contrib.auth import views
app_name="blog"



urlpatterns = [
    path('tag/<slug:tag_slug>/', v.post_list, name="tag"),

    path('', v.post_list, name="post_list"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', v.post_detail, name="post_detail"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('profile/', v.profile, name="profile"),
    path('add_post/', v.add_post, name="add_post"),
]
