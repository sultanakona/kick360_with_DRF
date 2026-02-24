from django.urls import path
from .views import ProfileSettingsView

urlpatterns = [
    path('profile/', ProfileSettingsView.as_view(), name='settings-profile'),
]
