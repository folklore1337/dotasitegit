from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include


from dotasiteview import views


urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.index, name='index'),
    path('login-error/', views.login_error, name='login_error'),
    path('verify_email/', views.verify_email, name='verify_email'),
    path('accounts/', include('allauth.urls')),
    path('auth/', include('social_django.urls', namespace='social')),
    path('signup/', views.SignUp, name='signup'),
    path('login/', views.LoginPage, name='login'),
    path('heroes', views.heroes, name='heroes'),
    path('logout/', views.logout_view, name='logout'),
    path('skins', views.skins, name='skins'),
    path('steam-profile/', views.steam_profile, name='steam_profile'),
    path('dotabuff-profile/', views.dotabuff_profile, name='dotabuff_profile'),
    path('add_to_favorites/<str:item_type>/<int:item_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/', views.favorites_list, name='favorites'),
    path('remove_from_favorites/skins/<int:item_id>/', views.remove_from_favorites, name='remove_from_favorites'),
] 

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)