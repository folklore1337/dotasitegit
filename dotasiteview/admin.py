from django.contrib import admin

from dotasiteview.models import MenuItem, SkinsItem, WeatherItem, Favorite

admin.site.register(MenuItem)
admin.site.register(SkinsItem)
admin.site.register(Favorite)
admin.site.register(WeatherItem)

