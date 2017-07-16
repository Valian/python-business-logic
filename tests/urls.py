# -*- coding: utf-8
from __future__ import unicode_literals, absolute_import

from django.conf.urls import url, include

from django_application_logic.urls import urlpatterns as django_application_logic_urls

urlpatterns = [
    url(r'^', include(django_application_logic_urls, namespace='django_application_logic')),
]
