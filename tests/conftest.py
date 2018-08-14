# setup tests
import pytest
from app.app import app


@pytest.fixture()
def app():
    app = Flask(__name__)
    app.debug = True
    return app