from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.core.mail import send_mail
from django.http import JsonResponse
from django.urls import reverse
from django.conf import settings
from .models import MenuItem, SkinsItem, WeatherItem, Favorite, EmailVerification
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
import random
import string
from django.contrib.auth.decorators import login_required

def generate_verification_code(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def index(request):
    return render(request, 'index.html')

def heroes(request):
    attribute_str = MenuItem.objects.filter(type__exact='STR').order_by('title')
    attribute_agi = MenuItem.objects.filter(type__exact='AGI').order_by('title')
    attribute_int = MenuItem.objects.filter(type__exact='INT').order_by('title')
    attribute_uni = MenuItem.objects.filter(type__exact='UNI').order_by('title')
    context = {
        'attribute_str' : attribute_str,
        'attribute_agi' : attribute_agi,
        'attribute_int' : attribute_int,
        'attribute_uni' : attribute_uni,
    }
    return render(request, 'heroes.html', context=context)

def skins(request):
    hero_id = request.GET.get('hero_id')
    page_imo = request.GET.get('page_imo', 1)
    page_arc = request.GET.get('page_arc', 1)
    heroes = MenuItem.objects.all().order_by('title')

    if hero_id:
        rare_imo = SkinsItem.objects.filter(type='IMO', hero_id=hero_id).order_by('title')
        rare_arc = SkinsItem.objects.filter(type='ARC', hero_id=hero_id).order_by('title')
    else:
        rare_imo = SkinsItem.objects.filter(type='IMO').order_by('title')
        rare_arc = SkinsItem.objects.filter(type='ARC').order_by('title')

    weather = WeatherItem.objects.order_by('title')

    if request.user.is_authenticated:
        favorite_skins_ids = Favorite.objects.filter(user=request.user, skins_item__isnull=False).values_list('skins_item_id', flat=True)
    else:
        favorite_skins_ids = []

    for skin in rare_imo:
        skin.is_favorite = skin.id in favorite_skins_ids

    for skin in rare_arc:
        skin.is_favorite = skin.id in favorite_skins_ids

    paginator_imo = Paginator(rare_imo, 8)
    paginator_arc = Paginator(rare_arc, 12)

    rare_imo_page = paginator_imo.get_page(page_imo)
    rare_arc_page = paginator_arc.get_page(page_arc)

    context = {
        'rare_imo': rare_imo_page,
        'rare_arc': rare_arc_page,
        'weather': weather,
        'heroes': heroes,
        'current_hero_id': hero_id,
        'selected_hero_id': int(hero_id) if hero_id else None,
    }

    return render(request, 'skins.html', context)


def steam_profile(request):
    steam_profile_url = "https://steamcommunity.com/id/timsimpson3/"
    return render(request, 'steam_profile.html', {'steam_profile_url': steam_profile_url})

def dotabuff_profile(request):
    dotabuff_profile_url = "https://ru.dotabuff.com/players/215335290"
    return render(request, 'dotabuff_profile.html', {'dotabuff_profile_url': dotabuff_profile_url})


@login_required
def add_to_favorites(request, item_type, item_id):
    if item_type == 'skins':
        item = get_object_or_404(SkinsItem, id=item_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, skins_item=item)
    elif item_type == 'weather':
        item = get_object_or_404(WeatherItem, id=item_id)
        favorite, created = Favorite.objects.get_or_create(user=request.user, weather_item=item)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid item type'}, status=400)

    if created:
        return JsonResponse({'status': 'added'})
    else:
        return JsonResponse({'status': 'exists'})

def favorites_list(request):
    skins = SkinsItem.objects.all()
    favorites = Favorite.objects.filter(user=request.user)
    favorite_skins_ids = favorites.filter(skins_item__isnull=False).values_list('skins_item_id', flat=True)

    for skin in skins:
        skin.is_favorite = skin.id in favorite_skins_ids


    context = {
        'favorites': favorites,
        'skins': skins
    }
    return render(request, 'favorites.html', context)


def remove_from_favorites(request, item_id):
    if request.method == 'POST':
        try:
            favorite = Favorite.objects.get(skins_item__id=item_id, user=request.user)
            favorite.delete()
            return JsonResponse({'status': 'removed'})
        except Favorite.DoesNotExist:
            return JsonResponse({'status': 'not_found'}, status=404)
    return JsonResponse({'status': 'invalid_request'}, status=400)

def SignUp(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        
        if pass1 != pass2:
            return HttpResponse("Пароль не совпадает с введенным выше.")
        else:
            user = User(username=username, email=email)
            user.set_password(pass1)
            user.is_active = False  # Deactivate account till it is confirmed
            user.save()
            
            verification_code = generate_verification_code()
            EmailVerification.objects.create(user=user, code=verification_code)
            
            send_mail(
                'Verify your email',
                f'Your verification code is {verification_code}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            
            return redirect('verify_email')
        
    return render(request, 'signup.html')



def LoginPage(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Имя пользователя или пароль неправильны.")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')

def login_error(request):
    return render(request, 'login_error.html')

def auth_complete(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        pass1=request.POST.get('pass')
        user=authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return HttpResponse("Имя пользователя или пароль неправильны.")
        


def verify_email(request):
    if request.method == "POST":
        username = request.POST.get('username')
        code = request.POST.get('code')
        
        try:
            user = User.objects.get(username=username)
            verification = EmailVerification.objects.get(user=user)
            
            if verification.code == code:
                user.is_active = True
                user.save()
                verification.is_verified = True
                verification.save()
                
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                
                return redirect('index')
        
        except (User.DoesNotExist, EmailVerification.DoesNotExist):
            return HttpResponse("Invalid username or verification code.")
    
    return render(request, 'verify_email.html')
