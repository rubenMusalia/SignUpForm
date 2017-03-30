from rest_framework import generics
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import viewsets
from .serializers import (
    SnippetCreateSerializer,
    SnippetListSerializer,
    SnippetsDetailSerializer,
    SnippetSerializer,
    UserSerializer
    )
from rest_framework.decorators import detail_route
from ..models import Snippet
from django.shortcuts import get_object_or_404, redirect
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework import mixins
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
    )
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView


class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetListSerializer
   # permission_classes = AllowAny

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)  # A list of the snippets

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)  # An update of the snippet instance

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)  # Create an instance of the snippet

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)  # Delete the snippet


class SnippetCreateAPIView(generics.CreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetCreateSerializer


class SnippetListAPIView(generics.ListAPIView):
    filter_backends = [SearchFilter, OrderingFilter]
    queryset = Snippet.objects.all()
    serializer_class = SnippetListSerializer

    # permission_classes = AllowAny

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)  # A list of the snippets


# class SnippetDetailView(
#             generics.RetrieveUpdateDestroyAPIView,
#             # mixins.DestroyModelMixin,
#             # mixins.UpdateModelMixin,
#             # generics.RetrieveAPIView):
# ):
#     queryset = Snippet.objects.all()
#     serializer_class = SnippetsDetailSerializer
#     permission_classes = AllowAny,

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)
    #
    # def delete(self, request, *args, **kwargs):
    #     return self.delete(request, *args, **kwargs)


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailAPIView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'user': reverse('user-list', request=request, format=format),
        'snippets': reverse('snippet-list', request=request, format=format)
    })


class SnippetHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()
        return Response(snippet.highlighted)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = IsAuthenticatedOrReadOnly


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = IsAuthenticatedOrReadOnly


@detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
def highlight(self, request,*args,**kwargs):
    snippet = self.get_object()
    return Response(snippet.highlighted)


def perform_create(self, serializer):
    serializer.save(owner=self.request.user)


class SnippetDetailAPI2(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'api/profile_detail.html'

    def get(self, request, pk):
        snippet = get_object_or_404(Snippet, pk=pk)
        serializer = SnippetSerializer(snippet)
        return Response({'serializer': serializer, 'snippet': snippet})

    def post(self, request, pk):
        snippet = get_object_or_404(Snippet, pk=pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'snippet': snippet})
        serializer.save()
        return redirect('list')