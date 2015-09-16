from django.conf.urls import url, include

urlpatterns = (
    url('^dps/', include('django_dps.urls')),
)
