# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Callable, Dict, List

from config import PRESENT_SEQUENCE
from models import Stage, Task
from problems import (
    make_association_task,
    make_composite_task,
    make_grid_task,
    make_nback_task,
    make_order_task,
    make_route_task,
    make_rule_memory_task,
    make_sequence_task,
    make_story_detail_task,
    make_swap_task,
)


def tutorial_problem(difficulty: str):
    return make_sequence_task(
        difficulty,
        items=["회중시계", "책", "찻잔", "열쇠", "촛대", "지도"],
        base_count=3,
        low_count=3,
        high_count=3,
        intro="토끼굴을 떨어지는 동안 물건들이 하나씩 보입니다. 순서를 기억하세요.",
        question_template="{position}번째로 본 물건은 무엇이었나요?",
        base_memory_ms=4500,
        tip="나타난 순서를 머릿속으로 이어 붙여 기억해 보세요.",
        presentation=PRESENT_SEQUENCE,
        item_ms=1000,
        gap_ms=250,
    )


def small_door_problem(difficulty: str):
    return make_sequence_task(
        difficulty,
        items=[
            "열쇠",
            "병",
            "케이크",
            "부채",
            "장갑",
            "작은 문",
            "커튼",
            "금빛 열쇠",
        ],
        base_count=4,
        low_count=3,
        high_count=6,
        intro="작은 방에서 물건이 하나씩 나타납니다. 순서를 기억하세요.",
        base_memory_ms=4300,
        presentation=PRESENT_SEQUENCE,
        item_ms=900,
        gap_ms=250,
    )


def pool_problem(difficulty: str):
    return make_association_task(
        difficulty,
        left_pool=["흰 토끼", "오리", "쥐", "도도새", "앵무새", "게"],
        right_pool=[
            "왼쪽 위",
            "가운데 위",
            "오른쪽 위",
            "왼쪽 아래",
            "가운데 아래",
            "오른쪽 아래",
        ],
        sample_count=4,
        intro="눈물의 웅덩이에서 모두의 위치를 기억하세요.",
        question_template="{target}는 어디에 있었나요?",
        base_memory_ms=5000,
    )


def caucus_problem(difficulty: str):
    return make_order_task(
        difficulty,
        items=["도도새", "오리", "쥐", "앵무새", "독수리", "게"],
        intro="코커스 경주의 순서를 기억하세요.",
        base_memory_ms=5000,
    )


def rabbit_house_problem(difficulty: str):
    return make_nback_task(
        difficulty,
        item_pool=[str(i) for i in range(1, 10)],
        intro="흰 토끼의 집에서 숫자 표지가 하나씩 지나갑니다.",
        noun="숫자",
    )


def caterpillar_problem(difficulty: str):
    """애벌레 에피소드: 누적 계산이 아니라 규칙 기억 훈련."""
    return make_rule_memory_task(
        difficulty,
        rule_keys=[
            "버섯의 왼쪽 조각",
            "버섯의 오른쪽 조각",
        ],
        rule_values=[
            "몸이 커진다",
            "몸이 작아진다",
        ],
        intro=(
            "애벌레는 버섯의 두 조각이 서로 다른 효과를 가진다고 알려 줍니다.\n"
            "어느 쪽이 몸을 키우고 어느 쪽이 몸을 줄이는지는 "
            "이번 문제의 규칙을 보고 기억해야 합니다."
        ),
    )


def duchess_problem(difficulty: str):
    return make_association_task(
        difficulty,
        left_pool=["공작부인", "요리사", "아기", "고양이"],
        right_pool=["후추", "수프", "접시", "자장가"],
        sample_count=4,
        intro="부엌의 관계를 기억하세요.",
        base_memory_ms=5200,
        extra_lines=[
            "추가 상황: 후추가 나오면 모두 재채기합니다.",
            "추가 상황: 접시가 날아가면 아기가 웃습니다.",
            "추가 상황: 자장가가 들리면 고양이가 미소 짓습니다.",
        ],
    )


def cheshire_problem(difficulty: str):
    return make_route_task(
        difficulty,
        intro=(
            "체셔 고양이가 알려 준 길입니다.\n"
            "앨리스는 출발점에서 다음 순서대로 이동합니다."
        ),
        base_memory_ms=5200,
    )


