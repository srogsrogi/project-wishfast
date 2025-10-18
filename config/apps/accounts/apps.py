# Django에서 앱 구성을 정의할 때 사용하는 기본 클래스 AppConfig를 불러옵니다.
# 각 앱의 이름(name), verbose_name, 기본 설정 등을 지정할 수 있습니다.
from django.apps import AppConfig


# Accounts 앱의 설정 정보를 정의하는 클래스입니다.
# Django는 이 클래스를 통해 'accounts' 앱을 인식하고 초기화합니다.
class AccountsConfig(AppConfig):
    # default_auto_field:
    # Django 3.2 이후부터 모델의 기본 PK(primary key) 필드 타입을 지정할 수 있습니다.
    # "BigAutoField"는 64비트 정수형 자동 증가 필드이며, 대규모 데이터베이스에 적합합니다.
    default_auto_field = "django.db.models.BigAutoField"

    # name:
    # Django가 이 앱을 내부적으로 식별할 때 사용하는 "전체 Python 경로"입니다.
    # 즉, settings.py의 INSTALLED_APPS에도 동일한 경로로 등록되어야 합니다.
    # (이 프로젝트는 apps 폴더 구조를 config 내부에 두고 있으므로 이렇게 지정됨)
    name = "config.apps.accounts"
