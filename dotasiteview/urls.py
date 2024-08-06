
from django.urls import path, include

urlpatterns = [
    path('', include('dotasite.urls')),
    path('social_auth/', include('social_django.urls', namespace='social')),
]