def tea_party_problem(difficulty: str):
    return make_swap_task(
        difficulty,
        people=["모자장수", "3월 토끼", "잠쥐", "앨리스"],
        items=["차", "케이크", "우유", "잼"],
        intro="미친 다과회의 자리와 물건 교환을 추적하세요.",
        base_memory_ms=6200,
    )


def queen_garden_problem(difficulty: str):
    return make_sequence_task(
        difficulty,
        items=["장미", "붓", "카드", "왕관", "창", "홍학", "열쇠", "시계"],
        base_count=5,
        low_count=4,
        high_count=7,
        intro=(
            "하트 여왕이 나타나기 전 카드 병사들이 물건을 하나씩 옮깁니다.\n"
            "나타나는 순서를 기억하세요."
        ),
        base_memory_ms=3100,
        presentation=PRESENT_SEQUENCE,
        item_ms=700,
        gap_ms=180,
    )


def croquet_problem(difficulty: str):
    return make_grid_task(
        difficulty,
        intro=(
            "크로케 경기입니다.\n"
            "고슴도치 공은 3×3 경기장의 '가운데'에서 시작합니다."
        ),
        subject_name="고슴도치",
        base_memory_ms=5200,
    )


def turtle_problem(difficulty: str):
    return make_story_detail_task(
        difficulty,
        category_pools={
            "시간": ["아침", "정오", "오후", "저녁"],
            "장소": ["바위", "해변", "동굴", "학교"],
            "수업": ["산수", "그림", "노래", "춤"],
            "음식": ["수프", "파이", "빵", "해초"],
        },
        intro_template=(
            "가짜 거북의 이야기를 기억하세요.\n\n"
            "가짜 거북은 {시간}에 {장소}로 갔습니다.\n"
            "그곳에서 {수업} 수업을 들었고,\n"
            "끝난 뒤 {음식}를 먹었습니다."
        ),
        question_templates={
            "시간": "가짜 거북이 그곳에 간 때는 언제였나요?",
            "장소": "가짜 거북은 어디로 갔나요?",
            "수업": "어떤 수업을 들었나요?",
            "음식": "이야기 끝에 먹은 것은 무엇인가요?",
        },
        base_memory_ms=6000,
    )


def trial_problem(difficulty: str):
    return make_composite_task(
        difficulty,
        generators=[
            small_door_problem,
            rabbit_house_problem,
            tea_party_problem,
            croquet_problem,
            turtle_problem,
        ],
        memory_prefix="♛ 최종 재판 ♛\n\n",
        question_prefix="재판 질문:\n",
    )


TRAINING_TYPE_LABELS: Dict[Callable[[str], Task], str] = {
    tutorial_problem: "순서 기억",
    small_door_problem: "순서 기억",
    pool_problem: "대응 기억",
    caucus_problem: "순위 기억",
    rabbit_house_problem: "N-Back",
    caterpillar_problem: "규칙 기억",
    duchess_problem: "대응 기억",
    cheshire_problem: "공간 추적",
    tea_party_problem: "교환 추적",
    queen_garden_problem: "순서 기억",
    croquet_problem: "공간 추적",
    turtle_problem: "이야기 기억",
    trial_problem: "복합 훈련",
}


def get_training_type(generator: Callable[[str], Task]) -> str:
    return TRAINING_TYPE_LABELS.get(generator, "기타")


