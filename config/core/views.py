from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Prediction
from core.services.prediction_service import gerar_previsao
from .serializers import PredictionSerializer, PredictionModelSerializer
from modelo.predictor import prever_preco
from drf_spectacular.utils import extend_schema, OpenApiTypes
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from core.permissions import IsOwnerOrAdmin


@extend_schema(
    request=PredictionSerializer,
    responses={200: OpenApiTypes.OBJECT},
    description="Realiza a previsão de preço de um imóvel com base nos dados fornecidos",
)
class PredictionPriceView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PredictionSerializer(data=request.data)

        if serializer.is_valid():
            resultado = gerar_previsao(serializer.validated_data, request.user)
            return Response(resultado)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    responses=PredictionModelSerializer(many=True)
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
            predictions = predictions.filter(preco_previsto__gte=min_price)

        if max_price:
            predictions = predictions.filter(preco_previsto__lte=max_price)

        if property_type:
            predictions = predictions.filter(property_type=property_type)

        predictions = predictions.order_by('-criado_em')

        serializer = PredictionModelSerializer(predictions, many=True)
        return Response(serializer.data)


class PredictionDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Prediction.objects.all()
    serializer_class = PredictionModelSerializer
    permission_classes = [IsOwnerOrAdmin]
