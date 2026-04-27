from django.urls import path
from .views import PredictionPriceView, PredictionListView

urlpatterns = [
    path("predict/", PredictionPriceView.as_view(), name="predict"),
    path('predictions/', PredictionListView.as_view()),
]
