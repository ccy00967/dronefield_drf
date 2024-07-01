from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserListSerializer,
    CustomTokenObtainPairSerializer,
)

from user.permissions import OnlyOwnerCanUpdate


# 지금 permission을 따로 파일을 만들었다 do not repeat yourself (DRY) 실천해보기, def post 함수 수정해보기


# 토큰2개를 발급한다 - 안쓸것 같으니까 나중에 주석처리하기
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# 유저 회원가입 처리 - 이메일, 비밀번호 사용
class UserRegistrationView(generics.GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            serializer.save() # 데이터베이스에 유저정보 저장
            status_code = status.HTTP_201_CREATED

            response = {
                "success": True,
                "statusCode": status_code,
                "message": "User successfully registered!",
                #"user": serializer.data, # 패스워드까지 노출된다, 아래로그인 참고해서(.data[]형식) 바꾸기
                "user" : {
                    "eamil" : serializer.data["email"],
                    "name" : serializer.data["name"],
                }
            }

            return Response(response, status=status_code)


# 이메일과 비밀번호로 로그인
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        valid = serializer.is_valid(raise_exception=True)

        if valid:
            status_code = status.HTTP_200_OK

            # 유저로그인시리얼라이저의 validation 참고해서 작성
            response = {
                "success": True,
                "statusCode": status_code,
                "message": "User logged in successfully",
                "access": serializer.data["access"],
                "refresh": serializer.data["refresh"],
                "authenticatedUser": {
                    "email": serializer.data["email"],
                    "role": serializer.data["role"],
                },
            }

            return Response(response, status=status_code)
        
# refresh 토큰으로 로그인하는 로직 만들기 - 브라우저에 저장된 쿠키의 refresh를 사용해서 로그인
# 이전에 로그인한 사람을 알아보고 자동으로 로그인 할 수 있음 - 매우 편리 
# 위의 로그인 성공시 프론트에서 토큰을 저장할지, 백에서 저장을 요구할지 결정하기 - 백에서도 명령이 되나??


# 여기는 나중에 유저가 자신의 정보를 수정하거나
# 어드민이 유저들의 정보를 수정하는 코드로 바꾸기
# 방제사 등록을 하려면 어드민이 직접 role을 수정하는 방식 구현
class UserListView(generics.GenericAPIView):
    serializer_class = UserListSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user.role != 1:
            response = {
                "success": False,
                "status_code": status.HTTP_403_FORBIDDEN,
                "message": "You are not authorized to perform this action",
            }
            return Response(response, status.HTTP_403_FORBIDDEN)
        else:
            users = CustomUser.objects.all()
            serializer = self.serializer_class(users, many=True)
            response = {
                "success": True,
                "status_code": status.HTTP_200_OK,
                "message": "Successfully fetched users",
                "users": serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)


# 사용자 정보를 수정 - 오직 자기자신의 정보만 수정가능 - access토큰으로 인증
class UserDataUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserListSerializer
    name = "userinfo"

    permission_classes = (
        IsAuthenticated,
        OnlyOwnerCanUpdate,
    )

    # 중요!
    # 토큰을 입력받으면 자동으로 디코딩되어 request에 담기는 것 같다
    # 결론) 뷰에는 queryset으로 데이터를 가져오고
    # 보여질 데이터는 시리얼라이저에서 제한하기
    # 퍼미션스파일에 여러가지 퍼미션을 만들어서 유져용, 어드민용을 만들기!
    # 즉, 뷰파일을 깔끔하게 유지하고 로직들을 전부 퍼미션 파일로 옮긴다
