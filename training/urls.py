from django.urls import path
from .views import TrainingVideoListView, TrainingCompleteView

urlpatterns = [
    path('', TrainingVideoListView.as_view(), name='training-list'),
    path('<int:pk>/complete/', TrainingCompleteView.as_view(), name='training-complete'),
]
