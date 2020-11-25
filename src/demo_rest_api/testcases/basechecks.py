import utils.globalmethods as gm
from values import dics, strings, integers
import allure


def validate_status_code_by_response_body(expected_status, response_body):
    with allure.step("Validate status code from response body"):
        assert response_body['code'] == expected_status, "Response body: {}".format(str(response_body))


class BaseChecks:
    def validate_user_resource(self, list_expected_status_code, expected_json_body):
        with allure.step("Check resource: 'User'"):
            response_body = gm.get_json_body(self.response)
            gm.validate_status_code(list_expected_status_code[0], self.response.status_code)
            validate_status_code_by_response_body(list_expected_status_code[1], response_body)
            gm.validate_headers(dics.verified_header, self.response.headers)
            gm.validate_json_bodies(expected_json_body, response_body["data"],
                                    exclude_paths=["root['id']", "root['updated_at']", "root['created_at']"])
            gm.validate_json_schema("{}/user.json".format(strings.relative_path_json_schemas), response_body)

    def validate_created_user(self):
        self.validate_user_resource(list_expected_status_code=[integers.status_OK, integers.status_Created],
                                    expected_json_body=dics.post_user)

    def validate_updated_user(self):
        self.validate_user_resource(list_expected_status_code=[integers.status_OK, integers.status_OK],
                                    expected_json_body=dics.put_user)

    def validate_deleted_user(self):
        with allure.step("Check User deletion"):
            response_body = self.get_response_body_with_status_check()
            validate_status_code_by_response_body(integers.status_No_Content, response_body)
            gm.validate_headers(dics.verified_header, self.response.headers)
            gm.validate_json_bodies(dics.delete_user, response_body, exclude_paths=[])
            gm.validate_json_schema("{}/delete_user.json".format(strings.relative_path_json_schemas), response_body)

    def validate_authentication_failed(self):
        with allure.step("Check authentication failed by invalid token"):
            response_body = self.get_response_body_with_status_check()
            validate_status_code_by_response_body(integers.status_Unauthorized, response_body)
            gm.validate_headers(dics.verified_header, self.response.headers)
            gm.validate_json_bodies(dics.unauthorized_response_body, response_body, exclude_paths=[])
            gm.validate_json_schema("{}/unauthorized_response_body.json".format(strings.relative_path_json_schemas),
                                    response_body)

    def validate_unprocessable_entity_for_empty_obj(self):
        with allure.step("Check unprocessable entity by sending empty object"):
            response_body = self.get_response_body_with_status_check()
            validate_status_code_by_response_body(integers.status_Unprocessable_Entity, response_body)
            gm.validate_headers(dics.verified_header, self.response.headers)
            gm.validate_json_bodies(dics.unprocessable_entity_empty_obj, response_body, exclude_paths=[])
            gm.validate_json_schema("{}/unprocessable_entity_empty_obj.json".format(strings.relative_path_json_schemas),
                                    response_body)

    def update_url_by_id(self):
        with allure.step("Update URL of the 'User' resource"):
            response_body = gm.get_json_body(self.response)
            temp_id = response_body['data']['id']
            strings.url_get_resource_by_id = "{}/{}".format(self.response.url, temp_id)

    def get_response_body_with_status_check(self):
        response_body = gm.get_json_body(self.response)
        gm.validate_status_code(integers.status_OK, self.response.status_code)
        return response_body
