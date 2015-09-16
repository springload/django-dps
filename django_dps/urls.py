from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^success/(?P<token>.*)$', views.transaction_success, {},
        'django_dps_transaction_success'),
    url(r'^failure/(?P<token>.*)$', views.transaction_failure, {},
        'django_dps_transaction_failure'),
)
