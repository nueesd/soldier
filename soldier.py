import streamlit as st
import random

def init_session_state():
    if 'survival_score' not in st.session_state:
        st.session_state.survival_score = 8000  # 생존 점수 초기값
    if 'current_scenario' not in st.session_state:
        st.session_state.current_scenario = 0
    if 'game_over' not in st.session_state:
        st.session_state.game_over = False
    if 'history' not in st.session_state:
        st.session_state.history = []

def get_scenario(scenario_num):
    scenarios = [
        {
            "title": "전쟁 발발",
            "image": "전쟁발발.jpg",
            "description": "1950년 6월 25일, 북한군이 남침했습니다. 국군 병사로서 첫 임무를 수행해야 합니다. 어떻게 하시겠습니까?",
            "choices": {
                "부대에 합류한다": {"score": 1000, "message": "부대와 함께 방어선을 구축했습니다."},
                "상관에게 보고한다": {"score": 1000, "message": "상관에게 보고하여 명령을 받았습니다."},
                "가족을 보호하러 간다": {"score": -3000, "message": "집으로 가다 상관에게 걸렸습니다. 가족은 중요하지만 나라를 위한 임무를 수행해야 합니다."},
                "혼란 속에 대기한다": {"score": -1000, "message": "혼란 속에서 시간을 낭비했습니다."}
            }
        },
        {
            "title": "서울 방어",
            "image": "서울함락.jpg",
            "description": "전쟁이 시작되고 사흘 뒤, 서울이 함락 위기에 처했습니다. 어떻게 하시겠습니까?",
            "choices": {
                "적과 맞서 싸운다": {"score": -3000, "message": "용감하게 싸워 방어에 기여했으나 서울을 빼앗겼습니다."},
                "후퇴하여 재정비한다": {"score": -2000, "message": "전력을 보존하여 후방에서 재정비했습니다."},
                "지원군을 요청한다": {"score": -3000, "message": "지원군 요청이 지연되었고 북한군에게 서울을 빼앗겼습니다."},
                "무기를 버리고 도망친다": {"score": -10000, "message": "도망치다 북한군에 의해 죽음을 맞이했습니다."}
            }
        },
        {
            "title": "미군 참전",
            "image": "미군참전.jpg",
            "description": "1950년 7월 1일, 미 지상군 선발대가 부산에 도착했습니다. 어떻게 미군과 협력하시겠습니까?",
            "choices": {
                "미군과 합동 작전을 계획한다": {"score": 1000, "message": "효율적인 협력으로 전력을 강화했습니다."},
                "정보를 제공한다": {"score": 1000, "message": "유용한 정보를 제공하여 전투에 기여했습니다."},
                "명령 없이 독단적으로 행동한다": {"score": -3000, "message": "혼란을 초래하여 작전에 차질이 생겼습니다."},
                "협력을 거부한다": {"score": -1000, "message": "미군과의 협력이 실패했습니다."}
            }
        },
        {
            "title": "낙동강 방어선",
            "image": "낙동강방어선.jpg",
            "description": "낙동강 방어선이 마지막 방어선입니다. 어떤 전략을 선택하시겠습니까?",
            "choices": {
                "방어선을 강화한다": {"score": 1000, "message": "방어선을 강화하여 적의 진격을 막았습니다."},
                "유엔군과 협력한다": {"score": 2000, "message": "유엔군과 협력하여 방어를 성공적으로 수행했습니다."},
                "정찰 임무를 게을리 한다. ": {"score" : -5000,"message":"적 움직임 파악에 실패하여 방어선이 뚫렸습니다."},
                "부산에 가족이 피난했다는 소식을 듣고 몰래 도망간다": {"score": -1000,"message": "도망가기 직전, 북한군의 공격으로 실패했습니다."}
                }
        },
        {
            "title": "인천상륙작전",
            "image": "인천상륙작전.jpg",
            "description": "1950년 9월 15일, 인천상륙작전이 성공했습니다. 서울을 되찾기 위한 다음 계획은 무엇입니까?",
            "choices": {
                "서울로 진격한다": {"score": 2000, "message": "서울로 진격하여 도시를 탈환했습니다."},
                "부대 재정비 후 진격한다": {"score": 1000, "message": "재정비 후 안전하게 진격했습니다."},
                "적의 반격을 무시하고 무리하게 진격한다": {"score": -1000, "message": "무리한 진격으로 병력 손실이 발생했습니다."},
                "작전을 지연시켜 기회를 놓친다": {"score": -2000, "message": "작전 지연으로 적이 방어를 강화했습니다."}
            }
        },
        {
            "title": "평양 탈환",
            "image": "평양탈환.jpg",
            "description": "1950년 10월, 평양을 탈환할 기회가 왔습니다. 어떻게 하시겠습니까?",
            "choices": {
                "신속하게 진격하여 탈환한다": {"score": 2000, "message": "10월 19일 평양을 성공적으로 탈환했습니다."},
                "포위 작전을 펼친다": {"score": 1000, "message": "포위 작전으로 적을 제압하여 10월 19일 평양을 성공적으로 탈환했습니다."},
                "무리하게 진격한다": {"score": -2000, "message": "병력이 크게 손실되었습니다."},
                "적의 방어를 과소평가하고 실패한다": {"score": -3000, "message": "적의 방어를 과소평가하여 작전이 실패했습니다."}
            }
        },
        {
    "title": "중공군 참전",
    "image": "중공군.jpg",
    "description": "1950년 10월 25일, 중공군이 참전했습니다. 어떻게 대처하시겠습니까?",
    "choices": {
        "방어선을 재정비하고 대비한다": {"score": -2000, "message": "방어선을 재정비했지만, 중공군의 강력한 공세로 어려움을 겪었습니다."},
        "유엔군과 협력하여 대응한다": {"score": -2000, "message": "유엔군과 협력했으나, 중공군의 압도적인 숫자에 밀렸습니다."},
        "혼란에 빠져 지휘 체계 붕괴된다": {"score": -2000, "message": "지휘 체계가 붕괴되어 큰 혼란이 발생했습니다."},
        "후방으로 철수하며 병력을 재정비한다": {"score": -2000, "message": "병력을 보존하며 철수했지만, 전력 손실은 피할 수 없었습니다."},
            }
        },
        {
            "title": "1·4 후퇴",
            "image": "14후퇴.jpg",
            "description": "1951년 1월 4일, 서울이 다시 함락되었습니다. 한겨울에 후퇴 작전을 수행해야 합니다. 어떻게 하시겠습니까?",
            "choices": {
                "질서 있게 후퇴하며 방어선을 구축한다": {"score": -1000, "message": "질서 있게 후퇴했지만, 방어선 구축에 어려움을 겪었습니다."},
                "유엔군과 협력하여 후방으로 이동한다": {"score": -500, "message": "유엔군과 협력했으나, 후방 이동 중 큰 손실이 있었습니다."},
                "혼란 속에 무질서하게 후퇴한다": {"score": -2000, "message": "혼란 속에서 무질서하게 후퇴하여 병력이 크게 분산되었습니다."},
                "장비를 포기하고 급히 철수한다": {"score": -2000, "message": "장비를 포기하고 급히 철수하여 전력 손실이 발생했습니다."}
            }
        },
        {
            "title": "서울 재탈환",
            "image": "서울재탈환.jpg",
            "description": "서울을 다시 탈환할 기회가 왔습니다. 어떻게 하시겠습니까?",
            "choices": {
                "전면 공격으로 탈환 시도한다": {"score": 2000, "message": "서울을 성공적으로 탈환했습니다."},
                "포위 작전으로 안전하게 접근한다": {"score": 1500, "message": "포위 작전으로 적을 효과적으로 제압했습니다."},
                "정찰을 강화한 뒤 신중히 진격한다": {"score": 1200, "message": "정찰을 강화하여 적의 방어를 무력화하고 진격에 성공했습니다."},
                "유엔군과 협력하여 공동 작전을 펼친다": {"score": 1800, "message": "유엔군과 협력하여 공동 작전으로 서울을 탈환했습니다."}
            }
        },
        {
            "title": "고지전과 정전 협정(휴전협정)",
            "image": "고지전.jpg",
            "description": "1953년 7월 27일 오전 10시 정전 협정이 서명되었습니다. 하지만 정전 협정은 12시간 후인 오후 10시부터 효과가 있습니다. 고지전을 통해 유리한 고지를 점령하려 합니다. 어떻게 하시겠습니까?",
            "choices": {
                "휴전이 되었으니 고향으로 돌아간다": {"score": -2000, "message": "아직 휴전이 되려면 몇 시간 남았습니다. 병력이 부족하여 국군이 밀리고 있습니다."},
                "또다시 일어날 수 있는 전쟁을 대비해 병력을 보존한다": {"score": -1000, "message": "아직 휴전이 되지 않았습니다. 지금은 병력을 보존할 때가 아닙니다."},
                "휴전 협정과 관련없이 무리하게 공격한다": {"score": -2000, "message": "무리한 공격으로 병력 손실이 발생했습니다."},
                "고지를 점령하여 유리한 위치를 확보하고자 한다": {"score" : -1000,"message":"고지를 점령하였습니다만.. 곧바로 빼앗겼습니다."}
            }
        }
    ]

    return scenarios[scenario_num] if scenario_num < len(scenarios) else None

