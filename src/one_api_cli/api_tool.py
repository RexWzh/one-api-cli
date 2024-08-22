import os
import httpx
import asyncio
from types import MethodType
from loguru import logger

DEBUG_MODE = os.environ.get('DEBUG_MODE', 'False').lower() == 'true'

class APITool:
    """
    A base class for making HTTP requests using httpx.

    Example:
        api = APITool()
        response = api.make_request('GET', 'https://api.example.com/resource')
        print(response)
    """

    def __init__(self, **default_kwargs):
        """
        Initialize the APITool with default request parameters.

        Args:
            **default_kwargs: Default keyword arguments for httpx requests.
        """
        self.default_kwargs = default_kwargs

    def make_request(self, method, url, **kwargs):
        """
        Make a synchronous HTTP request.

        Args:
            method (str): The HTTP method (e.g., 'GET', 'POST').
            url (str): The URL to send the request to.
            **kwargs: Additional keyword arguments for httpx requests.

        Returns:
            httpx.Response: The response from the server.
        """
        if DEBUG_MODE:
            logger.debug(f"Making request: {method} {url}")
        with httpx.Client() as client:
            request_kwargs = {**self.default_kwargs, **kwargs}
            response = client.request(method, url, **request_kwargs)
            response.raise_for_status()  # Ensure the request was successful
            return response

    async def make_async_request(self, method, url, **kwargs):
        """
        Make an asynchronous HTTP request.

        Args:
            method (str): The HTTP method (e.g., 'GET', 'POST').
            url (str): The URL to send the request to.
            **kwargs: Additional keyword arguments for httpx requests.

        Returns:
            httpx.Response: The response from the server.
        """
        if DEBUG_MODE:
            logger.debug(f"Making request: {method} {url}")
        async with httpx.AsyncClient() as client:
            request_kwargs = {**self.default_kwargs, **kwargs}
            response = await client.request(method, url, **request_kwargs)
            response.raise_for_status()  # Ensure the request was successful
            return response

    def default_postprocess(self, response):
        """
        Default post-processing function.

        Args:
            response (httpx.Response): The response from the server.

        Returns:
            dict: The JSON response from the server.
        """
        return response.json()

class postprocess:
    """
    A decorator to dynamically create API request methods with post-processing.

    Example:
        class MyAPI(APITool):
            @postprocess
            def myfunc(self, response):
                return response.json()

            @myfunc.post('{self.base_url}/resource')
            def foo(self, key='word'):
                return {'json': {'key': key}}

            @myfunc.get('{self.base_url}/resource')
            def bar(self):
                return {}
    """
    def __init__(self, func):
        self.func = func

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return MethodType(self, instance)

    def __call__(self, instance, response):
        return self.func(instance, response)

    def request_method(self, method, url_template):
        def decorator(request_func):
            if asyncio.iscoroutinefunction(request_func):
                async def wrapper(instance, *args, **kwargs):
                    url = url_template.format(self=instance)
                    request_kwargs = request_func(instance, *args, **kwargs)
                    response = await instance.make_async_request(method, url, **request_kwargs)
                    return self(instance, response)
            else:
                def wrapper(instance, *args, **kwargs):
                    url = url_template.format(self=instance)
                    request_kwargs = request_func(instance, *args, **kwargs)
                    response = instance.make_request(method, url, **request_kwargs)
                    return self(instance, response)
            return wrapper
        return decorator

    def get(self, url_template):
        return self.request_method('GET', url_template)

    def post(self, url_template):
        return self.request_method('POST', url_template)

    def put(self, url_template):
        return self.request_method('PUT', url_template)

    def delete(self, url_template):
        return self.request_method('DELETE', url_template)
