from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from comrade_core import views

_REACT_INDEX = settings.BASE_DIR.parent / 'client' / 'dist' / 'index.html'

urlpatterns = [
    path('admin/', admin.site.urls),

    # API routes (all prefixed with /api/ to match React's baseURL: '/api')
    path('api/', include('comrade_core.urls')),
    path('api/user/info/', views.get_user_info, name='get_user_info'),
    path('api/auth/google-config/', views.google_config, name='google_config'),
    path('api/accounts/google/login/callback/', views.google_oauth_callback, name='google_oauth_callback'),

    # Legacy Django template routes (dev / admin convenience)
    path('login/', views.login_page, name='login_page'),
    path('map/', views.map, name='map'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Serve React SPA for all non-API routes (production: React build exists)
if _REACT_INDEX.exists():
    urlpatterns += [
        re_path(r'^(?!api/|admin/|static/|media/).*$',
                TemplateView.as_view(template_name='index.html'),
                name='react_spa'),
    ]
