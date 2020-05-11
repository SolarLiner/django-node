from example_nodeview.models import House, Person
from noderesponse.generic.detail import DetailNodeView
from noderesponse.generic.list import ListNodeView


class HousesView(ListNodeView):
    model = House
    node_view_name = "house_list"


class HouseDetailView(DetailNodeView):
    model = House
    node_view_name = "house_detail"


class PeopleView(ListNodeView):
    model = Person
    node_view_name = "people_list"


class PersonDetailView(DetailNodeView):
    model = Person
    node_view_name = "person_detail"
