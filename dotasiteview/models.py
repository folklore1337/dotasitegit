from django.db import models
from django.contrib.auth.models import User

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

# Герои
class MenuItem(models.Model):
    title = models.CharField(max_length=50, verbose_name='Имя героя')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='images', verbose_name='Изображение героя')
    icon = models.ImageField(upload_to='images', default='default_icon.png', verbose_name='Иконка героя')
    link = models.URLField(max_length=200, blank=True, null=True)
    link_dotabuff = models.URLField(max_length=200, blank=True, null=True)

    TYPE = [
        ('STR', 'Сила'),
        ('AGI', 'Ловкость'),
        ('INT', 'Интеллект'),
        ('UNI', 'Универсальный')
    ]

    type = models.CharField(choices=TYPE, max_length=3, default='STR', verbose_name='Атрибут')

    def __str__(self):
        return self.title
    
# Предметы
class SkinsItem(models.Model):
    title = models.CharField(max_length=50, unique=True, verbose_name='Название скина')
    image = models.ImageField(upload_to='images', verbose_name='Изображение скина')
    link = models.URLField(max_length=200, blank=True, null=True, verbose_name='Ссылка на стим')
    link_1 = models.URLField(max_length=200, blank=True, null=True, verbose_name='Ссылка на лис-скинс')
    id = models.AutoField(primary_key=True)
    hero = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True, blank=True,)
    icon = models.ImageField(upload_to='images', verbose_name='Иконка героя для панели сортировки')

    TYPE = [
        ('IMO', 'Immortal'),
        ('ARC', 'Arcana')
    ]

    type = models.CharField(choices=TYPE, max_length=3, default='IMO', verbose_name='Редкость')

    def __str__(self):
        return self.title
    
# Погода
class WeatherItem(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название погоды')
    image = models.ImageField(upload_to='images', verbose_name='Изображение погоды')
    link = models.URLField(max_length=200, blank=True, null=True, verbose_name='Ссылка на стим')
    link_1 = models.URLField(max_length=200, blank=True, null=True, verbose_name='Ссылка на лис-скинс')
    
    def __str__(self):
        return self.title
    

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    skins_item = models.ForeignKey(SkinsItem, null=True, blank=True, on_delete=models.CASCADE)
    weather_item = models.ForeignKey(WeatherItem, null=True, blank=True, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('user', 'skins_item', 'weather_item')
    
    def __str__(self):
        return f"{self.user.username}'s favorite"
    

