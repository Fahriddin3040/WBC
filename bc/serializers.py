from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view
from rest_framework import serializers
from .models import Operations, User, Category
from rest_framework.serializers import ModelSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'password', 'username', 'email',)

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        user = super(UserSerializer, self).create(validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class OperationSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='slug', queryset=Category.objects.all())

    class Meta:
        model = Operations
        fields = ['id', 'category', 'type', 'amount', 'date_time']

    def __init__(self, *args, **kwargs):
        super(OperationSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user:
            self.fields['category'].queryset = Category.get_categories(user=request.user)



class CategorySerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    class Meta:
        model = Category
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
