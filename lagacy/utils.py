from datetime import datetime
# sols to earth date

from datetime import datetime, timedelta


def sols_to_earth_date(sol, landing_date_str="2018-11-26"):
    """
    화성 시간(sol)을 지구 날짜로 변환.

    Parameters:
    - sol (int): 화성 일수
    - landing_date_str (str): 착륙 날짜 (YYYY-MM-DD 형식)

    Returns:
    - datetime: 변환된 지구 날짜
    """
    # 화성의 1 sol은 약 24시간 39분 35.244초로, 지구 일수로는 약 1.02749125일입니다.
    mars_sol_in_earth_days = 1.02749125

    # 착륙 날짜를 datetime 객체로 변환
    landing_date = datetime.strptime(landing_date_str, "%Y-%m-%d")

    # 총 지구 일수 계산
    total_earth_days = sol * mars_sol_in_earth_days

    # 착륙 날짜에 총 지구 일수를 더함
    earth_date = landing_date + timedelta(days=total_earth_days)

    return earth_date
