from django.urls import path

from .views import base_views, notice_views, answer_views

app_name = 'bbs'

urlpatterns = [
    # base_views.py
    path('', base_views.index, name='index'),
    path('<int:notice_id>/', base_views.detail, name='detail'),
    # notice_views.py
    path('notice/create/', notice_views.notice_create, name='notice_create'),
    path('notice/modify/<int:notice_id>/', notice_views.notice_modify, name='notice_modify'),
    path('notice/delete/<int:notice_id>/', notice_views.notice_delete, name='notice_delete'),
    # answer_views.py
    path('answer/create/<int:notice_id>/', answer_views.answer_create, name='answer_create'),
    path('answer/modify/<int:answer_id>/', answer_views.answer_modify, name='answer_modify'),
    path('answer/delete/<int:answer_id>/', answer_views.answer_delete, name='answer_delete'),
]