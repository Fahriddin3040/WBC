from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view
from rest_framework import serializers
from .models import Operations, User
from rest_framework.serializers import ModelSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class OperationSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Operations
        fields = '__all__'

    # ('user', 'category', 'reason', 'price', 'date_time')


# @extend_schema(tags=["Posts"]
# @extend_schema_view(
#     retrieve=extend_schema(
#         summary="Детальная информация о посте",
#         responses={
#             status.HTTP_500_INTERNAL_SERVER_ERROR: OpenApiResponse(
#                 response=None,
#                 description='Описание 500 ответа'),
#         },
#     ),)
