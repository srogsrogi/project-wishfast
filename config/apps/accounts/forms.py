# Django의 forms 모듈을 불러옵니다.
# Django에서는 Form 클래스를 이용해 HTML 폼을 선언형 방식으로 정의하고,
# 입력값 검증 및 렌더링을 쉽게 처리할 수 있습니다.
from django import forms


# 사용자의 기본역(default_station)을 수정/입력받기 위한 폼입니다.
# Form 클래스를 상속받아 하나의 입력 필드를 정의합니다.
class ProfileForm(forms.Form):
    # CharField: 문자열 입력 필드 (HTML의 <input type="text"> 형태)
    # label: 화면에 표시될 입력란 이름
    # required=False → 비워도 검증 오류가 발생하지 않음 (선택 입력 가능)
    default_station = forms.CharField(label="기본역", required=False)
