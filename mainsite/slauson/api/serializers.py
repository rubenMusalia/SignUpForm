from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.serializers import (
    HyperlinkedIdentityField,
    SerializerMethodField,
    EmailField,
    CharField,
    ValidationError
    )
from ..models import Profile
from django.db.models import Q


class ProfileCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"


#  This works just like the get_absolute_url in views (return reverse)

detail_url = HyperlinkedIdentityField(
        view_name='slauson-api:detail',
        lookup_field='pk'
    )
# delete_url = HyperlinkedIdentityField(
#         view_name='slauson-api:delete',
#         lookup_field='pk'
#     )


class ProfileListSerializer(serializers.ModelSerializer):
    url = detail_url
    user = SerializerMethodField()

    class Meta:
        model = Profile
        fields = [
            'id',
            'user',
            # 'location',
            # 'bio',
            'birth_date',
            'url',
        ]

    def get_user(self, obj):
        return str(obj.user.username)


class ProfileDetailSerializer(serializers.ModelSerializer):
    user = SerializerMethodField(read_only=True)
    image = SerializerMethodField

    class Meta:
        model = Profile
        fields = [
            'pk',
            'user',
            'bio',
            'location',
            'birth_date',
            #'image'
        ]

    def get_user(self, obj):
            return str(obj.user.username)

    # Gets the url field for the image SerializedMethodField above
    # def get_image(self, obj):
    #     try:
    #         image = obj.image.url
    #     except:
    #         image = None
    #     return image


# class ProfileDeleteSerializer(serializers.ModelSerializer):
#     url = delete_url
#
#     class Meta:
#         model = Profile
#         fields = [
#             'url'
#         ]

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    email = EmailField(label='Email Address')
    email2 = EmailField(label='Confirm Email')

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'email2'
        ]
        extra_kwargs = {"password": {"write_only": True}
                        }

    # this method is a validation method for both email fields(not necessary on both ends
    # but it shows which one doesnt't match the other)
    def validate_email(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        email2 = value

        user_qs = User.objects.filter(email=email2)
        if user_qs.exists():
            # query's the db to ensure that the email address being provided hasn't been registered by another user
            raise ValidationError("The email provided has already been registered by another user")
        if email1 != email2:
            raise ValidationError("Both Email fields MUST match")
        return value

    # validation for email2
    def validate_email2(self, value):
        data = self.get_initial()
        email1 = data.get('email')
        email2 = value
        if email1 != email2:
            raise ValidationError("Both Email fields MUST match")
        return value

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        email = validated_data['email']

        user_obj = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        user_obj.set_password(password)
        user_obj.save()
        return validated_data


class UserLoginSerializer(serializers.ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    email = EmailField(required=False, allow_blank=True, label='Email Address')
    username = CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'email',
            'token'
        ]
        extra_kwargs = {"password": {"write_only": True}
                        }

    def validate(self, data):
        user_obj = None
        email = data.get("email", None)
        username = data.get("username", None)
        password = data["password"]
        if not email and not username:
            raise ValidationError("A username or email is required")
        # queryset search to make sure username/email is a user model 7 it's distinct(only one object in the queryset)

        user = User.objects.filter(
                Q(email=email) |
                Q(username=username)
            ).distinct()
        user = user.exclude(email__isnull=True).exclude(email__iexact='')
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not valid")
            # checks the password against the user object
        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect password,please try again")
        return data


# class UserDetailSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [
#             'username',
#             'first_name',
#             'last_name',
#         ]
