from django.views.generic.dates import DateMixin, BaseDateListView, BaseArchiveIndexView, YearMixin, \
    BaseYearArchiveView, MonthMixin, BaseMonthArchiveView, WeekMixin, BaseWeekArchiveView, BaseDayArchiveView, DayMixin, \
    BaseTodayArchiveView, BaseDateDetailView
from django.views.generic.list import MultipleObjectMixin

from noderesponse.generic.detail import BaseDetailNodeView
from noderesponse.views import NodeView, NodeResponseMixin


class BaseDateListNodeView(MultipleObjectMixin, DateMixin, NodeView):
    allow_empty = False
    date_list_period = 'year'

    get = BaseDateListView.get
    get_dated_items = BaseDateListView.get_dated_items
    get_ordering = BaseDateListView.get_ordering
    get_dated_queryset = BaseDateListView.get_dated_queryset
    get_date_list_period = BaseDateListView.get_date_list_period
    get_date_list = BaseDateListView.get_date_list


class BaseArchiveIndexNodeView(BaseDateListNodeView):
    context_object_name = 'latest'

    get_dated_items = BaseArchiveIndexView.get_dated_items


class ArchiveIndexNodeView(BaseArchiveIndexView):
    pass


class BaseYearArchiveNodeView(YearMixin, BaseDateListNodeView):
    date_list_period = 'month'
    make_object_list = False

    get_dated_items = BaseYearArchiveView.get_dated_items
    get_make_object_list = BaseYearArchiveView.get_make_object_list


class YearArchiveNodeView(NodeResponseMixin, BaseYearArchiveView):
    pass


class BaseMonthArchiveNodeView(YearMixin, MonthMixin, BaseDateListNodeView):
    date_list_period = 'day'

    get_dated_items = BaseMonthArchiveView.get_dated_items


class MonthArchiveNodeView(NodeResponseMixin, BaseMonthArchiveNodeView):
    pass


class BaseWeekArchiveNodeView(YearMixin, WeekMixin, BaseDateListNodeView):
    get_dated_items = BaseWeekArchiveView.get_dated_items


class WeekArchiveNodeView(NodeResponseMixin, BaseWeekArchiveNodeView):
    pass


class BaseDayArchiveNodeView(YearMixin, MonthMixin, DayMixin, BaseDateListNodeView):
    get_dated_items = BaseDayArchiveView.get_dated_items
    _get_dated_items = BaseDayArchiveView._get_dated_items


class DayArchiveNodeView(NodeResponseMixin, BaseDayArchiveNodeView):
    pass


class BaseTodayArchiveNodeView(BaseDayArchiveNodeView):
    get_dated_items = BaseTodayArchiveView.get_dated_items


class TodayArchiveNodeView(NodeResponseMixin, BaseTodayArchiveNodeView):
    pass


class BaseDateDetailNodeView(YearMixin, MonthMixin, DayMixin, DateMixin, BaseDetailNodeView):
    get_object = BaseDateDetailView.get_object


class DateDetailNodeView(NodeResponseMixin, BaseDateDetailNodeView):
    pass