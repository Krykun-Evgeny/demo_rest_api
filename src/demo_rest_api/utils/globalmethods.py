import allure
import requests
import logging
import os
import json
from deepdiff import DeepDiff
import jsonschema
from jsonschema import validate

LOG_LEVEL = logging.INFO
common_formatter = logging.Formatter('%(asctime)s [%(levelname)-7s][ln-%(lineno)-3d]: %(message)s',
                                     datefmt='%Y-%m-%d %I:%M:%S')

root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def setup_logger(log_file, level=logging.INFO, name='', formatter=common_formatter):
    handler = logging.FileHandler(log_file, mode='w')
    handler.setFormatter(formatter)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


api_formatter = logging.Formatter('%(asctime)s: %(message)s', datefmt='%Y-%m-%d %I:%M:%S')
api_outputs_filename = '{}\\logs\\api_outputs.log'.format(root_path)
log_api = setup_logger(api_outputs_filename, LOG_LEVEL, 'log_api', formatter=api_formatter)


def pretty_print_request(request):
    log_api.info('{}\n{}\n\n{}\n\n{}\n'.format(
        '-----------Request----------->',
        '{} {}'.format(request.method, request.url),
        '\n'.join('{}: {}'.format(k, v) for k, v in request.headers.items()),
        request.body)
    )


def pretty_print_response(response):
    log_api.info('{}\n{}\n\n{}\n\n{}\n'.format(
        '<-----------Response-----------',
        'Status code: {}'.format(str(response.status_code)),
        '\n'.join('{}: {}'.format(k, v) for k, v in response.headers.items()),
        response.text
    ))


def file_logging(response):
    pretty_print_request(response.request)
    pretty_print_response(response)


def send_put_request_json(url, headers, payload):
    with allure.step("Send PUT request by URL: {}".format(url)):
        response = requests.put(url, headers=headers, data=json.dumps(payload))
        file_logging(response)
        return response


def send_post_request_json(url, headers, payload):
    with allure.step("Send POST request by URL: {}".format(url)):
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        file_logging(response)
        return response


def send_get_request_json(url, headers):
    with allure.step("Send GET request by URL: {}".format(url)):
        response = requests.get(url, headers=headers)
        file_logging(response)
        return response


def send_delete_request_json(url, headers):
    with allure.step("Send DELETE request by URL: {}".format(url)):
        response = requests.delete(url, headers=headers)
        file_logging(response)
        return response


def get_json_body(response):
    try:
        response_body = response.json()
        return response_body
    except ValueError as err:
        assert False, "{}".format(err)


def validate_status_code(expected_status, actual_status):
    with allure.step("Validate status code"):
        assert expected_status == actual_status, "Expected status code: {}\nActual status code: {}". \
            format(expected_status, actual_status)


def validate_headers(expected_headers, actual_headers):
    with allure.step("Validate response headers"):
        for expected_key in expected_headers:
            assert expected_key in actual_headers, \
                "Expected response header is absent: {}\nActual headers: {}".format(expected_key, str(actual_headers))
            expected_value = expected_headers.get(expected_key)
            actual_value = actual_headers.get(expected_key)
            if expected_value:
                assert expected_value == actual_value, \
                    "Header key: {}\nExpected value: {}\nActual value: {}".format(expected_key, expected_value, actual_value)


def validate_json_bodies(expected_body, actual_body, exclude_paths):
    with allure.step("Validate response body"):
        differences = DeepDiff(expected_body, actual_body, exclude_paths=exclude_paths)
        assert not differences, "Differences\n{}\nExpected body:\n{}\nActual body:\n{}".\
            format(differences.pretty(), str(expected_body), str(actual_body))


def get_schema(path_json_schema):
    with open(path_json_schema, 'r') as file:
        schema = json.load(file)
    return schema


def validate_json_schema(path_json_schema, json_data):
    with allure.step("Validate response body by JSON schema"):
        execute_api_schema = get_schema(path_json_schema)

        try:
            validate(instance=json_data, schema=execute_api_schema)
        except jsonschema.exceptions.ValidationError as err:
            assert False, "Given JSON data is InValid\n{}".format(err)

        return True
