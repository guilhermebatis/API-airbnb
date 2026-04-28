from django.urls import path
from .views import PredictionPriceView, PredictionListView, PredictionDetailView, PredictionStatusView

urlpatterns = [
    path("predict/", PredictionPriceView.as_view(), name="predict"),
    path('predictions/', PredictionListView.as_view()),
    path('predictions/<int:pk>/', PredictionDetailView.as_view(),
         name='prediction-detail'),
    path('predictions/status', PredictionStatusView.as_view(),
         name='prediction-status')
]
