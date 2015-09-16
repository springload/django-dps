from django.conf.urls import url

from . import views

urlpatterns = (
    url(r'^result/(?P<token>.*)$', views.transaction_result, {},
        'dps_transaction_result'),
)
