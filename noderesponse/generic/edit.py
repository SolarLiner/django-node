from django.views.generic.edit import ProcessFormView, FormMixin, ModelFormMixin, BaseCreateView, BaseUpdateView, \
    DeletionMixin

from noderesponse.generic.detail import BaseDetailNodeView
from noderesponse.views import NodeView, NodeResponseMixin


class ProcessFormNodeView(NodeView):
    get = ProcessFormView.get
    post = ProcessFormView.post
    put = ProcessFormView.put


class BaseFormNodeView(FormMixin, ProcessFormNodeView):
    pass


class FormNodeView(NodeResponseMixin, BaseFormNodeView):
    pass


class BaseCreateNodeView(ModelFormMixin, ProcessFormNodeView):
    get = BaseCreateView.get
    post = BaseCreateView.post


class CreateNodeView(NodeResponseMixin, NodeView):
    pass


class BaseUpdateNodeView(ModelFormMixin, ProcessFormNodeView):
    get = BaseUpdateView.get
    post = BaseUpdateView.post


class UpdateNodeView(NodeResponseMixin, BaseUpdateNodeView):
    pass


class BaseDeleteNodeView(DeletionMixin, BaseDetailNodeView):
    pass


class DeleteNodeView(NodeResponseMixin, BaseDeleteNodeView):
    pass