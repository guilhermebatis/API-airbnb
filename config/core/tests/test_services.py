from django.test import TestCase
from django.contrib.auth.models import User
from core.services.prediction_service import generate_prediction
from core.models import Prediction


class ServicesTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123')

    def test_generate_prediction(self):
        data = {"host_is_superhost": True,
                "host_total_listings_count": 5,
                "latitude": -23.5,
                "longitude": -46.6,
                "accommodates": 3,
                "bathrooms": 1,
                "bedrooms": 2,
                "beds": 2,
                "extra_people": 50,
                "minimum_nights": 2,
                "number_of_reviews": 10,
                "instant_bookable": True,
                "num_amenities": 15,
                "property_type": "apartment",
                "cancellation_policy": "flexible"}

        result = generate_prediction(data, self.user)

        self.assertIn('predicted_price', result)
        self.assertIn('id', result)
        self.assertIsInstance(result['predicted_price'], (int, float))
        self.assertEqual(Prediction.objects.count(), 1)
        self.assertGreater(result['predicted_price'], 0)

    def test_generate_prediction_invalid_input(self):
        data = {}

        with self.assertRaises(ValueError):
            generate_prediction(data, self.user)

    def test_generate_prediction_creates_multiple_records(self):
        data = {"host_is_superhost": True,
                "host_total_listings_count": 5,
                "latitude": -23.5,
                "longitude": -46.6,
                "accommodates": 3,
                "bathrooms": 1,
                "bedrooms": 2,
                "beds": 2,
                "extra_people": 50,
                "minimum_nights": 2,
                "number_of_reviews": 10,
                "instant_bookable": True,
                "num_amenities": 15,
                "property_type": "apartment",
                "cancellation_policy": "flexible"}

        generate_prediction(data, self.user)
        generate_prediction(data, self.user)

        self.assertEqual(Prediction.objects.count(), 2)
