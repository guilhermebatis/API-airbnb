from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Prediction
from core.services.prediction_service import generate_prediction, average_price_per_property
from .serializers import PredictionSerializer, PredictionModelSerializer
from modelo.predictor import predict_price
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiExample, OpenApiParameter
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from core.permissions import IsOwnerOrAdmin
import logging
from django.contrib.auth.models import User
logger = logging.getLogger(__name__)


@extend_schema(
    summary="Gerar previsão de preço de imóvel",
    request=PredictionSerializer,
    responses={200: OpenApiTypes.OBJECT},
    description="Realiza a previsão de preço de um imóvel com base nos dados fornecidos",
    examples=[
        OpenApiExample(
            "Exemplo de entrada",
            value={
                "host_is_superhost": True,
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
                "cancellation_policy": "flexible"
            }
        )],
    tags=["Predictions"]
)
class PredictionPriceView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PredictionSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        try:
            resultado = generate_prediction(
                serializer.validated_data, request.user)
            return Response(resultado)

        except Exception as e:
            logger.error(f'error gerating prediction: {e}')
            return Response({"error": 'gerating prediction'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    summary="Listar previsões do usuário",
    description="Retorna todas as previsões do usuário autenticado. Admins veem todas as previsões do sistema.",
    responses=PredictionModelSerializer(many=True),
    tags=["Predictions"],
    parameters=[
        OpenApiParameter(
            name="min_price",
            type=float,
            description="Filtrar por preço mínimo previsto"
        ),
        OpenApiParameter(
            name="max_price",
            type=float,
            description="Filtrar por preço máximo previsto"
        ),
        OpenApiParameter(
            name="property_type",
            type=str,
            description="Filtrar por tipo de imóvel (ex: casa, apartamento)"
        ),
    ]
)
class PredictionListView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.is_staff:
            predictions = Prediction.objects.all()
        else:
            predictions = Prediction.objects.filter(user=request.user)

         # 🔍 filtros
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        property_type = request.query_params.get('property_type')

        if min_price:
            predictions = predictions.filter(predicted_price__gte=min_price)

        if max_price:
            predictions = predictions.filter(predicted_price__lte=max_price)

        if property_type:
            predictions = predictions.filter(property_type=property_type)

        predictions = predictions.order_by('-criado_em')

        serializer = PredictionModelSerializer(predictions, many=True)
        return Response(serializer.data)


@extend_schema(
    summary="Detalhes de uma previsão",
    description="""
    Retorna uma previsão específica pertencente ao usuário ou admin.
    """,
    tags=["Predictions"],
    responses=PredictionModelSerializer,
)
class PredictionDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
    queryset = Prediction.objects.all()
    serializer_class = PredictionModelSerializer


@extend_schema(
    description="Retorna a média de preço por tipo de propriedade"
)
class PredictionStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        property_type = request.query_params.get('property_type')
        user_id = request.user.id
        dados = average_price_per_property(user_id, property_type)
        list = []

        for tipo, avg_price in dados:
            list.append({
                "property_type": tipo,
                "avg_price": avg_price
            })

        return Response(list)


class RegisterView(APIView):
    permission_classes = []

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Missing username or password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "User already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        User.objects.create_user(username=username, password=password)

        return Response(
            {"message": "User created"},
            status=status.HTTP_201_CREATED
        )
