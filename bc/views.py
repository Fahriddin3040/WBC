import rest_framework.exceptions
from django.http import HttpResponseRedirect
from django.utils.decorators import classonlymethod
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, generics, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from . import models
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import OperationSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.views import SpectacularSwaggerView

@extend_schema_view(
    list=extend_schema(
        summary="Получить список постов",
    ),
    update=extend_schema(
        summary="Изменение существующего поста",
    ),
    partial_update=extend_schema(
        description='Это вот, типо описание!',
    ),
    create=extend_schema(
        summary="Создание нового поста",
    ),
)
class OperationModelViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication]
    serializer_class = OperationSerializer
    queryset = models.Operations.objects.all()

    @classmethod
    def as_view(cls, actions=None, **initkwargs):
        def view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return super(cls, cls).as_view(actions, **initkwargs)(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('/api/v1/auth/login')

        return view


    def auth_check(self, request):
        if request.user.is_authenticated:
            return 1
        else:
            return HttpResponseRedirect('/api/v1/auth/login')

    def user_check(self, data):
        if not self.request.user.is_authenticated:
            raise rest_framework.exceptions.NotFound("Пользователь не найден!")

        if data.user.id != self.request.user.id:
            raise rest_framework.exceptions.NotFound("Требуемый вами объект не найден!")

    def user_check_detail(self, instance):
        if not self.request.user.is_authenticated:
            raise rest_framework.exceptions.NotFound("Пользователь не найден!")

        if instance.user.id != self.request.user.id:
            raise rest_framework.exceptions.NotFound("Требуемый вами объект не найден!")

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.user_check_detail(instance)
        serializer = self.serializer_class(instance=instance)
        return Response(serializer.data, status=200)

    # def update(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     serializer = self.serializer_class(data=instance)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        self.user_check(request.data)
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=201)

    def list(self, request, *args, **kwargs):

        try:
            queryset = models.Operations.objects.filter(user_id=self.request.user.id)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except:
            raise rest_framework.exceptions.NotFound("Требуемый вами объект не найден!")


class UserAPIView(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]
    queryset = models.User.objects.all()
    serializer_class = UserSerializer

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        tokens = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

        return Response(tokens, status=status.HTTP_201_CREATED)


class SwaggerView(SpectacularSwaggerView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [SessionAuthentication]


def redirect_to_note(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/api/v1/note')
    else:
        return HttpResponseRedirect('/api/auth/login')
