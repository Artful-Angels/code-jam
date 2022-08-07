from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_ALLOW_ALL = True


# Using redis server

# Channel layers config wirth redis
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            # Redis hosts config if the server running with Docker
            "hosts": [("redis_layer", 6379)],
            # Redis hosts config if the server running in localhost
            # "hosts": [("127.0.0.1",6379)]
        },
    },
}
# Cache config with redis

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis_cache/1",
        "TIMEOUT": 3600,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "MAX_ENTRIES": 2000,
        },
    }
}


# Using local memory and ram

# 2 -Channel layers config running on memory (without redis server)
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels.layers.InMemoryChannelLayer"
#     }
# }


# Cache config in local memory (without need redis)

# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
#         "LOCATION": "unique-snowflake",
#         "TIMEOUT": 3600,
#         "OPTIONS": {
#             "MAX_ENTRIES": 2000,
#         },
#     }
# }