def show_game():
    st.title("6.25 전쟁 국군 생존기")
    
    # 현재 생존 점수 표시
    st.sidebar.metric("생존 점수", st.session_state.survival_score)
    
    # 게임 오버 체크
    if st.session_state.survival_score <= 0:
        st.session_state.game_over = True
    
    if st.session_state.game_over:
        st.error("게임 오버! 생존에 실패했습니다.")
        if st.button("다시 시작"):
            st.session_state.clear()
            st.rerun()
        return

    # 현재 시나리오 가져오기
    scenario = get_scenario(st.session_state.current_scenario)
    
    if scenario is None:
        st.success(f"축하합니다! 전쟁에서 끝까지 생존했습니다. 최종 생존 점수: {st.session_state.survival_score}")
        if st.button("다시 시작"):
            st.session_state.clear()
            st.rerun()
        return

    st.header(scenario["title"])
    
    # 이미지가 있는 경우 표시
    if "image" in scenario and scenario["image"]:
        st.image(scenario["image"])
    
    st.write(scenario["description"])
    
    # 선택지 제공
    choice = st.radio("선택하세요:", list(scenario["choices"].keys()), key=f"scenario_{st.session_state.current_scenario}")
    
    if st.button("선택 완료", key="choice_confirm_btn"):
        result = scenario["choices"][choice]
        st.session_state.survival_score += result["score"]
        st.session_state.history.append(f"{scenario['title']}: {choice} ({result['message']})")
        
        # 결과 메시지 표시
        if result["score"] > 0:
            st.success(f"{result['message']} (점수 +{result['score']})")
        else:
            st.error(f"{result['message']} (점수 {result['score']})")
        
        st.session_state.current_scenario += 1
        st.rerun()

    # 지난 선택 히스토리 표시
    if st.session_state.history:
        st.sidebar.header("지난 선택들")
        for event in st.session_state.history:
            st.sidebar.write(event)

def main():
    st.markdown(
        """
        <style>
        /* 메인 영역 스타일 */
        .stApp {
            background-color: white; /* 배경 흰색 */
            color: black !important; /* 텍스트 검은색 */
        }

        /* 버튼 스타일 */
        .stButton > button {
            color: black;
            background-color: transparent;
            border: 1px solid black;
        }
        .stButton > button:hover {
            color: white;
            background-color: black;
        }
        
        /* 사이드바 스타일 */
        section[data-testid="stSidebar"] {
            background-color: black !important; /* 배경을 검은색으로 설정 */
        }
        section[data-testid="stSidebar"] * {
            color: white !important; /* 사이드바 내 모든 텍스트를 흰색으로 설정 */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    init_session_state()
    show_game()

if __name__ == "__main__":
    main()
