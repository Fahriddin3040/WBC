import rest_framework.exceptions
from django.http import HttpResponseRedirect
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from .serializers import OperationSerializer, UserSerializer, CategorySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework import viewsets, status
from .models import Category, User
from . import models


@extend_schema_view(
    list=extend_schema(
        summary="Получить список постов",
    ),
    update=extend_schema(
        summary="Изменение существующего поста",
    ),
    destroy=extend_schema(
        description='Это вот, типо описание!',
    ),
    create=extend_schema(
        summary="Создание нового поста",
    ),
    retrieve=extend_schema(
        summary='Частичный возврат!'
    ),
)
class OperationModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    serializer_class = OperationSerializer
    queryset = models.Operations.objects.all()
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['date_time', 'typ', 'amount']
    search_fields = ['category__title', 'amount']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    @extend_schema(summary="Получить операцию", description="Возвращает все операции авторизированного пользоваетля.")
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user_id=self.request.user.id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @extend_schema(summary="Частичное получение", description="Возвращает определённый объект операции.")
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance)
        return Response(serializer.data, status=200)

    @extend_schema(summary="Удалить операцию", description="Удаляет определённую запись.")
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

    def create(self, request, *args, **kwargs):
        data = request.data
        category = data['category']
        cat_obj = Category.objects.filter(id=category, user_id=request.user)

        if cat_obj:
            serializer = self.serializer_class(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        else:
            raise rest_framework.exceptions.ValidationError('Выбрана некорректная категория!!!')


@extend_schema_view(

)
class UserAPIView(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh),
        }

        return Response(tokens, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args):
        user = request.user

        serializer = self.serializer_class(user)
        return Response(serializer.data, status=201)

    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True

        partial = kwargs.pop('partial', False)
        instance = User.objects.get(id=request.user.id)
        serializer = self.serializer_class(instance=instance, data=request.data, partial=partial)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        raise rest_framework.exceptions.NotFound("Ошибка изменения! Возможны некорректные данные!")

    def destroy(self, request, *args):
        pk = request.user.id

        instance = self.queryset.filter(id=pk)
        instance.delete()


@extend_schema_view(
    list=extend_schema(
        summary="Получить список категорий авторизированного пользователья",
    ),
    update=extend_schema(
        summary="Изменение существующкей категории",
    ),
    destroy=extend_schema(
        summary='Удаление определённой категории',
    ),
    create=extend_schema(
        summary="Добавление категории пользователья",
    ),
    retrieve=extend_schema(
        summary='Частичный возврат!'
    ),
)
class CategoryApiView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = models.Category.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication, SessionAuthentication]

    def get(self, request):
        queryset = self.queryset.filter(user_id=self.request.user.id)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def get_detail(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        if instance.user != request.user:
            raise rest_framework.exceptions.NotAcceptable('У вас нет доступа к этой записи!')

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return self.get(request)

    def delete(self, request, pk):
        super().destroy()
        instance = self.get_object()
        instance.delete()


def redirect_to_note(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/api/v1/note')
    else:
        return HttpResponseRedirect('/api/auth/login')


def login_access(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/api/v1/auth/login/')
    else:
        return HttpResponseRedirect('/api/v1/note/')


# def tokens_for_user(user):
#     refresh = RefreshToken.for_user(user)
#
#     return {
#         'refresh': str(refresh),
#         'access': str(refresh.access.token),
#     }
