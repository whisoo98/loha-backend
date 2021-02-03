"""loha URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url

urlpatterns = [
    path('admin/', admin.site.urls),
    path('product/', include('product.urls')),
    path('collections/', include('category.urls')),
    path('user/', include('user.urls')),
    path('usergroup/', include('usergroup.urls')),
    path('cart/', include('cart.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('catalog/', include('catalog.urls')),
    path('payment/', include('payment.urls')),
    path('coupon/',include('coupon.urls')),
    path('influencer/', include('influencer.urls')),
    path('media/', include('media.urls')),
    path('images/', include('images.urls')),
    path('review/', include('review.urls')),
    path('order/', include('order.urls')),
    path('chat/',include('chat.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
