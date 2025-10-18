# Django의 forms 모듈을 불러옵니다.
# Django의 Form 클래스는 사용자 입력을 검증하고 HTML 폼 요소를 자동 생성하는 데 사용됩니다.
from django import forms


# 사용자가 역명을 입력할 수 있도록 하는 검색 폼입니다.
# Django의 Form 클래스를 상속받아 정의합니다.
class StationSearchForm(forms.Form):
    # CharField: 문자열 입력을 받는 기본 필드 타입입니다.
    # HTML에서는 <input type="text"> 요소로 렌더링됩니다.
    station = forms.CharField(
        # label: 폼 필드 이름 옆에 표시될 라벨(“역명”이라는 글자).
        label="역명",

        # widget: HTML 렌더링 시 사용할 위젯(입력창 형태)을 지정합니다.
        # 기본값은 TextInput이지만, attrs를 이용해 placeholder나 class 속성을 추가할 수 있습니다.
        widget=forms.TextInput(
            attrs={
                "placeholder": "예) 신도림",  # 입력창에 회색 힌트로 표시되는 문구
                "class": "input",            # CSS 스타일 적용을 위한 클래스명
            }
        )
    )
