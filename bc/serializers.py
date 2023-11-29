import rest_framework.exceptions
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view
from rest_framework import serializers
from .models import Operations, User, Category
from typing import Union
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class UserSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField(method_name='get_balance',  read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'password', 'username', 'email', 'balance')

    def get_balance(self, obj) -> Union[float, int]:
        return obj.calculated_balance()


class OperationSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), )
    category_title = serializers.SerializerMethodField(method_name='get_category_title')
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Operations
        fields = ['id', 'user', 'category', 'category_title', 'typ', 'amount', 'date_time']

    def __init__(self, *args, **kwargs):
        super(OperationSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user:
            user_categories = Category.objects.filter(user_id=request.user.id)
            self.fields['category'].queryset = user_categories

    def get_category_title(self, obj) -> str:
        return obj.category.title

    def get_username(self, obj) -> str:
        return obj.user.username

    def get_categories(self):
        categories = Category.objects.filter(user=self.user)
        return categories


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Category
        fields = ['title', 'user']


class TokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username

        return token
