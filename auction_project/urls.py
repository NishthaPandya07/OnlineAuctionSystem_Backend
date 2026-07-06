from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from listings import views as listing_views

urlpatterns = [
    path('', listing_views.listing_list, name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('listings/', include('listings.urls')),
    path('bids/', include('bids.urls')),
    path('timers/', include('timers.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
