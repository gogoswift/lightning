import json
import functools
import urllib.parse
import re

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import engines
from django.contrib.staticfiles import finders
from django.conf import settings
from rest_framework.utils import encoders

from bsm_config.settings import site_setting
from api_basebone.export.fields import get_app_field_schema
from api_basebone.export.menu import get_menu_data
from api_basebone.export.setting import get_settins
from api_basebone.restful.serializers import create_serializer_class

lightning_static_url = getattr(settings, 'LIGHTNING_STATIC_URL', 'lightning')
static_url = settings.STATIC_URL
public_path = getattr(settings, 'LIGHTNING_CDN_HOST', '').rstrip('/') + static_url + lightning_static_url

public_path_placeholder = '{{public_path}}'


def unquote_placeholder(text):
    return text.replace(urllib.parse.quote_plus(public_path_placeholder), public_path_placeholder)


index_template = open(finders.find(lightning_static_url + '/index.html')).read()
index_template = unquote_placeholder(index_template)
index_template = index_template.replace(public_path_placeholder + '/manifest.json', '/basebone/manifest.json')
index_template = engines['django'].from_string(index_template)

index_content = index_template.render({
    'public_path': public_path,
    'injection': json.dumps({
    }, cls=encoders.JSONEncoder),  # encoders.JSONEncoder 解决django lazy object不能json.dumps的问题
})
login_response = HttpResponse(index_content)

manifest = open(finders.find(lightning_static_url + '/manifest.json')).read()
manifest = unquote_placeholder(manifest)
manifest_template = engines['django'].from_string(manifest)


service_worker = open(finders.find(lightning_static_url + '/service-worker.js')).read()
[precache_manifest] = re.findall(r'precache-manifest\.\w+\.js', service_worker)
service_worker = unquote_placeholder(service_worker)
service_worker = service_worker.replace(public_path_placeholder+'/precache-manifest', '/basebone/precache-manifest')
service_worker_template = engines['django'].from_string(service_worker)
service_worker = service_worker_template.render({
    'public_path': public_path,
})
service_worker_response = HttpResponse(service_worker, content_type='application/javascript')


precache_manifest = open(finders.find(lightning_static_url + '/' + precache_manifest)).read()
precache_manifest = precache_manifest.replace(public_path_placeholder + '/index.html', '/basebone/index.html')
precache_manifest_template = engines['django'].from_string(precache_manifest)
precache_manifest = precache_manifest_template.render({
    'public_path': public_path,
})
precache_manifest_response = HttpResponse(precache_manifest, content_type='application/javascript')


def get_userinfo(user):
    model = get_user_model()
    serializer_class = create_serializer_class(model)
    serializer = serializer_class(user)
    return serializer.data


# def adapt_decorator_to_method(d):
#     return lambda method: functools.wraps(method)(lambda self, *args, **kwargs:  d(lambda *a, **k: method(self, *a, **k))(*args, **kwargs))


def adapt_high_order_decorator_to_method(b):
    return lambda *args, **kwargs: lambda method: functools.wraps(method)(lambda self, *method_arg, **method_kwargs: b(*args, **kwargs)(lambda *a, **k: method(self, *a, **k))(*method_arg, **method_kwargs))


login_required = adapt_high_order_decorator_to_method(login_required)


class LightningView:
    def __init__(self, lightning_context):
        self.lightning_context = lightning_context

    @property
    def export_service(self):
        return self.lightning_context.export

    @login_required(redirect_field_name='redirect', login_url='/user/login')
    def index_view(self, request):
        user = request.user
        content = index_template.render({
            'public_path': public_path,
            'injection': json.dumps({
                '$$schemas': get_app_field_schema(),
                '$$admins': self.export_service.get_app_admin_config(request),
                '$$menus': get_menu_data(user),
                '$$settings': get_settins(),
                '$$userinfo': get_userinfo(user),
                '$$permissions': user.get_all_permissions(),
            }, cls=encoders.JSONEncoder),  # encoders.JSONEncoder 解决django lazy object不能json.dumps的问题
        })
        return HttpResponse(content)

    @staticmethod
    def login_page(request):
        return login_response

    @staticmethod
    def image_url(raw, size, provider):
        if provider == 'oss':
            return raw + '?x-oss-process=image/resize,m_pad,h_{0},w_{0},limit_0'.format(size)
        return raw

    @classmethod
    def manifest(cls, request):
        content = manifest_template.render({
            'public_path': public_path,
        })
        content = json.loads(content)
        title = site_setting['TITLE']
        if title:
            content['name'] = title
            content['short_name'] = title
        short_name = site_setting['SHORT_NAME']
        if short_name:
            content['short_name'] = short_name
        logo = site_setting['LOGO']
        if logo and '#' in logo:
            url, provider = logo.rsplit('#', 1)
            content['icons'] = [{
                'sizes': '{0}x{0}'.format(s),
                'src': cls.image_url(url, s, provider),
            } for s in [128, 192, 512]]
        content = json.dumps(content)
        return HttpResponse(content, content_type='application/json')

    @staticmethod
    def service_worker(request):
        return service_worker_response

    @staticmethod
    def precache_manifest(request):
        return precache_manifest_response
