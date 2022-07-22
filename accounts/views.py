from rest_framework import viewsets, status
from rest_framework.response import Response

from accounts.tasks import email_to_user
from accounts.utils import custom_error_response
from accounts.models import CustomUser
from accounts.serializers import EditUserSerializer, UserSerializer, CreateUserSerializer


class UserView(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', 'put', 'delete',)
    serializer_class = CreateUserSerializer
    queryset = CustomUser

    def get_serializer_class(self):
        if self.action == 'update':
            self.serializer_class = EditUserSerializer
        else:
            self.serializer_class = CreateUserSerializer
        return self.serializer_class

    def get_queryset(self):
        queryset = self.queryset.objects.all()
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Function to create user
        :param request: wsgi request
        :return: return response for HTTP_201_CREATED or HTTP_BAD_REQUEST
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Call method for email send
            email = request.data['email']
            to_list = [email]
            email_to_user(to_list)
            return Response(status=status.HTTP_201_CREATED, data=serializer.data)
        return custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=serializer.errors)

    def list(self, request, *args, **kwargs):

        """
        Function to list all users
        :param request: wsgi request
        :return: All the Registered Users
        """
        self.serializer_class = UserSerializer
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(data=serializer.data)

    def update(self, request, *args, **kwargs):
        """
        Function to create user
        :param request: wsgi request
        :return: update user on the basis of id
        """
        obj = self.get_object()
        self.serializer_class = EditUserSerializer
        serializer = self.serializer_class(obj, data=request.data, context={'id': obj.id})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data=serializer.data)
        return custom_error_response(status=status.HTTP_400_BAD_REQUEST, detail=serializer.errors)

    def retrieve(self, request, *args, **kwargs):
        """
        Function to retrieve user
        :param request: wsgi request
        :return: return retrieved data or response for HTTP_BAD_REQUEST
        """
        obj = self.get_object()
        serializer = UserSerializer(obj)
        return Response(data=serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Function to destroy user
        :param request: wsgi request
        :return: return response for HTTP_201_OK or HTTP_BAD_REQUEST
        """
        user_id = self.kwargs['pk']
        obj_del = self.queryset.objects.filter(id=user_id)
        if obj_del:
            obj_del.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
