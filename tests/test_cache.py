import pytest
import redis
from dialogs.cache import get_cache


def test_get_cache(app):
    with app.app_context():
        cache = get_cache()
        assert cache is get_cache()
