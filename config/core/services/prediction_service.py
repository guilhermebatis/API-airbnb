
from modelo.predictor import prever_preco
from core.models import Prediction


def gerar_previsao(user, dados):
    # 1. gerar previsão
    preco = prever_preco(dados)

    # 2. salvar no banco
    prediction = Prediction.objects.create(
        user=user,
        host_is_superhost=dados.get('host_is_superhost'),
        host_total_listings_count=dados.get('host_total_listings_count'),
        latitude=dados.get('latitude'),
        longitude=dados.get('longitude'),
        accommodates=dados.get('accommodates'),
        bathrooms=dados.get('bathrooms'),
        bedrooms=dados.get('bedrooms'),
        beds=dados.get('beds'),
        extra_people=dados.get('extra_people'),
        minimum_nights=dados.get('minimum_nights'),
        number_of_reviews=dados.get('number_of_reviews'),
        instant_bookable=dados.get('instant_bookable'),
        num_amenities=dados.get('num_amenities'),
        property_type=dados.get('property_type'),
        cancellation_policy=dados.get('cancellation_policy'),
        preco_previsto=preco
    )

    # 3. retorno padronizado
    return {
        "preco_previsto": preco,
        "id": prediction.id
    }
