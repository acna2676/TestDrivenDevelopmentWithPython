from django.urls import include, re_path

from accounts import urls as accounts_urls
from lists import urls as list_urls
from lists import views as list_views

urlpatterns = [
    re_path(r'^$', list_views.home_page, name='home'),
    re_path(r'^lists/', include(list_urls)),
    re_path(r'^accounts/', include(accounts_urls)),
]
