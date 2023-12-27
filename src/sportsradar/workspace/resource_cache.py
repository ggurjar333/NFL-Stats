"""Implementations of datastore resource caches."""
from abc import ABC, abstractmethod
from typing import Any, Dict

import redis
import json
import traceback

import src.sportsradar.logging_helpers

logger = src.sportsradar.logging_helpers.get_logger(__name__)


class NFLStatsResourceKey(Dict):
    """Uniquely identifies a specific resource."""

    def __dict__(self):
        # Convert the NFLStatsResourceKey instance to a dict representation
        return self.values()


# class NFLStatsResourceKey(NamedTuple):
#     """Uniquely identifies a specific resource."""
#
#     def to_dict(self):
#         # Convert the NFLStatsResourceKey instance to a dictionary representation
#         return self._asdict()
#
#     def __str__(self):
#         # Convert the NFLStatsResourceKey instance to a string representation
#         return "some_string_representation"


def add(self, resource: NFLStatsResourceKey, value: bytes):
    """Adds (or updates) resource to the cache with given value."""
    if self.is_read_only():
        logger.debug(f"Read only cache: ignoring set({resource})")
        return
    self._db.set(str(resource), value)


def get(self, resource: NFLStatsResourceKey) -> bytes:
    """Retrieves value associated with a given resource."""
    value = self._db.get(str(resource))
    if value is None:
        raise KeyError(f"Resource {resource} not found in the Redis cache")
    return value


def delete(self, resource: NFLStatsResourceKey):
    """Deletes resource from the cache."""
    if self.is_read_only():
        logger.debug(f"Read only cache: ignoring delete({resource})")
        return
    self._db.delete(str(resource))


def contains(self, resource: NFLStatsResourceKey) -> bool:
    """Returns True if resource is present in the cache."""
    return bool(self._db.exists(str(resource)))


class AbstractCache(ABC):
    """Defines interface for the generic resource caching layer."""

    def __init__(self, read_only: bool = False):
        """Constructs instance and sets read-only attribute."""
        self._read_only = read_only

    def is_read_only(self) -> bool:
        """Returns true if the cache is read-only and should not be modified."""
        return self._read_only

    @abstractmethod
    def get(self, resource: NFLStatsResourceKey) -> bytes:
        """Retrieves content of the given resource or throws KeyError."""
        pass

    @abstractmethod
    def add(self, resource: NFLStatsResourceKey, content: bytes) -> None:
        """Adds resource to the cache and sets the content."""
        pass

    @abstractmethod
    def delete(self, resource: NFLStatsResourceKey) -> None:
        """Removes the resource from cache."""
        pass

    @abstractmethod
    def contains(self, resource: NFLStatsResourceKey) -> bool:
        """Returns True if the resource is present in the cache."""
        pass


class LayeredCache(AbstractCache):
    """Implements multi-layered system of caches.

    This allows building multi-layered system of caches. The idea is that you can have
    faster local cache with fall-back to the more remote or expensive caches that can
    be accessed in case of missing content.

    Only the closest layer is being written to (set, delete), while all remaining layers
    are read-only (get).
    """

    def __init__(self, *caches: list[AbstractCache], **kwargs: Any):
        """Creates layered cache consisting of given cache layers.

        Args:
            caches: List of caching layers to uses. These are given in the order
            of decreasing priority.
        """
        super().__init__(**kwargs)
        self._caches: list[AbstractCache] = list(caches)

    def add_cache_layer(self, cache: AbstractCache):
        """Adds a cache layer.

        The priority is below all other.
        """
        self._caches.append(cache)

    def num_layers(self):
        """Returns the number of caching layers that are in this LayeredCache."""
        return len(self._caches)

    def get(self, resource: NFLStatsResourceKey) -> bytes:
        """Returns the content of a given resource."""
        for i, cache in enumerate(self._caches):
            if cache.contains(str(resource)):
                logger.debug(
                    f"get:{resource} found in {i}-th layer ({cache.__class__.__name__})."
                )
                return cache.get(resource)
            logger.debug(f"get:{resource} not found in the layered cache.")
            raise KeyError(f"{resource} not found in the layered cache.")

    def add(self, resource: NFLStatsResourceKey, value):
        """Adds (or replaces) resource into the cache with given value."""
        if self.is_read_only():
            logger.debug(f"Read only cache: ignoring set({resource})")
            return
        for cache_layer in self._caches:
            if cache_layer.is_read_only():
                continue
            cache_layer.add(
                str(resource), value
            )  # Convert the NFLStatsResourceKey to string
            logger.debug(
                f"Add {resource} to cache layer {cache_layer.__class__.__name__}"
            )
            break

    def delete(self, resource: NFLStatsResourceKey):
        """Removes resource from the cache if the cache is not in the read_only mode."""
        if self.is_read_only():
            logger.debug(f"Read only cache: ignoring delete({resource})")
            return
        for cache_layer in self._caches:
            if cache_layer.is_read_only():
                continue
            cache_layer.delete(str(resource))
            break

    def contains(self, resource: NFLStatsResourceKey) -> bool:
        """Returns True if resource is present in the cache."""
        for i, cache_layer in enumerate(self._caches):
            if cache_layer.contains(str(resource)):
                logger.debug(
                    f"contains:{resource} found in {i}-th layer ({cache_layer.__class__.__name__})."
                )
                return True
        logger.debug(f"contains: {resource} not found in the layered cache.")
        return False

    def is_optionally_cached(self, resource: NFLStatsResourceKey) -> bool:
        """Returns True if resource is contained in the closest write-enabled layer."""
        for cache_layer in self._caches:
            if cache_layer.is_read_only():
                continue
            logger.debug(
                f"{resource} is optionally cached in {cache_layer.__class__.__name__}"
            )
            return cache_layer.contains(resource)


