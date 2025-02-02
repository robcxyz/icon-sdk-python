# -*- coding: utf-8 -*-
# Copyright 2018 ICON Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import requests_mock

from unittest.mock import patch
from tests.example_config import BASE_DOMAIN_URL_V3_FOR_TEST
from unittest import main

from iconsdk.utils.validation import is_block
from tests.api_full_response.example_response import result_error_v3, result_success_v3
from tests.api_full_response.test_full_response_base import TestFullResponseBase


@patch('iconsdk.providers.http_provider.HTTPProvider._make_id', return_value=1234)
class TestFullResponseGetBlockByHash(TestFullResponseBase):

    def test_get_block_by_hash_full_response(self, _make_id):
        # used valid hash and got and valid block
        with requests_mock.Mocker() as m:
            expected_request = {
                'jsonrpc': '2.0',
                'method': 'icx_getBlockByHash',
                'id': 1234,
                'params': {
                    'hash': self.block_hash
                }
            }

            response_json = {
                'jsonrpc': '2.0',
                'result': self.block,
                'id': 1234
            }

            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3/", json=response_json)
            result_dict = self.icon_service.get_block(self.block_hash, full_response=True)
            actual_request = json.loads(m._adapter.last_request.text)
            result_keys = result_dict.keys()
            result_content = result_dict['result']

            self.assertEqual(expected_request, actual_request)
            self.assertEqual(result_success_v3.keys(), result_keys)
            self.assertTrue(is_block(result_content))

    def test_get_block_by_wrong_hash(self, _make_id):
        # used invalid hash and got and invalid block

        invalid_block_hash = "0x033f8d96045eb8301fd17cf078c28ae58a3ba329f6ada5cf128ee56dc2af26f7"
        with requests_mock.Mocker() as m:
            response_json = {
                'jsonrpc': '2.0',
                'error': {
                    "code": -32602,
                    "message": "fail wrong block hash"
                },
                'id': 1234
            }

            m.post(f"{BASE_DOMAIN_URL_V3_FOR_TEST}/api/v3/", json=response_json, status_code=400)
            result_dict = self.icon_service.get_block(invalid_block_hash, full_response=True)
            self.assertEqual(result_dict.keys(), result_error_v3.keys())


if __name__ == "__main__":
    main()