from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import AllowAny
from .serializers import PredictionSerializer
from modelo.model_loader import pipeline, colunas_treino
from modelo.preprocess import transformar_entrada


class PredictionPriceView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        selializer = PredictionSerializer(data=request.data)

        if selializer.is_valid():
            dados = selializer.validated_data

            df = transformar_entrada(dados, colunas_treino)

            previsao = pipeline.predict(df)
            return Response({
                "preco_previsto": float(previsao[0])
            })

        return Response(selializer.errors, status=status.HTTP_400_BAD_REQUEST)
