# An RPC protocol based on the JSON-RPC 2.0 protocol, using pickle instead of
# json.

# CR cam: Why are we rolling our own rpc, complete with a transport layer??

import asyncio
import pickle
import logging
from dataclasses import dataclass
from collections.abc import Coroutine
from typing import NewType, Optional, Any, Callable, TypeVar, Generic, NoReturn
from typing_extensions import Protocol

import Transport

RequestId = NewType("RequestId", int)


# Calculate the next request ID
def increment_requestid(id: RequestId) -> RequestId:
    return RequestId(id + 1)


@dataclass
class Request:
    id: Optional[RequestId]
    method: str
    params: list[Any]

    def __init__(self, *, method, params, id):
        self.method = method
        self.params = params
        self.id = id

    def serialize(self) -> bytes:
        return pickle.dumps(self)

    def is_notification(self) -> bool:
        return self.id is None


@dataclass
class Response:
    id: Optional[RequestId]
    payload: Any
    is_error: bool

    def __init__(self, *, id: Optional[RequestId], payload: Any, is_error: bool):
        self.id = id
        self.payload = payload
        self.is_error = is_error

    # Convert this response to jsonrpc format
    def serialize(self) -> bytes:
        return pickle.dumps(self)


T = TypeVar("T")


# An [Ivar] is a write-once, concurrent [ref]. Initially, when an ivar is
# created it is "empty", and attempting to [read] from it will block until it
# is [fill]ed from another job.
# XXX: This probably shouldn't live here.
# asyncio sucks for not having this builtin
class Ivar(Generic[T]):
    ev: asyncio.Event
    t: T

    def __init__(self):
        self.ev = asyncio.Event()
        # We explicitly do not set [self.t] here; it should be set by [fill]
        # only.

    async def read(self) -> T:
        await self.ev.wait()
        return self.t

    def fill(self, val: T):
        self.t = val
        self.ev.set()


class Session:
    session: Transport.Session
    curr_id: RequestId
    pending_jobs: set[asyncio.Task]
    pending_requests: dict[RequestId, Ivar[Response]]
    handlers: dict[str, Callable[..., Coroutine[None, None, Any]]]
    raise_on_error_response: bool

    # Initialize session
    def __init__(self, session, raise_on_error_response: bool):
        self.curr_id = RequestId(0)
        self.session = session
        self.handlers = dict()
        self.pending_jobs = set()
        self.pending_requests = dict()
        self.raise_on_error_response = raise_on_error_response

    def register_handler(
        self,
        method_name: str,
        action: Callable[..., Coroutine[None, None, Any]],
    ):
        self.handlers[method_name] = action

    def run_in_background(self, coro: Coroutine):
        task = asyncio.create_task(coro)
        self.pending_jobs.add(task)
        task.add_done_callback(self.pending_jobs.discard)

    async def report_error_nofail(self, error: Exception) -> None:
        logging.exception(f"{error}")
        resp = Response(id=None, payload=error, is_error=True)
        try:
            # send the message
            await self.session.send(
                # convert response to string and encode
                resp.serialize()
            )
        except asyncio.CancelledError:
            raise
        except Exception as e:
            logging.exception(
                f"while reporting previous error, encountered another: {e}"
            )

    # Helper: Handle client request and send response
    async def handle_and_respond(self, req: Request) -> None:
        # if no such requested method, send error
        if req.method not in self.handlers:
            await self.report_error_nofail(ValueError(f"no such method: {req.method}"))
            return
        try:
            result = await self.handlers[req.method](*req.params)
            success = True
        except asyncio.CancelledError:
            raise
        except Exception as e:
            result = e
            success = False

        # Notifications do not expect a response
        if req.is_notification():
            return

        # This [id=req.id] is a bit cheeky. The meaning of [None] in [req.id]
        # is different from [None] in [resp.id], but we know that [req.id]
        # isn't None because of the [req.is_notification] guard above, so we
        # can just satisfy the typechecker without unwrapping.
        resp = Response(id=req.id, payload=result, is_error=not success)

        await self.session.send(resp.serialize())

    # This is the function server uses to handle client requests
    def handle(self, req: Request) -> None:
        self.run_in_background(self.handle_and_respond(req))

    # Calculate fresh request ID for this session
    def fresh_id(self) -> RequestId:
        prev = self.curr_id
        self.curr_id = increment_requestid(self.curr_id)
        return prev

    def raise_response(self, obj: Response) -> NoReturn:
        if isinstance(obj.payload, Exception):
            raise obj.payload
        else:
            raise ValueError(f"error: {obj.payload}")

    # This is the function client uses to send requests
    async def request(
        self, method, *params, is_notification=False
    ) -> Optional[Response]:
        # if notification, no response expected
        if is_notification:
            wait_for_resp = False
            id = None
        else:
            # if will be expecting response, mark request as pending
            wait_for_resp = True
            id = self.fresh_id()
            result_box: Ivar[Response] = Ivar()
            self.pending_requests[id] = result_box

        # create the request, convert it to string, encode, and send
        req = Request(method=method, params=params, id=id)
        await self.session.send(req.serialize())

        # wait for response, read it, and delete pending request
        if wait_for_resp:
            result = await result_box.read()
            # included only to make mypy accept that [wait_for_resp] implies
            # [id is not None]
            assert id is not None
            del self.pending_requests[id]
            if result.is_error and self.raise_on_error_response:
                self.raise_response(result)
            return result.payload
        return None

    async def notification(self, method, *params):
        await self.request(method, *params, is_notification=True)

    # Loop to handle all events: client requests and server responses
    async def run_event_loop(self) -> None:
        async for payload in self.session:
            try:
                obj = pickle.loads(payload)
                if isinstance(obj, Request):
                    self.handle(obj)
                elif isinstance(obj, Response):
                    if obj.id is None:
                        self.raise_response(obj)
                    if obj.id not in self.pending_requests:
                        self.run_in_background(
                            self.report_error_nofail(
                                ValueError("received response to nonexistent request")
                            )
                        )

                    self.pending_requests[obj.id].fill(obj)
                else:
                    self.run_in_background(
                        self.report_error_nofail(ValueError("malformed message"))
                    )
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logging.exception(f"{e}")


# create a session
def spawn_session(reader, writer, *, raise_on_error_response=True) -> Session:
    sess = Transport.Session(reader, writer)
    return Session(sess, raise_on_error_response)
