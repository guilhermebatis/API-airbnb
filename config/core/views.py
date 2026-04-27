from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import PredictionSerializer
from modelo.model_loader import pipeline, colunas_treino
from modelo.preprocess import transformar_entrada


@extend_schema(
    request=PredictionSerializer,
    responses={200: OpenApiTypes.OBJECT},
    description="Realiza a previsão de preço de um imóvel com base nos dados fornecidos",
)
class PredictionPriceView(APIView):

    permission_classes = [AllowAny]

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

        if selializer.is_valid():
            dados = selializer.validated_data

            df = transformar_entrada(dados, colunas_treino)

            previsao = pipeline.predict(df)
            return Response({
                "preco_previsto": float(previsao[0])
            })

        return Response(selializer.errors, status=status.HTTP_400_BAD_REQUEST)
