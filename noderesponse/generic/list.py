from django.views.generic.list import MultipleObjectMixin, BaseListView

from noderesponse.views import NodeView, NodeResponseMixin


class BaseListNodeView(MultipleObjectMixin, NodeView):
    get = BaseListView.get


class ListNodeView(NodeResponseMixin, BaseListNodeView):
    pass
