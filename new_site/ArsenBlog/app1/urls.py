


from django.urls import path, register_converter
from . import views as v
from django.contrib.auth import views as authviews
app_name="blog"



urlpatterns = [
    path('tag/<slug:tag_slug>/', v.post_list, name="tag"),

    path('', v.post_list, name="post_list"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', v.post_detail, name="post_detail"),
    path('login/', authviews.LoginView.as_view(), name="login"),
    path('loginout/', authviews.LogoutView.as_view(), name="logout"),
    path('profile/', v.profile, name="profile"),
]
