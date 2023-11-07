"""
URL configuration for salers project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from goods.views import *

urlpatterns = [
    # Default:
    path('admin/', admin.site.urls),
    path('', ProductHome.as_view(), name='home'),
    path('about/', about, name='about'),
    # Community Forms:
    path('sell/', Sell.as_view(), name='sell'),
    path('feedback/', Feedback.as_view(), name='feedback'),
    # Registration Forms:
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    # Showing:
    path('Product/<slug:post_slug>/', ShowPost.as_view(), name='post'),
    path('category/<slug:cat_slug>/', ProductCategory.as_view(), name='category'),
    # path('profile/<slug:username>', show_profile, name='profile'),
    path('profile/<slug:username>/', ShowProfile.as_view(), name='profile'),
    # Captcha
    path('captcha/', include('captcha.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = pageNotFound
