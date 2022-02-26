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
    path(r'^upvote/<int:id>/$' , views.upvote , name='upvote'),
    path(r'^solved/<slug:slug>/$' , views.solved , name='solved'),
    path(r'^category/<int:id>/$' , views.category_view , name='category'),
    path(r'^subcategory/<int:id>/$' , views.sub_category_view , name='subcategory'),
    path(r'^answer/<slug:slug>/$' , views.answer_view , name='answer'),
    path('post_question' , views.post_question , name='post_question'),
    path('notifications' , views.notification_view , name='notifications'),
    path('recommended_to_answer', views.recommend_questions , name='recommended_to_answer'),
]
