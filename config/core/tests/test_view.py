from rest_framework.test import APITestCase
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from unittest.mock import patch
from core.services.prediction_service import generate_prediction


class PredictionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpass123')

        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def test_prediction_price_success(self):
        response = self.client.post('/api/predict/', {"host_is_superhost": True,
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
                                                      "cancellation_policy": "flexible"}, format='json')

        self.assertEqual(response.status_code, 200)
        self.assertIn('predicted_price', response.data)
        self.assertIsInstance(response.data['predicted_price'], (int, float))

    def test_prediction_price_invalid_input(self):

        response = self.client.post('/api/predict/', {}, format='json')

        self.assertEqual(response.status_code, 400)

    def test_unauthorized_access(self):
        self.client.credentials()

        response = self.client.post('/api/predict/', {}, )

        self.assertEqual(response.status_code, 401)

    @patch('core.views.generate_prediction')
    def test_prediction_mocked(self, mock_generate):
        mock_generate.return_value = {
            "predicted_price": 500,
            "id": 1
        }

        response = self.client.post('/api/predict/', {"host_is_superhost": True,
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
                                                      "cancellation_policy": "flexible"}, format='json')

        self.assertEqual(response.data['predicted_price'], 500)
        mock_generate.assert_called_once()

    def test_user_cannot_access_other_prediction(self):

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

        user_1 = User.objects.create_user(
            username='user', password='pass123')
        user_2 = User.objects.create_user(
            username='otheruser', password='otherpass123')

        prediction = generate_prediction(data, user_1)
        prediction_id = prediction['id']

        refresh = RefreshToken.for_user(user_2)
        token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.get(f'/api/predictions/{prediction_id}/')

        self.assertEqual(response.status_code, 403)

    def test_admin_can_access_all_predictions(self):

        user_1 = User.objects.create_user(
            username='user', password='pass123')

        admin_user = User.objects.create_user(
            username='admin', password='adminpass123', is_staff=True)

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

        prediction = generate_prediction(data, user_1)
        prediction_id = prediction['id']

        refresh = RefreshToken.for_user(admin_user)
        token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.get(f'/api/predictions/{prediction_id}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['id'], prediction_id)
        self.assertIn('predicted_price', response.data)
