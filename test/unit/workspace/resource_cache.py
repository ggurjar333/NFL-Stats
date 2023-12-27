# These are the unit tests for the `resource_cache.py` module
# As we are going to interact with a database, remember to setup
# and tear down your test environment properly.

import unittest
from unittest.mock import patch, MagicMock
from src.sportsradar.workspace.resource_cache import (
    NFLStatsResourceKey,
    AbstractCache,
    LayeredCache,
    RedisCache,
)


class TestResourceCache(unittest.TestCase):
    """
    Test cases for testing the cache mechanisms implemented in the resource_cache.py
    """

    def setUp(self) -> None:
        """Set up test fixtures, if any."""
        self.resource_key = NFLStatsResourceKey()
        self.resource_value = b"This is a test"

    def tearDown(self) -> None:
        """Tear down test fixtures, if any."""
        pass

    @patch("redis.StrictRedis")
    def test_redis_cache(self, mock_redis):
        """Test RedisCache implementation"""
        cache = RedisCache()
        mock_redis.exists.return_value = False
        self.assertEqual(cache.contains(self.resource_key), False)
        mock_redis.set.return_value = None
        cache.add(self.resource_key, self.resource_value)
        mock_redis.get.return_value = self.resource_value
        self.assertEqual(cache.get(self.resource_key), self.resource_value)
        mock_redis.delete.return_value = None
        cache.delete(self.resource_key)

    @patch.object(AbstractCache, "__abstractmethods__", set())
    def test_abstract_cache(self):
        """Test AbstractCache implementation"""
        cache = AbstractCache()
        with self.assertRaises(KeyError):
            cache.get(
                "nonexistent resource key"
            )  # This key does not exist in the cache

    def test_layered_cache(self):
        """Test LayeredCache implementation"""
        # Mocking a AbstractCache object
        cache = MagicMock(spec=AbstractCache)

        cache.contains.return_value = True  # Ensure the key exists in the cache
        cache.get.return_value = self.resource_value

        layered_cache = LayeredCache(cache)
        layered_cache.add(self.resource_key, self.resource_value)
        self.assertEqual(layered_cache.get(self.resource_key), self.resource_value)


if __name__ == "__main__":
    unittest.main()