class RedisCache(AbstractCache):
    """Implements cache system using Redis server."""

    def __init__(self, host="localhost", port=6379, **kwargs: Any):
        """Constructs a RedisCache instance."""
        super().__init__(**kwargs)
        self._db = redis.StrictRedis(host=host, port=port)

    def get(self, resource: NFLStatsResourceKey) -> bytes:
        """Retrieves value associated with a given resource."""
        value = self._db.get(str(resource))
        if value is None:
            raise KeyError(f"Resource {resource} not found in the Redis cache")
        return value

    def add(self, resource: NFLStatsResourceKey, value: bytes):
        """Adds (or updates) resource to the cache with given value."""
        if self.is_read_only():
            logger.debug(f"Read only cache: ignoring set({resource})")
            return
        self._db.set(str(resource), value)

    def delete(self, resource: NFLStatsResourceKey):
        """Deletes resource from the cache."""
        if self.is_read_only():
            logger.debug(f"Read only cache: ignoring delete({resource})")
            return
        self._db.delete(str(resource))

    def contains(self, resource: NFLStatsResourceKey) -> bool:
        """Returns True if resource is present in the cache."""
        return bool(self._db.exists(str(resource)))

    def put_dict(self, key, dictionary):
        """Store a dictionary in the Redis."""
        try:
            dict_json = json.dumps(dictionary)
            self._db.set(key, dict_json)
        except Exception as e:
            logger.error(f"Failed to put dict in Redis: {str(e)}")

    def get_dict(self, key):
        """Retrieve a dictionary from the Redis."""
        try:
            dict_json = self._db.get(key)
            if dict_json is None:
                return None
            return json.loads(dict_json)
        except Exception as e:
            logger.error(f"Failed to put dict in Redis: {str(e)}")
            return None


# python

# Create an instance of RedisCache
try:
    redis_cache = RedisCache()
except Exception:
    print("Failed to create Redis cache")
    traceback.print_exc()

# Check all the operations: add, get, contains and delete
try:
    # Create a 'LayeredCache' with the redis cache as its only layer
    layered_cache = LayeredCache(redis_cache)
    # Create a resource key
    resource_key = NFLStatsResourceKey()  # Initialize it properly
    # Add a resource to the layered cache
    layered_cache.add(resource_key, f"{'abc':123}")

    # Check if the resource exists in the cache
    if layered_cache.contains(resource_key):
        print("Resource exists in the cache.")
        # Get the resource value
        value = layered_cache.get(resource_key)
        print(f"Value: {value}")
    # Delete the resource
    if layered_cache.contains(resource_key):
        print(f"Deleting the resource: {resource_key.values()}")
        layered_cache.delete(resource_key)
except Exception:
    print("An error occurred during cache operations.")
    traceback.print_exc()


# # Create an instance of RedisCache
# redis_cache = RedisCache()
#
# # Create a 'LayeredCache' with the redis cache as its only layer
# layered_cache = LayeredCache(redis_cache)
#
# # Create a resource key
# resource_key = NFLStatsResourceKey()
#
# # Add a resource to the layered cache
# layered_cache.add(resource_key, b"Some content")
#
# # Check if the resource exists in the cache
# if layered_cache.contains(resource_key):
#     print("Resource exists in the cache.")
#
# # Get the resource value
# value = layered_cache.get(resource_key)
# print(f'Value: {value}')
#
# # Delete the resource
# layered_cache.delete(resource_key)
