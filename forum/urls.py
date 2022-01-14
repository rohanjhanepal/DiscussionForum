from django.urls import path
from . import views


app_name = 'forum'
urlpatterns = [
    path('', views.index, name='home'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),    #post detail view
    path('/login' , views.login, name='login'),
    path('/logout' , views.logout_view, name='logout'),
    path('/search' , views.search, name='search'),
]
