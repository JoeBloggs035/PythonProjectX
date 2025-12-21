import pytest


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        "viewport": {
            "width": 1280,
            "height": 600,
        }
    }
