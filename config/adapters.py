from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings


class MyAccountAdapter(DefaultAccountAdapter):
    """
    기본 allauth Account 어댑터를 상속하여 커스터마이징합니다.
    예: 이메일/패스워드 방식의 회원가입 허용 여부 제어
    """

    def is_open_for_signup(self, request):
        """
        사이트의 회원가입 가능 여부를 결정합니다.
        False를 반환하면 이메일/패스워드를 통한 신규 회원가입이 비활성화됩니다.
        (소셜 로그인만 허용하고 싶을 때 유용합니다.)
        """
        return True


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    기본 allauth SocialAccount 어댑터를 상속하여 커스터마이징합니다.
    예: 소셜 로그인 시 신규 회원가입 허용 여부 제어
    """

    def is_open_for_signup(self, request, sociallogin):
        """소셜 계정을 통해 신규 사용자를 생성할 수 있는지 여부를 제어합니다."""
        return True