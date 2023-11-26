from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view
from rest_framework import serializers
from .models import Operations, User, Category
from rest_framework.serializers import ModelSerializer


class UserSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField(method_name='get_balance',  read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'username', 'email', 'balance')

    def create(self, validated_data):
        password = validated_data.pop('password', None)

        user = super(UserSerializer, self).create(validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def get_balance(self, obj):
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

    def get_category_title(self, obj):
        return obj.category.title

    def get_username(self, obj):
        return obj.user.username

    def get_categories(self):
        categories = Category.objects.filter(user=self.user)
        return categories


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Category
        fields = ['title', 'user']
