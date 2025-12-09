import functools
import inspect
import types
from http import HTTPStatus
from typing import Any
import logging
import traceback

logger = logging.getLogger("AT_SIMULATION_API")


class Error(Exception):
    def __init__(
        self,
        error: str,
        status_code: int,
        http_error: str,
        error_details: dict[str, Any],
        **kwargs,
    ):
        super().__init__(error)
        self.error = error
        self.http_error = http_error
        self.status_code = status_code
        self.error_details = error_details
        self.context = kwargs

    def to_dict(self):
        return {
            "error": str(self),
            "status_code": self.status_code,
            "error_details": self.error_details,
            **self.context,
        }


class InternalServerError(Error):
    def __init__(self, error: str, error_details: dict[str, Any] = {}, **kwargs):
        super().__init__(
            error,
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            http_error="Internal Server Error",
            error_details=error_details,
            **kwargs,
        )


class BadRequestError(Error):
    def __init__(self, error: str, error_details: dict[str, Any] = {}, **kwargs):
        super().__init__(
            error,
            status_code=HTTPStatus.BAD_REQUEST,
            http_error="Bad Request Error",
            error_details=error_details,
            **kwargs,
        )


class AuthError(Error):
    def __init__(self, error: str, error_details: dict[str, Any] = {}, **kwargs):
        super().__init__(
            error,
            status_code=HTTPStatus.UNAUTHORIZED,
            http_error="Authorization Error",
            error_details=error_details,
            **kwargs,
        )


class ForbiddenError(Error):
    def __init__(self, error: str, error_details: dict[str, Any] = {}, **kwargs):
        super().__init__(
            error,
            status_code=HTTPStatus.FORBIDDEN,
            http_error="Forbidden Error",
            error_details=error_details,
            **kwargs,
        )


class NotFoundError(Error):
    def __init__(self, error: str, error_details: dict[str, Any] = {}, **kwargs):
        super().__init__(
            error,
            status_code=HTTPStatus.NOT_FOUND,
            http_error="Not Found Error",
            error_details=error_details,
            **kwargs,
        )


def wrap_exceptions():
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Error as e:
                logger.error(traceback.format_exc())
                class_name = None
                if len(args) > 0:
                    instance_or_cls = args[0]
                    if inspect.isclass(instance_or_cls):
                        class_name = instance_or_cls.__name__
                    elif hasattr(instance_or_cls, "__class__"):
                        class_name = instance_or_cls.__class__.__name__

                method_name = func.__name__
                e.error = f"{class_name}.{method_name}: {str(e)}"
                raise e
            except Exception as e:
                logger.error(traceback.format_exc())
                class_name = None
                if len(args) > 0:
                    instance_or_cls = args[0]
                    if inspect.isclass(instance_or_cls):
                        class_name = instance_or_cls.__name__
                    elif hasattr(instance_or_cls, "__class__"):
                        class_name = instance_or_cls.__class__.__name__

                method_name = func.__name__
                context = {"class_name": class_name, "method_name": method_name}
                raise InternalServerError(
                    f"{class_name}.{method_name}: {str(e)}", **context
                ) from e

        return wrapper

    return decorator


class WrapMethodsMeta(type):
    def __new__(cls, name, bases, dct):
        for attr_name, attr_value in dct.items():
            if isinstance(attr_value, types.FunctionType):
                dct[attr_name] = wrap_exceptions()(attr_value)
        return super().__new__(cls, name, bases, dct)
