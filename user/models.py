from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)

"""
사용자 정보 정리)
관리자) 최고 관리자를 의미 - 서비스 운영자

이용자)
드론 방제전문집단) 업체
방제가 필요한 개인) 고객

업체)
1. 이메일
2. 주소
3. 업체이름
4. 전화번호

고객)
1. 이메일
2. 주소
3. 고객이름
4. 전화번호
"""


# 헬퍼 클래스
class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):

        # 주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError(("The password must be set"))

        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email=None, password=None, **extra_fields):

        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", 1)

        if extra_fields.get("role") != 1:
            raise ValueError("Superuser must have role of Global Admin")

        return self.create_user(email, password, **extra_fields)


# 현재 데이터베이스에 유저정보가 정수형으로 순차적으로 입력된다 - user_id?이건가?
# 유니크키값으로 바꾸기 - 겹치지 않는 고유값으로 수정하기
# AbstractBaseUser를 상속해서 유저 커스텀
class CustomUser(AbstractBaseUser, PermissionsMixin):

    ADMIN = 1
    MANAGER = 2
    DRONE_EXTERMINATOR = 3
    CUSTOMER = 4

    ROLE_CHOICES = (
        (ADMIN, "Admin"),
        (MANAGER, "Manager"),
        (DRONE_EXTERMINATOR, "Drone_exterminator"),
        (CUSTOMER, "Customer"),
    )

    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)
    name = models.CharField(max_length=50, blank=False, default="", unique=False)
    address = models.CharField(
        max_length=200, blank=True, default="", unique=False
    )  # 나중에 주소 형식같은 것을 적용하기
    call_number = models.CharField(
        max_length=20, blank=True, default="", unique=False
    )  # 나중에 전화번호 형식같은 것을 적용하기
    role = models.PositiveSmallIntegerField(
        choices=ROLE_CHOICES, blank=True, null=True, default=4
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # 사용자의 username field는 email으로 설정 (이메일로 로그인)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # 헬퍼 클래스 사용
    objects = CustomUserManager()

    def __str__(self):
        return self.email
