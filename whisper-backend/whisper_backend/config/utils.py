from django.core.cache import cache

from .models import Setting


def get_setting(key, default=None):
    # Проверяем кэш
    cached_value = cache.get(key)
    if cached_value:
        return cached_value

    # Если в кэше нет, запрашиваем из базы данных
    try:
        setting = Setting.objects.get(key=key)
        cache.set(key, setting.value, timeout=3600)  # Кэшируем на 1 час
        return setting.value
    except Setting.DoesNotExist:
        return default
