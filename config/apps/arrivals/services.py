# 운영체제 환경 변수 접근을 위한 os 모듈과
# HTTP 요청을 보낼 requests 라이브러리를 가져옵니다.
import os, requests

# urllib.parse의 quote 함수는 URL 인코딩(특수문자 → %형식)을 위해 사용됩니다.
# 예: "신도림" → "%EC%8B%A0%EB%8F%84%EB%A6%BC"
from urllib.parse import quote


# 환경변수에서 서울 열린데이터포털의 지하철 실시간 도착정보 API 키를 불러옵니다.
# 환경변수 이름: SEOUL_SUBWAY_API_KEY
# 키가 설정되지 않았으면 기본값은 빈 문자열("")입니다.
SEOUL_API_KEY = os.getenv("SEOUL_SUBWAY_API_KEY", "")


# 특정 역(station_name)의 실시간 열차 도착 정보를 가져오는 함수입니다.
# 반환형은 dict (파이썬 딕셔너리)입니다.
def fetch_realtime_arrivals_by_station(station_name: str) -> dict:
    """
    서울교통공사/서울열린데이터포털 실시간 도착 정보 API 예시.

    실제 서비스에서는 API 명세에 맞게 endpoint(요청 URL)나 key를 수정해야 합니다.
    여기서는 단순히 '역명' 단위로 요청을 보내고,
    응답 데이터를 '호선/상·하행' 단위로 묶어주는 예시 구조입니다.
    """

    # API 키가 없으면 바로 오류 메시지를 반환합니다.
    if not SEOUL_API_KEY:
        return {"error": "SEOUL_SUBWAY_API_KEY missing"}

    # API 호출용 URL 구성
    # (예시) http://swopenapi.seoul.go.kr/api/subway/<인증키>/json/realtimeStationArrival/0/100/<역명>
    # 역명은 한글이므로 quote()로 URL 인코딩 처리합니다.
    url = f"http://swopenapi.seoul.go.kr/api/subway/{SEOUL_API_KEY}/json/realtimeStationArrival/0/100/{quote(station_name)}"

    # API 요청을 보냅니다. (타임아웃 5초)
    resp = requests.get(url, timeout=5)

    # 응답을 JSON 형태로 파싱합니다.
    data = resp.json()


    # 도착 정보 목록을 담을 리스트 생성
    arrivals = []

    # JSON 데이터 중 'realtimeArrivalList' 키에 해당하는 리스트를 순회
    # → 각 열차의 도착 정보를 추출
    for row in data.get("realtimeArrivalList", []):
        arrivals.append({
            "line": row.get("subwayId"),       # 지하철 노선 ID (예: 1001=1호선, 1002=2호선 등)
            "updnLine": row.get("updnLine"),   # 상행/하행 여부
            "trainLineNm": row.get("trainLineNm"),  # 열차 방면 또는 도착지 설명
            "arvlMsg2": row.get("arvlMsg2"),   # 도착 메시지 (예: "곧 도착", "○○행 ○○출발")
            "barvlDt": row.get("barvlDt"),     # 도착 예정 시간(초 단위)
        })


    # 라인(노선)과 방향(상행/하행)을 묶어서 그룹화할 딕셔너리 생성
    grouped = {}

    for a in arrivals:
        # key = (호선 ID, 상행/하행)
        key = (a["line"], a["updnLine"])

        # grouped에 동일한 키가 없으면 새 리스트 생성, 있으면 append
        grouped.setdefault(key, []).append(a)

    # 최종 반환 구조: {"station": 역명, "groups": {(line, updnLine): [도착리스트...]}}
    return {"station": station_name, "groups": grouped}
