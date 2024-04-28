
# 이제보니까 request가 알아서 디코딩 되서 나온다!!!!
# 여기 파일은 무쓸모임 --------------------------
# 그래도 나중에 찾아볼 것을 대비해서 남겨두자

from rest_framework import permissions

import jwt
from dronefieldrestapi.settings import SIMPLE_JWT
from rest_framework_simplejwt.authentication import JWTAuthentication


class OnlyOwnerCanUpdate(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # getRawAccessToken = str(request.auth)

        # 토큰 decode를 안해도 보이네??
        # print(request.user.email)
        # print(request.user.role)
        # print(request.user.name)

        return obj.email == request.user.email

        # try:
        #     decodedToken = jwt.decode(
        #         getRawAccessToken,
        #         SIMPLE_JWT['SIGNING_KEY'],
        #         algorithms=[SIMPLE_JWT['ALGORITHM']],
        #     )

        #     # 등록된 이메일이 같다면 수정을 허용 - 나중에 user_id로 수정할까?
        #     return obj.email == decodedToken.get('email')

        # except:
        #     return False


# # 문제!) 왜 request에 user가 달려있는지, 왜 사용자 이메일 정보가 들어있는지 알수없다!
# # 나는 액세스토큰만을 받아서 정보를 중간에 노출하지않고 싶다! 그러면 request.user항목이 없어져야한다!
# # 나중에 천천히 알아보면서 삭제하기 -
# print(request.user)
# print(request.auth)
# print("----------------")
# print(request.body)
# print(request.headers.get("Authorization", None))
# # access = request.headers.get('Authorization', None)
# # payload = jwt.decode(access, SECRET_KEY, algorithms='HS256')
# # print(payload['email'])
# # 여기서부터 작업
# # 아래의 코드를 참고해서 이제부터 모든 콘텐츠를 액세스토큰을 사용해서 접근하게하고
# # 각 테이블?데이터?들을 액세스 토큰에 존재하는 정보를 사용하여 권한을 설정하면 된다!
# # 아래의 코드는 simplejwt에서 제공하는 클래스를 사용해서 access토큰을 해석해서
# # access 토큰에 있는 정보를 모두 가져왔다
# JWT_authenticator = JWTAuthentication()
# # authenitcate() verifies and decode the token
# # if token is invalid, it raises an exception and returns 401
# response = JWT_authenticator.authenticate(request)
# if response is not None:
#     # unpacking
#     user, token = response
#     print("this is decoded token claims", token.payload)
#     print("---------------------------")
#     print(token.payload.get("email"))
# else:
#     print("no token is provided in the header or the header is missing")
# return Response({}, status.HTTP_403_FORBIDDEN)


# 만약 그냥 일반 사용자 - GET, HEAD, OPTIONS 요청에만 True - 3개를 안전한 요청이라고 한다
# if request.method in permissions.SAFE_METHODS:
#     return True
# 만약 위의 3개중 하나가 아닌 경우 request.user가 obj.owner와 동일할때만 가능
# else:
#     return obj.email == request.email
# if obj.email == request.email:
#     return True
