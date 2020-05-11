from django.views import View

from noderesponse.http import NodeHttpResponse


class NodeView(View):
    def options(self, request, *args, **kwargs):
        response = NodeHttpResponse(data=self.get_data())
        response['Allow'] = ', '.join(self._allowed_methods())
        response['Content-Length'] = '0'
        return response


class NodeResponseMixin:
    node_view_name = None
    response_class = NodeHttpResponse
    content_type = None

    def get_node_view_name(self):
        if self.node_view_name is not None:
            return self.node_view_name
        raise NotImplementedError("Need to set `node_view_name` or `get_node_view_name()`")

    def render_to_response(self, context, **kwargs):
        kwargs.setdefault('content_type', self.content_type)
        return self.response_class(data=self.get_data(**context, **kwargs))

    def get_data(self, **kwargs):
        if "view" in kwargs:
            kwargs.pop("view")
        return {'view': self.get_node_view_name(), 'data': kwargs}
