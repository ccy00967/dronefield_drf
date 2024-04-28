from .models import CustomUser
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

# from rest_framework_simplejwt.tokens import RefreshToken, AuthUser


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# 토큰에 원하는 정보 담기
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["email"] = user.email
        token["name"] = user.name
        # ...

        return token


# 유저 가입을 담당하는 코드 - DB에 회원가입한 유저를 저장한다
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "name",
            "password",
        )

    def create(self, validated_data):
        auth_user = CustomUser.objects.create_user(**validated_data)
        return auth_user


# 유저의 로그인을 담당하는 코드 - 위의 커스텀토큰시리얼라이저와 연계
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128, write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)

    def create(self, validated_date):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, data):
        email = data["email"]
        password = data["password"]

        # 위의 값을 이용해서 유저정보를 찾음, 유저 객체를 반환받음
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid login credentials")

        try:
            # refresh = RefreshToken.for_user(user)
            refresh = CustomTokenObtainPairSerializer.get_token(user)
            refresh_token = str(refresh)
            access_token = str(refresh.access_token)

            update_last_login(None, user)

            # view에 넘길 데이터들
            validation = {
                "access": access_token,
                "refresh": refresh_token,
                "email": user.email,
                "role": user.role,
            }

            return validation
        except CustomUser.DoesNotExist:
            raise serializers.ValidationError("Invalid login credentials")
        # 위의 try catch문이 필요없어 보인다. 나중에 더 공부해서 지우던지 하자
        # 중복인 이유:User.DoesNotExist가 try문의 어디서 발생하는지 모름


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "email",
            "name",
            "address",
            "call_number",
        )
