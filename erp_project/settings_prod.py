from .settings import *

# Override production settings
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')
ALLOWED_HOSTS = ['your-railway-app-name.up.railway.app']

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('postgresql://postgres:hHqoKXOxBuqJhwDQBOWIwxmvtIcdCYdO@postgres.railway.internal:5432/railway'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNFF = True

# Time zone
TIME_ZONE = 'Asia/Jakarta'