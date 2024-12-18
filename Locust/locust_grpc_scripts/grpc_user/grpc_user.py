from locust import User
from locust.exception import LocustError

import time
from typing import Any, Callable

import grpc
import grpc.experimental.gevent as grpc_gevent
from grpc_interceptor import ClientInterceptor

# patch grpc so that it uses gevent instead of asyncio
grpc_gevent.init_gevent()


class LocustInterceptor(ClientInterceptor):
    def __init__(self, environment, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.env = environment

    def intercept(
        self,
        method: Callable,
        request_or_iterator: Any,
        call_details: grpc.ClientCallDetails,
    ):
        response = None
        exception = None
        start_perf_counter = time.perf_counter()
        try:
            # Call the method, which could be a streaming call
            response = method(request_or_iterator, call_details)
            if hasattr(response, '__iter__'):
                # If the response is an iterator (streaming), consume it
                response_length = 0
                for resp in response:
                    # Measure length of each response
                    response_length += resp.ByteSize() if resp else 0
                # Fire a request event for the entire stream
                self.env.events.request.fire(
                    request_type="grpc",
                    name=call_details.method,
                    response_time=(time.perf_counter() - start_perf_counter) * 1000,
                    response_length=response_length,
                    response=response,
                    context=None,
                    exception=exception,
                )
            else:
                # Handle unary response
                response_length = response.ByteSize()
                self.env.events.request.fire(
                    request_type="grpc",
                    name=call_details.method,
                    response_time=(time.perf_counter() - start_perf_counter) * 1000,
                    response_length=response_length,
                    response=response,
                    context=None,
                    exception=exception,
                )
        except grpc.RpcError as e:
            exception = e
            self.env.events.request.fire(
                request_type="grpc",
                name=call_details.method,
                response_time=(time.perf_counter() - start_perf_counter) * 1000,
                response_length=0,
                response=None,
                context=None,
                exception=exception,
            )
        
        return response


class GrpcUser(User):
    abstract = True
    stub_class = None

    def __init__(self, environment):
        super().__init__(environment)
        for attr_value, attr_name in ((self.host, "host"), (self.stub_class, "stub_class")):
            if attr_value is None:
                raise LocustError(f"You must specify the {attr_name}.")

        self._channel = grpc.insecure_channel(self.host)
        interceptor = LocustInterceptor(environment=environment)
        self._channel = grpc.intercept_channel(self._channel, interceptor)

        self.stub = self.stub_class(self._channel)