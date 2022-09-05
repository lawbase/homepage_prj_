from django.urls import path

from . import views

app_name = 'bbs'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:notice_id>/', views.detail, name='detail'),
    path('notice/create/', views.notice_create, name='notice_create'),
    path('answer/create/<int:notice_id>/', views.answer_create, name='answer_create'),
]