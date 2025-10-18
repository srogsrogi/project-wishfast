# Django의 BaseCommand 클래스를 가져옵니다.
# BaseCommand를 상속하면 manage.py에서 실행할 수 있는 커스텀 명령어를 만들 수 있습니다.
from django.core.management.base import BaseCommand

# Django 프로젝트 설정(settings.py)에 접근하기 위해 import
from django.conf import settings

# django.contrib.sites 앱에서 제공하는 Site 모델을 불러옵니다.
# 각 사이트의 도메인 정보를 관리하는 모델 (ex: localhost:8000, example.com)
from django.contrib.sites.models import Site

# allauth의 소셜 로그인(SocialApp) 모델을 불러옵니다.
# provider(구글, 카카오 등)와 client_id, secret 등을 저장하는 모델입니다.
from allauth.socialaccount.models import SocialApp

# OS 환경 변수에서 값들을 읽기 위해 os 모듈을 가져옵니다.
import os


# Django 커스텀 명령어 클래스 정의
# BaseCommand를 상속하여 handle() 메서드를 구현하면 명령어로 등록됩니다.
class Command(BaseCommand):
    # 명령어의 설명(help 텍스트) — manage.py help에서 표시됩니다.
    help = "Create/Update Google SocialApp and Site domain from env"

    # 실제 실행 로직
    def handle(self, *args, **kwargs):
        # 1) 환경변수에서 SITE_DOMAIN 값을 불러옵니다.
        # 설정되어 있지 않으면 기본값은 "localhost:8000"
        domain = os.getenv("SITE_DOMAIN", "localhost:8000")

        # 2️) 현재 SITE_ID에 해당하는 Site 객체를 가져오거나 없으면 생성합니다.
        # settings.SITE_ID가 없으면 기본값 1을 사용.
        site, _ = Site.objects.get_or_create(id=getattr(settings, "SITE_ID", 1))

        # Site 객체의 도메인(domain)과 이름(name)을 환경변수 값으로 업데이트
        site.domain = domain
        site.name = domain
        site.save()

        # 콘솔에 성공 메시지를 출력
        self.stdout.write(self.style.SUCCESS(f"[Site] {site.domain}"))

        # 3️) Google OAuth 클라이언트 ID/Secret을 환경변수에서 읽습니다.
        client_id = os.getenv("GOOGLE_CLIENT_ID")
        secret = os.getenv("GOOGLE_CLIENT_SECRET")

        # 둘 중 하나라도 없으면 경고 메시지를 띄우고 종료
        if not client_id or not secret:
            self.stdout.write(self.style.WARNING("GOOGLE_CLIENT_* not set"))
            return

        # 4) Google용 SocialApp을 가져오거나 없으면 새로 생성합니다.
        # provider="google"로 식별, name="Google"로 표시
        app, _ = SocialApp.objects.get_or_create(provider="google", name="Google")

        # 환경변수에서 읽은 값으로 client_id/secret 갱신
        app.client_id = client_id
        app.secret = secret
        app.save()

        # 5️) 이 SocialApp을 현재 Site에 연결 (ManyToMany 관계)
        app.sites.set([site])

        # 콘솔에 성공 메시지 출력
        self.stdout.write(self.style.SUCCESS("[SocialApp] Google configured"))
