from rest_framework import generics

from customer.models import CustomerRequest
from customer.serializers import CustomerRequestSerializer

from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from customer.permissions import OnlyOwnerCanUpdate


# 로그인하지 않으면 get요청만 가능, 로그인했다면 post도 가능
class CustomerRequestListView(generics.ListCreateAPIView):
    queryset = CustomerRequest.objects.all()
    serializer_class = CustomerRequestSerializer
    name = "customer-request-list"

    # 여기서 조금 헤맸다 serializer.save를 할때 onwer로써 request.user를 저장한다
    # 이제 serializer로 가서 owner로 .user의 내용물에 접근할 수 있다
    # serializer에서 owner.[내용물]을 필드에 담아서 리턴받을 수 있게된다
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # authentication_classes = [JWTAuthentication]
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerCanUpdate,
    )


class CustomerRequestListUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomerRequest.objects.all()
    serializer_class = CustomerRequestSerializer
    name = "request-list-patch"
    # lookup_field = 'slug' # 이걸지정하면 주소에서 파라미터로 받은것을 특정한 이름으로 받는다?

    # authentication_classes = [JWTAuthentication]
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        OnlyOwnerCanUpdate,
    )
    # 데이터베이스에 작성자의 정보가 들어있지 않다!
    # 커스터머 시리얼라이저 수정하기!
    # OnlyOwnerCanUpdate 수정하기! - 토큰의 유저와 작성글의 유저가 같은경우 수정기능 동작하게
    # admin:admin, admin2:admin2
