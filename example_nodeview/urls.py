from django.urls import path

from example_nodeview.views import HousesView, HouseDetailView, PeopleView, PersonDetailView

urlpatterns = [
    path('', HousesView.as_view()),
    path('house/<pk>', HouseDetailView.as_view()),
    path('people', PeopleView.as_view()),
    path('person/<pk>', PersonDetailView.as_view()),
]