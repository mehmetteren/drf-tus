# -*- coding: utf-8 -*-
from django.urls import path, include
from rest_framework_tus.views import UploadViewSet

from .routers import TusAPIRouter
from .views import TestView

router = TusAPIRouter()
router.register(r'files', UploadViewSet, basename='upload')

urlpatterns = [
    path(r'', include((router.urls, 'rest_framework_tus'), namespace='api')),
    path('test', TestView.as_view(), name='test')
]
app_name = 'rest_framework_tus'
