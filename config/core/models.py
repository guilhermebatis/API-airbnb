from django.db import models
from django.contrib.auth.models import User


class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    host_is_superhost = models.BooleanField()
    host_total_listings_count = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    accommodates = models.IntegerField()
    bathrooms = models.IntegerField()
    bedrooms = models.IntegerField()
    beds = models.IntegerField()
    extra_people = models.FloatField()
    minimum_nights = models.IntegerField()
    number_of_reviews = models.IntegerField()
    instant_bookable = models.BooleanField()
    num_amenities = models.IntegerField()
    property_type = models.CharField(max_length=100,)
    cancellation_policy = models.CharField(
        max_length=100,)

    predicted_price = models.FloatField()

    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Predição - {self.predicted_price}"
