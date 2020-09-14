# Copyright (C) 2010-2012 Yaco Sistemas (http://www.yaco.es)
# Copyright (C) 2009 Lorenzo Gil Sanchez <lorenzo.gil.sanchez@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#            http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import copy
from importlib import import_module

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import saml2

from .utils import get_custom_setting

from deming.models import SamlConfig


def get_config_loader(path, request=None):
    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]
    try:
        mod = import_module(module)
    except ImportError as e:
        raise ImproperlyConfigured(
            'Error importing SAML config loader %s: "%s"' % (path, e))
    except ValueError as e:
        raise ImproperlyConfigured(
            'Error importing SAML config loader. Is SAML_CONFIG_LOADER '
            'a correctly string with a callable path?'
            )
    try:
        config_loader = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured(
            'Module "%s" does not define a "%s" config loader' %
            (module, attr)
            )

    if not hasattr(config_loader, '__call__'):
        raise ImproperlyConfigured(
            "SAML config loader must be a callable object.")

    return config_loader


def config_map(data):
    
    config = {
        # full path to the xmlsec1 binary programm
        'xmlsec_binary': '/usr/bin/xmlsec1',

        # your entity id, usually your subdomain plus the url to the metadata view
        'entityid': str(data.idp_entity),

        # directory with attribute mapping
        "attribute_map_dir": str(data.attributes_dir),

        # this block states what services we provide
        'service': {
            # we are just a lonely SP
            'sp': {
                # 'name': 'Federated Django sample SP',
                'name_id_format': getattr(saml2.saml, str(data.name_id_format),
                                          saml2.saml.NAMEID_FORMAT_UNSPECIFIED),

                # For Okta add signed logout requets. Enable this:
                # "logout_requests_signed": True,

                'endpoints': {
                    # url and binding to the assertion consumer service view
                    # do not change the binding or service name
                    'assertion_consumer_service': [
                        (str(data.acs_uri),
                        saml2.BINDING_HTTP_POST),
                    ],
                    # url and binding to the single logout service view
                    # do not change the binding or service name
                    'single_logout_service': [
                        (str(data.single_logout_service_uri_redirect),
                        saml2.BINDING_HTTP_REDIRECT),
                        (str(data.single_logout_service_uri_post),
                        saml2.BINDING_HTTP_POST),
                    ],
                },
            },
        },

        # where the remote metadata is stored, local, remote or mdq server.
        # One metadatastore or many ...
        'metadata': {
            'local': [str(data.metadata_file)],
        },

        'debug': 1,

        # Signing
        'key_file': str(data.sp_key_file),  # private part
        'cert_file': str(data.sp_certificate_file),  # public part

        # Encryption
        'encryption_keypairs': [{
            'key_file': str(data.sp_key_file),  # private part
            'cert_file': str(data.sp_certificate_file),  # public part
        }]
    }
    
    return config


def config_settings_loader(request=None):
    """Utility function to load the pysaml2 configuration.

    This is also the default config loader.
    """
    conf = saml2.config.SPConfig()
    saml_config_list = list(SamlConfig.objects.all())

    # conf.load(copy.deepcopy(settings.SAML_CONFIG))
    saml_config = config_map(saml_config_list[0].values)
    conf.load(saml_config)
    return conf


def get_config(config_loader_path=None, request=None):
    config_loader_path = config_loader_path or get_custom_setting(
        'SAML_CONFIG_LOADER', 'djangosaml2.conf.config_settings_loader')

    config_loader = get_config_loader(config_loader_path)
    return config_loader(request)
