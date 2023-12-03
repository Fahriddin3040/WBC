from rest_framework import serializers
from .models import Operations, User, Category
from typing import Union
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    balance = serializers.SerializerMethodField(method_name='get_balance',  read_only=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'password', 'username', 'email', 'balance')

    def get_balance(self, obj) -> Union[float, int]:
        result = 0

        notes = Operations.objects.filter(user=obj)

        for note in notes:
            if note.typ == 1:
                result -= note.amount
            elif note.typ == 2:
                result += note.amount
        return result


class OperationSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), )
    category_title = serializers.SerializerMethodField(method_name='get_category_title')
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Operations
        fields = ['id', 'user', 'category', 'category_title', 'typ', 'comment',  'amount', 'date_time']

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
        fields = ['id', 'user', 'title']


class TokenObtainSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['name'] = user.username

        return token
