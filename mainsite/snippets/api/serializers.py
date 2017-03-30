from rest_framework import serializers
from rest_framework.serializers import HyperlinkedIdentityField
from ..models import Snippet, LANGUAGE_CHOICES, STYLE_CHOICES
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    snippet = serializers.PrimaryKeyRelatedField(many=True, queryset=Snippet.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'snippets',)


class SnippetCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = "__all__"


detail_url = HyperlinkedIdentityField(
        view_name='snippets-api:detail',
        lookup_field='pk'
)


class SnippetListSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='snippets-api:detail', format='html')

    class Meta:
        model = Snippet
        fields = [
            'id', 'language', 'style', 'title', 'highlight', 'owner', 'code', 'url'
        ]

    url = detail_url

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SnippetsDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snippet
        fields = "__all__"


class SnippetSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')
    owner = serializers.ReadOnlyField(source='owner.username')

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.code = validated_data.get('code', instance.code)
        instance.linenos = validated_data.get('linenos', instance.linenos)
        instance.language = validated_data.get('language', instance.language)
        instance.style = validated_data.get('style', instance.style)
        instance.save()
        return instance


# class LoginSerializer(serializers.Serializer):
#     email = serializers.EmailField(
#         max_length=100,
#         style={'placeholder': 'Email', 'autofocus': True}
#     )
#     password = serializers.CharField(
#         max_length=100,
#         style={'input_type': 'password', 'placeholder': 'Password'}
#     )
#     rember_me = serializers.BooleanField()
