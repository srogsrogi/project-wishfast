# Django의 단축 함수(shortcuts) 불러오기
# render: 템플릿을 HTML로 렌더링해 반환
# redirect: 다른 URL로 리다이렉트할 때 사용
from django.shortcuts import render, redirect

# 로그인 여부를 검사하는 데코레이터 (현재 이 파일에서는 사용되지 않지만 import됨)
# 특정 뷰를 로그인 사용자만 접근하도록 제한할 때 사용합니다.
from django.contrib.auth.decorators import login_required

# 같은 앱 내의 forms.py에서 StationSearchForm을 가져옵니다.
from .forms import StationSearchForm

# 같은 앱 내의 services.py에서 실시간 도착 정보 API 호출 함수를 가져옵니다.
from .services import fetch_realtime_arrivals_by_station


# 메인 페이지(index): 역 검색 폼을 표시하는 역할
def index(request):
    # GET 파라미터를 이용해 폼 인스턴스를 생성합니다.
    # request.GET이 비어 있으면 None을 전달 → 빈 폼이 생성됩니다.
    form = StationSearchForm(request.GET or None)

    # 로그인한 사용자라면 기본역(default_station)을 자동으로 폼에 채워주는 로직입니다.
    if request.user.is_authenticated and not form.is_bound:
        # getattr를 중첩 사용하여 안전하게 접근:
        # request.user.profile이 없으면 None 반환 → AttributeError 방지.
        default_station = getattr(
            getattr(request.user, "profile", None),
            "default_station",
            ""
        )

        # 사용자의 프로필에 기본역이 설정되어 있다면 폼 초기값으로 지정
        if default_station:
            form = StationSearchForm(initial={"station": default_station})

    # arrivals/index.html 템플릿을 렌더링하면서 폼 객체를 전달
    return render(request, "arrivals/index.html", {"form": form})


# 실시간 도착 정보를 조회하는 페이지
def arrival_info(request):
    # GET 요청인 경우만 처리
    if request.method == "GET":
        # GET 파라미터로 전달된 데이터를 폼에 바인딩
        form = StationSearchForm(request.GET)

        # 폼이 유효한 경우 (입력 검증 통과)
        if form.is_valid():
            # 사용자가 입력한 역명 꺼내기
            station = form.cleaned_data["station"]

            # 서비스 레이어에서 실시간 도착 정보 요청
            result = fetch_realtime_arrivals_by_station(station)

            # 도착 정보 결과를 arrival_info.html 템플릿으로 전달하여 렌더링
            return render(
                request,
                "arrivals/arrival_info.html",
                {"result": result, "station": station},
            )

    # 폼이 유효하지 않거나 GET 요청이 아닐 경우 index 페이지로 리다이렉트
    return redirect("arrivals:index")