def build_stages() -> List[Stage]:
    return [
        Stage(
            "프롤로그 · 흰 토끼",
            "언니 옆에서 지루해하던 앨리스는 조끼를 입고 회중시계를 보는 흰 토끼를 발견합니다. "
            "토끼가 늦었다며 달려가자, 앨리스는 호기심을 참지 못하고 뒤를 쫓아 토끼굴로 뛰어듭니다.",
            tutorial_problem,
        ),
        Stage(
            "1장 · 작은 문과 금빛 열쇠",
            "긴 추락 끝에 앨리스는 여러 문이 있는 방에 도착합니다. 작은 문 너머에는 아름다운 정원이 보이지만 "
            "몸이 너무 큽니다. 병과 케이크를 먹으며 몸이 커졌다 작아졌다 하는 소동이 시작됩니다.",
            small_door_problem,
        ),
        Stage(
            "2장 · 눈물의 웅덩이",
            "몸이 지나치게 커진 앨리스는 서러워 울음을 터뜨리고 거대한 눈물 웅덩이를 만듭니다. "
            "다시 작아진 뒤 그 물에 빠지고, 여러 동물과 함께 헤엄치게 됩니다.",
            pool_problem,
        ),
        Stage(
            "3장 · 코커스 경주",
            "젖은 몸을 말리기 위해 도도새는 시작도 끝도 분명하지 않은 코커스 경주를 제안합니다. "
            "모두 제멋대로 달리다가 어느 순간 모두가 승자라는 결론이 납니다.",
            caucus_problem,
        ),
        Stage(
            "4장 · 흰 토끼의 집",
            "흰 토끼는 앨리스를 하녀로 착각해 집으로 심부름을 보냅니다. 집 안에서 무언가를 먹은 앨리스는 "
            "다시 거대해져 집을 가득 채우고, 밖에서는 동물들이 그녀를 끌어내려 소동을 벌입니다.",
            rabbit_house_problem,
        ),
        Stage(
            "5장 · 버섯 위의 애벌레",
            "버섯 위에서 물담배를 피우는 애벌레를 만납니다. 그는 앨리스에게 버섯의 한쪽은 몸을 키우고 "
            "다른 쪽은 몸을 줄인다고 알려 줍니다. 앨리스는 조금씩 원하는 크기를 조절하는 법을 익힙니다.",
            caterpillar_problem,
        ),
        Stage(
            "6장 · 공작부인의 부엌",
            "공작부인의 집은 후추와 연기, 날아다니는 접시로 엉망입니다. 요리사는 난폭하고 아기는 계속 울며, "
            "체셔 고양이만이 기묘한 미소를 짓고 있습니다. 앨리스가 아기를 데리고 나오자 아기는 돼지로 변합니다.",
            duchess_problem,
        ),
        Stage(
            "7장 · 체셔 고양이",
            "체셔 고양이는 나타났다 사라지기를 반복하며 길을 알려 줍니다. 앨리스가 어디로 가야 할지 묻자, "
            "고양이는 이곳에서는 모두가 미쳤다고 말하며 모자장수와 3월 토끼가 있는 방향을 가리킵니다.",
            cheshire_problem,
        ),
        Stage(
            "8장 · 미친 다과회",
            "모자장수, 3월 토끼, 잠쥐는 끝나지 않는 티타임을 보내고 있습니다. 자리는 계속 바뀌고, "
            "수수께끼와 말장난이 이어지며, 누가 무엇을 가지고 있었는지조차 금세 뒤섞입니다.",
            tea_party_problem,
        ),
        Stage(
            "9장 · 하트 여왕의 정원",
            "카드 병사들은 흰 장미를 잘못 심었다는 사실을 감추기 위해 장미를 붉게 칠합니다. "
            "하트 여왕이 나타나자 사소한 일에도 '목을 쳐라!'라고 외치며 모두를 공포에 빠뜨립니다.",
            queen_garden_problem,
        ),
        Stage(
            "10장 · 기묘한 크로케 경기",
            "앨리스는 살아 있는 홍학을 채로, 고슴도치를 공으로 쓰는 크로케 경기에 참가합니다. "
            "선수와 공과 골문이 제멋대로 움직이니 정상적인 경기 규칙은 아무 의미가 없습니다.",
            croquet_problem,
        ),
        Stage(
            "11장 · 가짜 거북과 그리폰",
            "그리폰은 앨리스를 가짜 거북에게 데려갑니다. 가짜 거북은 자신이 다녔다는 바닷속 학교와 "
            "이상한 수업, 춤, 음식에 대해 길고도 엉뚱한 이야기를 들려줍니다.",
            turtle_problem,
        ),
        Stage(
            "12장 · 하트 잭의 재판",
            "하트 잭이 여왕의 타르트를 훔쳤다는 재판이 열립니다. 증언은 앞뒤가 맞지 않고 규칙도 즉석에서 바뀝니다. "
            "앨리스는 점점 커지며 이 재판이 얼마나 터무니없는지 깨닫기 시작합니다.",
            trial_problem,
        ),
        Stage(
            "최종장 · 너희들은 카드일 뿐이야!",
            "재판이 완전히 엉망이 되자 앨리스는 마침내 두려움을 떨쳐 냅니다. "
            "여왕과 카드 병사들이 몰려들지만 앨리스는 그들을 향해 '너희들은 카드 한 벌일 뿐이야!'라고 외칩니다.",
            trial_problem,
        ),
    ]