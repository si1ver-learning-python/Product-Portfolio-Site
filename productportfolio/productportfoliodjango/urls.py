from django.contrib import admin
from django.urls import path
import products.views
import contact.views
from .settings import MEDIA_URL, MEDIA_ROOT
from django.conf.urls.static import static


urlpatterns = [
    path('admin/products/product/add/', products.views.admin_add_product),
    path('admin/', admin.site.urls),
    path('', products.views.home),
    path('contact', contact.views.contact),
    path('product/<str:product>', products.views.product)
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
