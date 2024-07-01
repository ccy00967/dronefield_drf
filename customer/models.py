from django.db import models

# 드론으로 방제가 필요한 사람들
# 사용자의 정보 - 외부키로 가져옴
# 주소
# 요청내용
# 예약(방제를 원하는) 날짜
# 요청 생성날짜

class CustomerRequest(models.Model):
    owner = models.ForeignKey(
        'user.CustomUser',
        related_name = 'customerrequest',
        on_delete=models.CASCADE,
        # db_column="owner_id" # 이름지정 - 기본값은 owner_id, 나중에 email로 바꾸기
    )

    address = models.CharField(max_length=200, blank=False, default='')
    requestContent = models.CharField(max_length=200, blank=False, default='')
    reservationDate = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.name;