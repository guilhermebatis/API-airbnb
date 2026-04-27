from rest_framework import serializers
from .models import Prediction


class PredictionSerializer(serializers.Serializer):
    user = serializers.StringRelatedField()
    host_is_superhost = serializers.BooleanField()
    host_total_listings_count = serializers.IntegerField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    accommodates = serializers.IntegerField()
    bathrooms = serializers.IntegerField()
    bedrooms = serializers.IntegerField()
    beds = serializers.IntegerField()
    extra_people = serializers.FloatField()
    minimum_nights = serializers.IntegerField()
    number_of_reviews = serializers.IntegerField()
    instant_bookable = serializers.BooleanField()
    num_amenities = serializers.IntegerField()

    property_type = serializers.ChoiceField(
        choices=['apartment', 'condominium', 'house', 'outro'])
    cancellation_policy = serializers.ChoiceField(
        choices=['moderate', 'flexible', 'strict', 'strict_14_with_grace_period'])


class PredictionModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prediction
        fields = '__all__'
