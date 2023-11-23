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
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    category_title = serializers.SerializerMethodField()

    class Meta:
        model = Operations
        fields = ['id', 'category', 'category_title', 'type', 'amount', 'date_time']

    def __init__(self, *args, **kwargs):
        super(OperationSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.user:
            user_categories = Category.objects.filter(user_id=request.user.id)
            self.fields['category'].queryset = user_categories

    def get_category_title(self, obj):
        return obj.category.title if obj.category else None


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)

    class Meta:
        model = Category
        fields = ['title', 'user']
