import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--bearer_token", action="store", default="testtoken",
        help="Define bearer token: https://gorest.co.in/consumer/login"
    )


@pytest.fixture
def bearer_token(request):
    return request.config.getoption("--bearer_token")


