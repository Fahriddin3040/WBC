import rest_framework.exceptions
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from . import models
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import OperationSerializer, UserSerializer, CategorySerializer
from rest_framework.permissions import IsAuthenticated


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
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['date_time', 'typ', 'amount']
    search_fields = ['category__title', 'amount']

    @classmethod
    def as_view(cls, actions=None, **initkwargs):
        def view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return super(cls, cls).as_view(actions, **initkwargs)(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('/api/v1/auth/login')

        return view

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance=instance)
        return Response(serializer.data, status=200)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()

    @csrf_exempt
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data, status=201)



class UserAPIView(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer

    # @csrf_exempt
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

    def update(self, request, *args):
        user = request.user

        serializer = self.serializer_class(instance=user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

        raise rest_framework.exceptions.NotFound("Ошибка изменения! Возможны некорректные данные!")

    def destroy(self, request, *args):
        pk = request.user.id

        instance = self.queryset.filter(id=pk)
        instance.delete()




class CategoryApiView(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = models.Category.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    @classmethod
    def as_view(cls, actions=None, **initkwargs):
        def view(request, *args, **kwargs):
            if request.user.is_authenticated:
                return super(cls, cls).as_view(actions, **initkwargs)(request, *args, **kwargs)
            else:
                return HttpResponseRedirect('/api/v1/auth/login')

        return view

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

    # def get_detail(self, request):
    #     instance = self.get_object()
    #     self.user_check(instance)
    #     serializer = self.serializer_class(instance)
    #     return Response(serializer.data)

    def delete(self, request):
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
