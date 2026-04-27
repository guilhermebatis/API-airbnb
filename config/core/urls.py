from django.urls import path
from .views import PredictionPriceView, PredictionListView, PredictionDetailView

urlpatterns = [
    path("predict/", PredictionPriceView.as_view(), name="predict"),
    path('predictions/', PredictionListView.as_view()),
    path('predictions/<int:pk>/', PredictionDetailView.as_view(),
         name='prediction-detail')
]
