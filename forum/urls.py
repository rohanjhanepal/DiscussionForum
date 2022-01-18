from django.urls import path
from . import views


app_name = 'forum'
urlpatterns = [
    path('', views.index, name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),    #post detail view for viewing post using slug
    path('search' , views.search, name='search'),
    path('login' , views.login_view, name='login'),
    path('logout' , views.logout_view, name='logout'),
    path('signup' , views.signup_view, name='signup'),
]
