# Django의 AppConfig 클래스를 불러옵니다.
# AppConfig는 Django가 각 앱을 인식하고 설정(이름, 레이블 등)을 관리할 수 있도록 해주는 클래스입니다.
from django.apps import AppConfig


# Arrivals 앱의 설정을 정의하는 클래스입니다.
# 모든 Django 앱은 (명시적으로든 암묵적으로든) 하나의 AppConfig를 갖습니다.
class ArrivalsConfig(AppConfig):
    # default_auto_field:
    # Django 3.2 이후 버전에서는 모델의 기본 PK 필드를 BigAutoField로 지정하는 것이 권장됩니다.
    # 즉, models.py에서 primary key를 따로 지정하지 않으면 자동으로 BigAutoField가 사용됩니다.
    default_auto_field = "django.db.models.BigAutoField"

    # name:
    # Django가 이 앱을 식별할 수 있도록 하는 "앱의 전체 Python 경로"입니다.
    # 이 프로젝트에서는 apps.py가 "config/apps/arrivals" 아래에 있으므로 이렇게 지정됩니다.
    # (중요) settings.py의 INSTALLED_APPS에도 동일한 경로로 등록되어야 합니다.
    name = "config.apps.arrivals"
