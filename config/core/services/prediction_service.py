
from modelo.predictor import predict_price
from core.models import Prediction
from django.db import connection


def generate_prediction(user, input_data):
    # 1. gerar previsão
    price = predict_price(input_data)

    # 2. salvar no banco
    prediction = Prediction.objects.create(
        user=user,
        host_is_superhost=input_data.get('host_is_superhost'),
        host_total_listings_count=input_data.get('host_total_listings_count'),
        latitude=input_data.get('latitude'),
        longitude=input_data.get('longitude'),
        accommodates=input_data.get('accommodates'),
        bathrooms=input_data.get('bathrooms'),
        bedrooms=input_data.get('bedrooms'),
        beds=input_data.get('beds'),
        extra_people=input_data.get('extra_people'),
        minimum_nights=input_data.get('minimum_nights'),
        number_of_reviews=input_data.get('number_of_reviews'),
        instant_bookable=input_data.get('instant_bookable'),
        num_amenities=input_data.get('num_amenities'),
        property_type=input_data.get('property_type'),
        cancellation_policy=input_data.get('cancellation_policy'),
        preco_previsto=price
    )

    # 3. retorno padronizado
    return {
        "predict_price": price,
        "id": prediction.id
    }


def average_price_per_property(user_id, property_type=None):
    with connection.cursor() as cursor:

        query = """
            SELECT property_type, AVG(predict_price)
            FROM core_prediction
            WHERE user_id = %s
            """
        params = [user_id]

        if property_type:
            query += " AND property_type = %s"
            params.append(property_type)

        query += " GROUP BY property_type"

        cursor.execute(query, params)

        result = cursor.fetchall()
    return (result)
