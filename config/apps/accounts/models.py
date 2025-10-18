# Django ORM(Object Relational Mapper)의 기본 클래스인 models를 불러옵니다.
# models.Model을 상속하면 데이터베이스 테이블과 매핑되는 클래스를 만들 수 있습니다.
from django.db import models

# Django 기본 인증 시스템에서 제공하는 기본 User 모델을 불러옵니다.
# (username, password, email 등을 포함)
from django.contrib.auth.models import User


# 사용자(User) 모델과 1:1로 연결되는 Profile(프로필) 모델을 정의합니다.
# 사용자별로 추가 정보를 저장할 때 주로 이런 식으로 확장합니다.
class Profile(models.Model):
    # User 모델과 1:1 관계를 맺습니다.
    # on_delete=models.CASCADE → User가 삭제되면 해당 Profile도 함께 삭제됩니다.
    # related_name="profile" → User 인스턴스에서 profile 속성으로 접근 가능하도록 합니다.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")

    # 사용자가 자주 이용하는 지하철역 이름을 저장할 필드입니다.
    # 최대 길이 50자로 설정, blank=True는 폼 입력에서 비워도 저장 가능함을 의미합니다.
    default_station = models.CharField(max_length=50, blank=True)

    # 객체를 문자열로 표현할 때 호출되는 메서드입니다.
    # 예: Admin 페이지나 쉘에서 Profile 객체를 출력하면 “username profile” 형태로 보임.
    def __str__(self):
        return f"{self.user.username} profile"
