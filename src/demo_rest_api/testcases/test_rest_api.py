import json

import allure
import pytest
from datetime import datetime

from testcases.basechecks import BaseChecks
from values import strings
import utils.globalmethods as gm
from values import dics


@pytest.fixture(scope="class")
def init(request):
    bearer_token = request.config.getoption("--bearer_token")
    with allure.step("Setup"):
        dics.headers['Authorization'] = 'Bearer {}'.format(bearer_token)
        # request.cls.relative_path_json_schemas = "../json_schemas/"
    yield
    with allure.step("Teardown"):
        pass


@pytest.mark.usefixtures("init")
class TestRestAPI(BaseChecks):
    def test_create_user(self):
        self.response = gm.send_post_request_json(url=strings.user_post_url, headers=dics.headers,
                                                  payload=dics.post_user)
        self.validate_created_user()
        self.update_url_by_id()

    def test_update_user(self):
        self.response = gm.send_put_request_json(url=strings.url_get_resource_by_id, headers=dics.headers,
                                                 payload=dics.put_user)
        self.validate_updated_user()

    def test_get_updated_user(self):
        self.response = gm.send_get_request_json(url=strings.url_get_resource_by_id, headers=dics.headers)
        self.validate_updated_user()

    def test_delete_updated_user(self):
        self.response = gm.send_delete_request_json(url=strings.url_get_resource_by_id, headers=dics.headers)
        self.validate_deleted_user()

    def test_authentication_failed_by_create_user(self, bearer_token):
        dics.headers['Authorization'] = 'Bearer {}'.format('invalid_token')
        self.response = gm.send_post_request_json(url=strings.user_post_url, headers=dics.headers,
                                                  payload=dics.post_user)
        self.validate_authentication_failed()
        dics.headers['Authorization'] = 'Bearer {}'.format(bearer_token)

    def test_unprocessable_entity_by_create_user(self):
        self.response = gm.send_post_request_json(url=strings.user_post_url, headers=dics.headers,
                                                  payload=dics.empty_dict)
        self.validate_unprocessable_entity_for_empty_obj()
