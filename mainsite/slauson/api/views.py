from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework import authentication, permissions
from rest_framework.permissions import (
    AllowAny,
    IsAdminUser,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    )
from rest_framework import viewsets
from ..models import Profile
from .serializers import (
    ProfileListSerializer,
    ProfileDetailSerializer,
    ProfileCreateSerializer,
    CreateUserSerializer,
    UserLoginSerializer,
    )

from .permissions import IsOwnerOrReadOnly
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
    )
from .pagination import ProfileLimitOffsetPagination, ProfileNumberPagination


class ProfileCreateAPIView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileCreateSerializer
    # permission_classes = [IsAuthenticated, IsAdminUser]


class ProfileListAPIView(generics.ListAPIView):
    serializer_class = ProfileListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['location', 'bio', 'birth_date',]
    queryset = Profile.objects.all()
    permission_classes = [AllowAny]
    pagination_class = ProfileNumberPagination  # ProfileLimitOffsetPagination
                                                #  LimitOffsetPagination , PageNumberPagination

    # this here overrides the default queryset method
    def get_queryset(self, *args, **kwargs):
        queryset_list = Profile.objects.all() # filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query:
            queryset_list = queryset_list.filter(
                # Q(user_first_name_icontains=query) |
                # Q(user_last_name_icontains=query) |
                Q(location_icontains=query) |
                Q(bio_icontains=query)
            ).ditinct()
        return queryset_list


# class ProfileUpdateAPIView(generics.RetrieveUpdateAPIView):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileDetailSerializer
#     permission_classes = [
#         # IsAuthenticatedOrReadOnly,
#         IsOwnerOrReadOnly
#                          ]


class ProfileDeleteView(generics.DestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileListSerializer
    lookup_field = 'pk'
    permission_classes = [
        IsAdminUser,
    ]


class ProfileDetailAPIView(
        mixins.UpdateModelMixin,
        generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileDetailSerializer
    permission_classes = IsAuthenticatedOrReadOnly, #IsOwnerOrReadOnly
    # lookup_field = 'slug'

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

# class ListUsers(APIView):
#     # View that lists all the users in the system
#     # Requires authentication
#     # Only the admin is able to access this view
#     authentication_classes = authentication.TokenAuthentication
#     permission_classes = (permissions.IsAdminUser,)
#
#     def get(self, request, format=None):
#         # Returns a list of the users
#         usernames = [user.username for user in User.objects.all()]
#         return Response(usernames)


class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = AllowAny,


class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args,**kwargs):
        data = request.data  # data that's coming through the login view
        serializer = UserLoginSerializer(data=data)  # running the data through the serializer
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.data
            return Response(new_data, status=HTTP_200_OK)  # the new_data passed through is valid if NOT next step
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)  # throws the error

