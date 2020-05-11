from django.views.generic.detail import SingleObjectMixin, BaseDetailView

from noderesponse.views import NodeView, NodeResponseMixin


class BaseDetailNodeView(SingleObjectMixin, NodeView):
    get = BaseDetailView.get


class DetailNodeView(NodeResponseMixin, BaseDetailNodeView):
    pass