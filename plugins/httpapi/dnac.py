# (c) 2019 Red Hat Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
---
author: Ansible Networking Team
httpapi: dnac
short_description: Connect to Cisco DNA Center
description:
  - The dnac plugin provides an implementation for interfacing with
    Cisco DNA Center server using the REST API
version_added: "2.8"
options:
"""
import json

from urllib2 import HTTPError

from ansible.module_utils._text import to_text
from ansible.module_utils.connection import ConnectionError
from ansible.plugins.httpapi import HttpApiBase


class HttpApi(HttpApiBase):

    def login(self, username, password):
        login_url = "/dna/system/api/v1/auth/token"

        response, response_data = self.connection.send(login_url, None,
                method='POST', force_basic_auth=True)

        try:
            response_data = json.loads(to_text(response_data.getvalue()))
        except ValueError:
            raise ConnectionError('Response was not valid JSON, got {0}'.format(
                to_text(response_data.getvalue())
            ))

    def logout(self):
        if self._auth:
            self.connection._auth = None

    def update_auth(self, response, response_data):
        response_data = json.loads(to_text(response_data.getvalue()))
        if 'Token' in response_data:
            self.connection._auth = {'X-Auth-Token': response_data['Token']}

    def send_request(self, url, **kwargs):
        data = kwargs.pop('data', None)
        if data and not isinstance(data, str):
            data = json.dumps(data)

        headers = kwargs.get('headers') or {}
        if 'Content-type' not in headers:
            headers['Content-type'] = 'application/json'
            kwargs['headers'] = headers

        response, response_data = self.connection.send(url, data, **kwargs)

        if isinstance(response, HTTPError):
            raise response

        try:
            response_data = to_text(response_data.getvalue())
        except ValueError:
            raise ConnectionError('Response was not valid JSON, got {0}'.format(
                to_text(response_data.getvalue())
            ))

        return response_data

    def get(self, url, **kwargs):
        kwargs['method'] = 'GET'
        return self.send_request(url, **kwargs)

    def post(self, url, **kwargs):
        kwargs['method'] = 'POST'
        return self.send_request(url, **kwargs)

    def put(self, url, **kwargs):
        kwargs['method'] = 'PUT'
        return self.send_request(url, **kwargs)

    def patch(self, url, **kwargs):
        kwargs['method'] = 'PATCH'
        return self.send_request(url, **kwargs)

    def delete(self, url, **kwargs):
        kwargs['method'] = 'DELETE'
        return self.send_request(url, **kwargs)
