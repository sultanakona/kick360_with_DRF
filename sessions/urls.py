from django.urls import path
from .views import SessionCompleteView, SessionHistoryView, SessionShareToggleView

urlpatterns = [
    path('complete/', SessionCompleteView.as_view(), name='session-complete'),
    path('history/', SessionHistoryView.as_view(), name='session-history'),
    path('<int:pk>/share/', SessionShareToggleView.as_view(), name='session-share-toggle'),
]
