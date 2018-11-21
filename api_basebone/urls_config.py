"""
输出配置的路由
"""

from django.urls import path, include

from .drf.routers import BaseBoneSimpleRouter as SimpleRouter
from api_basebone.restful.manage.config_views import ConfigViewSet

router = SimpleRouter(custom_base_name='schema-config')
router.register('', ConfigViewSet)

urlpatterns = router.urls
