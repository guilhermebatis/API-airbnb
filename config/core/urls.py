from django.urls import path
from .views import PredictionPriceView

urlpatterns = [
    path("predict/", PredictionPriceView.as_view(), name="predict"),
]
