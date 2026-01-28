from django.urls import path
from . import views

urlpatterns = [
    path('', views.api_root, name='api-root'),
    path('register/', views.register, name='register'),
    path('upload/', views.upload_csv, name='upload-csv'),
    path('summary/<int:dataset_id>/', views.summary, name='summary'),
    path('history/', views.history, name='history'),
]
