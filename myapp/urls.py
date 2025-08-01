# myapp/urls.py
from django.urls import path
from . import views
from .views import QuestionCreateView

app_name = 'myapp'

urlpatterns = [
    path('', views.QuestionListView.as_view(), name='question_list'),  # トップページ
    path('ask/', QuestionCreateView.as_view(), name='question_create'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
]
