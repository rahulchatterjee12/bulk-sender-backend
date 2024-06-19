from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('whatsapp/',include('bulk_send.urls'))
]
