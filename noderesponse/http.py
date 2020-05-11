import json
from json.encoder import JSONEncoder
from typing import Optional

import zmq
from django.db.models import QuerySet
from django.db.models.base import ModelBase
from django.forms import model_to_dict
from django.http.response import HttpResponseBase


class DataEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, QuerySet):
            return [entry for entry in o.values()]
        elif isinstance(o, ModelBase):
            return model_to_dict(o, fields=[field.name for field in o._meta.fields])
        return super().default(o)


class NodeProcess:
    context: Optional[zmq.Context] = None
    socket: Optional[zmq.Socket] = None

    @staticmethod
    def get_socket() -> zmq.Socket:
        self = NodeProcess
        if self.context is None:
            self.context = zmq.Context()
        if self.socket is None:
            self.socket = self.context.socket(zmq.REQ)
            self.socket.connect("tcp://localhost:5000")

        return self.socket


class NodeHttpResponse(HttpResponseBase):
    streaming = False

    def __init__(self, data=None, *args, **kwargs):
        super().__init__()
        self.data = data
        self._node_response = None

    def __repr__(self):
        return f"<{self.__class__.__name__} status_code={self.status_code} {self._content_type_for_repr}"

    def serialize(self):
        return self.serialize_headers() + b'\r\n\r\n' + self.content

    __bytes__ = serialize

    @property
    def content(self):
        if self._node_response is None:
            self._node_response = self._send_node_request()
        return self._node_response

    def _send_node_request(self):
        sock = NodeProcess.get_socket()

        sock.send_string(self._serialize_data())
        return bytes(sock.recv_string(), encoding="utf-8")

    def tell(self):
        return len(self.content)

    def getvalue(self):
        return self.content

    def writable(self):
        return False

    def writelines(self, lines):
        raise IOError()

    def _serialize_data(self):
        return json.dumps(self.data, cls=DataEncoder)

    def __iter__(self):
        return iter([self.content])
