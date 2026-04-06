import os
import pytest

pytest.register_assert_rewrite("tests.utils")

def pytest_runtest_setup(item):
    os.environ["__TRANSACTRON_LOG_FILTER"] = ".*"
    os.environ["__TRANSACTRON_LOG_LEVEL"] = "WARNING"
