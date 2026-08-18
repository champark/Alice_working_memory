이상한 나라의 앨리스 - 작업기억 어드벤처
모듈화 버전

실행 방법
---------
1. 이 폴더 구조를 그대로 유지합니다.
2. Python 3에서 main.py를 실행합니다.

    python main.py


파일 역할
---------
main.py
    프로그램 시작점.

app.py
    Tkinter UI, 라이프, 스테이지 진행, Enter 키,
    에피소드 선택, 정답/오답 같은 게임 흐름만 담당.

episodes.py
    앨리스의 스토리, 에피소드 제목, 에피소드별 단어,
    어떤 문제 엔진을 사용할지를 담당.
    앞으로 에피소드 수정 시 가장 자주 편집할 파일.

difficulty.py
    편안하게/보통/도전 난이도의 항목 수,
    기억시간, N-Back 속도, 교환횟수 등을 담당.

presentation.py
    문제를 '어떻게 보여주는가'만 담당.
    현재 static(동시 표시) / sequence(순차 표시) 지원.

models.py
    Task, Stage 공통 데이터 구조.

config.py
    창 크기, 라이프 수, 라운드 수, 색상 등 전역 설정.

problems/
    작업기억 문제 규칙 자체.
    에피소드 이름이나 Tkinter 화면 흐름을 몰라도 작동하도록 분리.

    sequence.py
        순서 기억

    association.py
        대응/연결 기억

    order.py
        순위/전후 관계 기억

    nback.py
        N-Back

    state_tracking.py
        상태 변화 누적 / 물건 교환 추적

    spatial.py
        자유 이동 / 3x3 위치 추적

    story_detail.py
        이야기 속 속성 기억

    composite.py
        여러 문제 엔진 중 하나를 무작위 선택

    common.py
        객관식 보기 생성 등의 공통 함수


설계 원칙
---------
[episodes.py]
    무엇을 보여줄 것인가 / 세계관

        ↓

[problems/]
    무엇을 기억하고 어떤 규칙으로 답할 것인가

        ↓

[presentation.py]
    동시에 보여줄지, 하나씩 보여줄지

        ↓

[difficulty.py]
    얼마나 많이, 얼마나 빠르게 보여줄지

        ↓

[app.py]
    실제 게임 진행과 화면 전환


주의
----
현재 버전은 기존 게임의 기능을 유지하면서 구조를 분리한 1차 리팩터링입니다.
추후 에피소드마다 '동일 엔진 + 다른 표시방식'을 자유롭게 고를 수 있도록
presentation 설정을 episodes.py 쪽으로 더 데이터화하기 좋게 설계했습니다.
