# -*- coding: utf-8 -*-
"""
이상한 나라의 앨리스 - 작업기억 어드벤처
Python 3.x / Tkinter 표준 라이브러리만 사용

실행:
    python alice_working_memory.py
"""

from __future__ import annotations

import random
import tkinter as tk
from dataclasses import dataclass
from typing import Callable, List, Optional, Tuple


# -----------------------------
# 기본 설정
# -----------------------------
APP_TITLE = "이상한 나라의 앨리스 - 작업기억 어드벤처"
START_LIVES = 5
ROUNDS_PER_STAGE = 3

BG = "#f6f1ff"
PANEL = "#ffffff"
INK = "#28233a"
MUTED = "#6e6780"
ACCENT = "#7652b8"
ACCENT_2 = "#b596e6"
GOOD = "#2e8b57"
BAD = "#c84d4d"
BAR_BG = "#ded6ee"
BAR_FG = "#8f6ccf"
BUTTON_BG = "#eee7fa"
BUTTON_ACTIVE = "#dfd2f4"


DIFFICULTIES = {
    "편안하게": {
        "memory_ms_mul": 1.35,
        "item_delta": -1,
        "nback": 1,
    },
    "보통": {
        "memory_ms_mul": 1.00,
        "item_delta": 0,
        "nback": 2,
    },
    "도전": {
        "memory_ms_mul": 0.78,
        "item_delta": 1,
        "nback": 2,
    },
}


@dataclass
class Task:
    memory_text: str
    question_text: str
    options: List[str]
    correct_index: int
    memory_ms: int
    tip: str = ""
    presentation: str = "static"
    sequence: Optional[List[str]] = None
    item_ms: int = 900
    gap_ms: int = 250


@dataclass
class Stage:
    title: str
    story: str
    generator: Callable[["AliceMemoryGame"], Task]


# -----------------------------
# 작업기억 문제 생성기
# -----------------------------
def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def stage_memory_ms(game: "AliceMemoryGame", base_ms: int) -> int:
    mul = DIFFICULTIES[game.difficulty]["memory_ms_mul"]
    return int(base_ms * mul)


def item_count(game: "AliceMemoryGame", base: int, low: int = 3, high: int = 8) -> int:
    delta = DIFFICULTIES[game.difficulty]["item_delta"]
    return clamp(base + delta, low, high)


def make_unique_options(correct: str, pool: List[str], count: int = 4) -> Tuple[List[str], int]:
    wrongs = [x for x in pool if x != correct]
    random.shuffle(wrongs)
    opts = [correct] + wrongs[: max(0, count - 1)]
    random.shuffle(opts)
    return opts, opts.index(correct)


def gen_tutorial(game: "AliceMemoryGame") -> Task:
    seq = random.sample(["회중시계", "책", "찻잔", "열쇠", "촛대", "지도"], 3)
    idx = random.randrange(len(seq))
    correct = seq[idx]
    opts, correct_idx = make_unique_options(correct, ["회중시계", "책", "찻잔", "열쇠", "촛대", "지도"])
    return Task(
        memory_text="토끼굴을 떨어지는 동안 이것들이 보였습니다.\n\n" + "   →   ".join(seq),
        question_text=f"{idx + 1}번째로 본 물건은 무엇이었나요?",
        options=opts,
        correct_index=correct_idx,
        memory_ms=stage_memory_ms(game, 4500),
        tip="순서 전체를 한 덩어리의 장면처럼 떠올려 보세요.",
    )


def gen_sequence_recall(game: "AliceMemoryGame") -> Task:
    pool = ["열쇠", "병", "케이크", "부채", "장갑", "작은 문", "커튼", "금빛 열쇠"]
    n = item_count(game, 4, 3, 6)
    seq = random.sample(pool, n)
    idx = random.randrange(n)
    correct = seq[idx]
    opts, correct_idx = make_unique_options(correct, pool)
    return Task(
        memory_text="작은 방에서 본 순서를 기억하세요.\n\n" + "  →  ".join(seq),
        question_text=f"{idx + 1}번째 물건은 무엇이었나요?",
        options=opts,
        correct_index=correct_idx,
        memory_ms=stage_memory_ms(game, 4300),
    )


def gen_association_positions(game: "AliceMemoryGame") -> Task:
    objects = random.sample(["흰 토끼", "오리", "쥐", "도도새", "앵무새", "게"], 4)
    positions = random.sample(
        ["왼쪽 위", "가운데 위", "오른쪽 위", "왼쪽 아래", "가운데 아래", "오른쪽 아래"],
        4,
    )
    pairs = list(zip(objects, positions))
    target_obj, correct = random.choice(pairs)
    memory = "눈물의 웅덩이에서 모두의 위치를 기억하세요.\n\n"
    memory += "\n".join(f"{obj:<6} : {pos}" for obj, pos in pairs)
    opts, correct_idx = make_unique_options(
        correct,
        ["왼쪽 위", "가운데 위", "오른쪽 위", "왼쪽 아래", "가운데 아래", "오른쪽 아래"],
    )
    return Task(
        memory_text=memory,
        question_text=f"{target_obj}는 어디에 있었나요?",
        options=opts,
        correct_index=correct_idx,
        memory_ms=stage_memory_ms(game, 5000),
    )


def gen_race_order(game: "AliceMemoryGame") -> Task:
    racers = random.sample(["도도새", "오리", "쥐", "앵무새", "독수리", "게"], item_count(game, 5, 4, 6))
    target_idx = random.randrange(1, len(racers))
    target = racers[target_idx]
    correct = racers[target_idx - 1]
    opts, correct_idx = make_unique_options(correct, racers)
    return Task(
        memory_text="코커스 경주의 순서를 기억하세요.\n\n" + "\n".join(
            f"{i + 1}위  {name}" for i, name in enumerate(racers)
        ),
        question_text=f"{target} 바로 앞에 있던 참가자는 누구였나요?",
        options=opts,
        correct_index=correct_idx,
        memory_ms=stage_memory_ms(game, 5000),
    )


def nback_timing(game: "AliceMemoryGame") -> Tuple[int, int]:
    # 숫자 1개 표시 시간 / 숫자 사이 빈 화면 시간
    if game.difficulty == "편안하게":
        return 1200, 320
    if game.difficulty == "도전":
        return 650, 200
    return 900, 250


def gen_nback(game: "AliceMemoryGame") -> Task:
    n_back = DIFFICULTIES[game.difficulty]["nback"]
    length = item_count(game, 7, 6, 9)
    digits = [random.randint(1, 9) for _ in range(length)]

    # 정답이 '같다'와 '다르다'가 골고루 나오게 일부러 구성
    want_same = random.choice([True, False])
    if want_same:
        digits[-1] = digits[-1 - n_back]
    else:
        forbidden = digits[-1 - n_back]
        choices = [d for d in range(1, 10) if d != forbidden]
        digits[-1] = random.choice(choices)

    item_ms, gap_ms = nback_timing(game)

    return Task(
        memory_text=(
            "흰 토끼의 집에서 숫자 표지가 하나씩 지나갑니다.\n\n"
            f"각 숫자를 보면서 {n_back}칸 전 숫자를 계속 기억하세요.\n"
            "마지막 숫자가 사라진 뒤 질문이 나옵니다."
        ),
        question_text=f"마지막 숫자는 {n_back}칸 전 숫자와 같았나요?",
        options=["같다", "다르다"],
        correct_index=0 if want_same else 1,
        memory_ms=0,
        tip="숫자는 한 번에 하나씩만 표시됩니다. 오답 시 같은 숫자열을 처음부터 다시 보여 줍니다.",
        presentation="sequence",
        sequence=[str(d) for d in digits],
        item_ms=item_ms,
        gap_ms=gap_ms,
    )


def gen_size_rules(game: "AliceMemoryGame") -> Task:
    # 왼쪽=-1, 오른쪽=+1
    n = item_count(game, 5, 4, 7)
    moves = [random.choice(["왼쪽", "오른쪽"]) for _ in range(n)]
    score = sum(1 if x == "오른쪽" else -1 for x in moves)
    correct = "커졌다" if score > 0 else "작아졌다" if score < 0 else "같다"
    return Task(
        memory_text=(
            "애벌레가 말합니다.\n"
            "왼쪽 버섯 = 한 단계 작아짐\n"
            "오른쪽 버섯 = 한 단계 커짐\n\n"
            "먹은 순서:\n" + "  →  ".join(moves)
        ),
        question_text="처음과 비교하면 앨리스의 크기는 어떻게 되었나요?",
        options=["커졌다", "작아졌다", "같다"],
        correct_index=["커졌다", "작아졌다", "같다"].index(correct),
        memory_ms=stage_memory_ms(game, 5200),
    )


def gen_condition_memory(game: "AliceMemoryGame") -> Task:
    people = ["공작부인", "요리사", "아기", "고양이"]
    items = ["후추", "수프", "접시", "자장가"]
    random.shuffle(items)
    pairs = dict(zip(people, items))
    target = random.choice(people)
    correct = pairs[target]

    extra_rule = random.choice([
        "후추가 나오면 모두 재채기한다.",
        "접시가 날아가면 아기가 웃는다.",
        "자장가가 들리면 고양이가 미소 짓는다.",
    ])

    memory = "부엌의 관계를 기억하세요.\n\n"
    memory += "\n".join(f"{p} ↔ {pairs[p]}" for p in people)
    memory += "\n\n추가 규칙: " + extra_rule

    opts, correct_idx = make_unique_options(correct, items)
    return Task(
        memory_text=memory,
        question_text=f"{target}와 연결되어 있던 것은 무엇인가요?",
        options=opts,
        correct_index=correct_idx,
        memory_ms=stage_memory_ms(game, 5200),
    )


def gen_route_memory(game: "AliceMemoryGame") -> Task:
    # 시작 좌표 (0,0), 4~6번 이동 후 최종 상대 위치 판정
    dirs = {
        "위": (0, -1),
        "아래": (0, 1),
        "왼쪽": (-1, 0),
        "오른쪽": (1, 0),
    }
    n = item_count(game, 5, 4, 7)
    moves = [random.choice(list(dirs.keys())) for _ in range(n)]
    x = y = 0
    for m in moves:
        dx, dy = dirs[m]
        x += dx
        y += dy

    if x == 0 and y == 0:
        correct = "출발점"
    elif abs(x) >= abs(y):
        correct = "오른쪽" if x > 0 else "왼쪽"
    else:
        correct = "아래쪽" if y > 0 else "위쪽"

    options = ["위쪽", "아래쪽", "왼쪽", "오른쪽", "출발점"]
    return Task(
        memory_text=(
            "체셔 고양이가 알려 준 길입니다.\n"
            "앨리스는 출발점에서 다음 순서대로 이동합니다.\n\n"
            + "  →  ".join(moves)
        ),
        question_text="이동이 끝났을 때 앨리스는 출발점에서 대체로 어느 쪽에 있나요?",
        options=options,
        correct_index=options.index(correct),
        memory_ms=stage_memory_ms(game, 5200),
    )


def gen_swap_matching(game: "AliceMemoryGame") -> Task:
    people = ["모자장수", "3월 토끼", "잠쥐", "앨리스"]
    items = ["차", "케이크", "우유", "잼"]
    random.shuffle(items)
    mapping = dict(zip(people, items))

    swaps = []
    swap_count = 1 if game.difficulty == "편안하게" else 2
    if game.difficulty == "도전":
        swap_count = 3

    for _ in range(swap_count):
        a, b = random.sample(people, 2)
        swaps.append((a, b))
        mapping[a], mapping[b] = mapping[b], mapping[a]

    target = random.choice(people)
    correct = mapping[target]

    initial_items = items[:]
    # 초기 매핑 재구성: 스왑을 역순으로 되돌림
    initial_map = mapping.copy()
    for a, b in reversed(swaps):
        initial_map[a], initial_map[b] = initial_map[b], initial_map[a]

    memory = "처음 자리:\n"
    memory += "\n".join(f"{p:<6} : {initial_map[p]}" for p in people)
    memory += "\n\n교환:\n"
    memory += "\n".join(f"{a} ↔ {b}" for a, b in swaps)

    opts, correct_idx = make_unique_options(correct, initial_items)
    return Task(
        memory_text=memory,
        question_text=f"모든 교환이 끝난 뒤 {target}가 가진 것은 무엇인가요?",
        options=opts,
        correct_index=correct_idx,
        memory_ms=stage_memory_ms(game, 6200),
    )


def gen_fast_sequence(game: "AliceMemoryGame") -> Task:
    pool = ["장미", "붓", "카드", "왕관", "창", "홍학", "열쇠", "시계"]
    n = item_count(game, 5, 4, 7)
    seq = random.sample(pool, n)
    idx = random.randrange(n)
    correct = seq[idx]
    opts, correct_idx = make_unique_options(correct, pool)
    return Task(
        memory_text=(
            "하트 여왕이 나타나기 전, 카드 병사들이 물건을 옮깁니다.\n"
            "이번에는 시간이 조금 짧습니다.\n\n"
            + "   →   ".join(seq)
        ),
        question_text=f"{idx + 1}번째 물건은 무엇이었나요?",
        options=opts,
        correct_index=correct_idx,
        memory_ms=stage_memory_ms(game, 3100),
    )


def gen_grid_tracker(game: "AliceMemoryGame") -> Task:
    # 3x3 좌표: x,y = 0..2
    labels = {
        (0, 0): "왼쪽 위", (1, 0): "가운데 위", (2, 0): "오른쪽 위",
        (0, 1): "왼쪽", (1, 1): "가운데", (2, 1): "오른쪽",
        (0, 2): "왼쪽 아래", (1, 2): "가운데 아래", (2, 2): "오른쪽 아래",
    }
    x = y = 1
    moves = []
    move_count = 3 if game.difficulty == "편안하게" else 4
    if game.difficulty == "도전":
        move_count = 5

    for _ in range(move_count):
        valid = []
        if y > 0:
            valid.append(("위", 0, -1))
        if y < 2:
            valid.append(("아래", 0, 1))
        if x > 0:
            valid.append(("왼쪽", -1, 0))
        if x < 2:
            valid.append(("오른쪽", 1, 0))
        name, dx, dy = random.choice(valid)
        moves.append(name)
        x += dx
        y += dy

    correct = labels[(x, y)]
    options = list(labels.values())
    random.shuffle(options)
    # 버튼이 너무 많아지는 것을 막기 위해 정답 + 오답 4개
    if correct not in options[:5]:
        options = [correct] + [o for o in options if o != correct][:4]
        random.shuffle(options)
    else:
        options = options[:5]
        if correct not in options:
            options[-1] = correct
            random.shuffle(options)

    return Task(
        memory_text=(
            "크로케 경기입니다.\n"
            "고슴도치 공은 3×3 경기장의 '가운데'에서 시작합니다.\n\n"
            "이동:\n" + "  →  ".join(moves)
        ),
        question_text="고슴도치는 마지막에 어디에 있나요?",
        options=options,
        correct_index=options.index(correct),
        memory_ms=stage_memory_ms(game, 5200),
    )


def gen_story_detail(game: "AliceMemoryGame") -> Task:
    times = ["아침", "정오", "오후", "저녁"]
    foods = ["수프", "파이", "빵", "해초"]
    subjects = ["산수", "그림", "노래", "춤"]
    places = ["바위", "해변", "동굴", "학교"]

    facts = {
        "시간": random.choice(times),
        "음식": random.choice(foods),
        "수업": random.choice(subjects),
        "장소": random.choice(places),
    }

    memory = (
        "가짜 거북의 이야기를 기억하세요.\n\n"
        f"가짜 거북은 {facts['시간']}에 {facts['장소']}로 갔습니다.\n"
        f"그곳에서 {facts['수업']} 수업을 들었고,\n"
        f"끝난 뒤 {facts['음식']}를 먹었습니다."
    )

    key = random.choice(list(facts.keys()))
    correct = facts[key]
    pool = {
        "시간": times,
        "음식": foods,
        "수업": subjects,
        "장소": places,
    }[key]
    q = {
        "시간": "가짜 거북이 그곳에 간 때는 언제였나요?",
        "음식": "이야기 끝에 먹은 것은 무엇인가요?",
        "수업": "어떤 수업을 들었나요?",
        "장소": "어디로 갔나요?",
    }[key]

    opts, correct_idx = make_unique_options(correct, pool)
    return Task(
        memory_text=memory,
        question_text=q,
        options=opts,
        correct_index=correct_idx,
        memory_ms=stage_memory_ms(game, 6000),
    )


def gen_trial_mix(game: "AliceMemoryGame") -> Task:
    # 최종장은 앞서 나온 핵심 유형을 무작위 혼합
    generator = random.choice([
        gen_sequence_recall,
        gen_nback,
        gen_swap_matching,
        gen_grid_tracker,
        gen_story_detail,
    ])
    task = generator(game)
    task.memory_text = "♛ 최종 재판 ♛\n\n" + task.memory_text
    task.question_text = "재판 질문:\n" + task.question_text
    return task


# -----------------------------
# 메인 게임
# -----------------------------
class AliceMemoryGame:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("900x800")
        self.root.minsize(760, 620)
        self.root.configure(bg=BG)

        self.difficulty = "보통"
        self.difficulty_var = tk.StringVar(value=self.difficulty)
        self.lives = START_LIVES
        self.stage_index = 0
        self.round_in_stage = 0
        self.current_task: Optional[Task] = None

        self.after_ids: List[str] = []
        self.timer_after_id: Optional[str] = None

        self.stages = self.build_stages()
        self.build_shell()
        self.show_title_screen()

    # ---------- 스테이지 데이터 ----------
    def build_stages(self) -> List[Stage]:
        return [
            Stage(
                "프롤로그 · 흰 토끼",
                "언니 옆에서 지루해하던 앨리스는 조끼를 입고 회중시계를 보는 흰 토끼를 발견합니다. "
                "토끼가 늦었다며 달려가자, 앨리스는 호기심을 참지 못하고 뒤를 쫓아 토끼굴로 뛰어듭니다.",
                gen_tutorial,
            ),
            Stage(
                "1장 · 작은 문과 금빛 열쇠",
                "긴 추락 끝에 앨리스는 여러 문이 있는 방에 도착합니다. 작은 문 너머에는 아름다운 정원이 보이지만 "
                "몸이 너무 큽니다. 병과 케이크를 먹으며 몸이 커졌다 작아졌다 하는 소동이 시작됩니다.",
                gen_sequence_recall,
            ),
            Stage(
                "2장 · 눈물의 웅덩이",
                "몸이 지나치게 커진 앨리스는 서러워 울음을 터뜨리고 거대한 눈물 웅덩이를 만듭니다. "
                "다시 작아진 뒤 그 물에 빠지고, 여러 동물과 함께 헤엄치게 됩니다.",
                gen_association_positions,
            ),
            Stage(
                "3장 · 코커스 경주",
                "젖은 몸을 말리기 위해 도도새는 시작도 끝도 분명하지 않은 코커스 경주를 제안합니다. "
                "모두 제멋대로 달리다가 어느 순간 모두가 승자라는 결론이 납니다.",
                gen_race_order,
            ),
            Stage(
                "4장 · 흰 토끼의 집",
                "흰 토끼는 앨리스를 하녀로 착각해 집으로 심부름을 보냅니다. 집 안에서 무언가를 먹은 앨리스는 "
                "다시 거대해져 집을 가득 채우고, 밖에서는 동물들이 그녀를 끌어내려 소동을 벌입니다.",
                gen_nback,
            ),
            Stage(
                "5장 · 버섯 위의 애벌레",
                "버섯 위에서 물담배를 피우는 애벌레를 만납니다. 그는 앨리스에게 버섯의 한쪽은 몸을 키우고 "
                "다른 쪽은 몸을 줄인다고 알려 줍니다. 앨리스는 조금씩 원하는 크기를 조절하는 법을 익힙니다.",
                gen_size_rules,
            ),
            Stage(
                "6장 · 공작부인의 부엌",
                "공작부인의 집은 후추와 연기, 날아다니는 접시로 엉망입니다. 요리사는 난폭하고 아기는 계속 울며, "
                "체셔 고양이만이 기묘한 미소를 짓고 있습니다. 앨리스가 아기를 데리고 나오자 아기는 돼지로 변합니다.",
                gen_condition_memory,
            ),
            Stage(
                "7장 · 체셔 고양이",
                "체셔 고양이는 나타났다 사라지기를 반복하며 길을 알려 줍니다. 앨리스가 어디로 가야 할지 묻자, "
                "고양이는 이곳에서는 모두가 미쳤다고 말하며 모자장수와 3월 토끼가 있는 방향을 가리킵니다.",
                gen_route_memory,
            ),
            Stage(
                "8장 · 미친 다과회",
                "모자장수, 3월 토끼, 잠쥐는 끝나지 않는 티타임을 보내고 있습니다. 자리는 계속 바뀌고, "
                "수수께끼와 말장난이 이어지며, 누가 무엇을 가지고 있었는지조차 금세 뒤섞입니다.",
                gen_swap_matching,
            ),
            Stage(
                "9장 · 하트 여왕의 정원",
                "카드 병사들은 흰 장미를 잘못 심었다는 사실을 감추기 위해 장미를 붉게 칠합니다. "
                "하트 여왕이 나타나자 사소한 일에도 '목을 쳐라!'라고 외치며 모두를 공포에 빠뜨립니다.",
                gen_fast_sequence,
            ),
            Stage(
                "10장 · 기묘한 크로케 경기",
                "앨리스는 살아 있는 홍학을 채로, 고슴도치를 공으로 쓰는 크로케 경기에 참가합니다. "
                "선수와 공과 골문이 제멋대로 움직이니 정상적인 경기 규칙은 아무 의미가 없습니다.",
                gen_grid_tracker,
            ),
            Stage(
                "11장 · 가짜 거북과 그리폰",
                "그리폰은 앨리스를 가짜 거북에게 데려갑니다. 가짜 거북은 자신이 다녔다는 바닷속 학교와 "
                "이상한 수업, 춤, 음식에 대해 길고도 엉뚱한 이야기를 들려줍니다.",
                gen_story_detail,
            ),
            Stage(
                "12장 · 하트 잭의 재판",
                "하트 잭이 여왕의 타르트를 훔쳤다는 재판이 열립니다. 증언은 앞뒤가 맞지 않고 규칙도 즉석에서 바뀝니다. "
                "앨리스는 점점 커지며 이 재판이 얼마나 터무니없는지 깨닫기 시작합니다.",
                gen_trial_mix,
            ),
            Stage(
                "최종장 · 너희들은 카드일 뿐이야!",
                "재판이 완전히 엉망이 되자 앨리스는 마침내 두려움을 떨쳐 냅니다. "
                "여왕과 카드 병사들이 몰려들지만 앨리스는 그들을 향해 '너희들은 카드 한 벌일 뿐이야!'라고 외칩니다.",
                gen_trial_mix,
            ),
        ]

    # ---------- UI ----------
    def build_shell(self) -> None:
        self.topbar = tk.Frame(self.root, bg=BG)
        self.topbar.pack(fill="x", padx=24, pady=(18, 8))

        self.stage_label = tk.Label(
            self.topbar, text="", bg=BG, fg=INK, font=("Malgun Gothic", 12, "bold")
        )
        self.stage_label.pack(side="left")

        self.life_label = tk.Label(
            self.topbar, text="", bg=BG, fg=BAD, font=("Malgun Gothic", 12, "bold")
        )
        self.life_label.pack(side="right")

        self.main = tk.Frame(
            self.root, bg=PANEL, highlightbackground="#d8cde9", highlightthickness=1
        )
        self.main.pack(fill="both", expand=True, padx=24, pady=(0, 16))

        self.title_label = tk.Label(
            self.main,
            text="",
            bg=PANEL,
            fg=INK,
            font=("Malgun Gothic", 24, "bold"),
            wraplength=800,
            justify="center",
        )
        self.title_label.pack(pady=(36, 16))

        self.body_label = tk.Label(
            self.main,
            text="",
            bg=PANEL,
            fg=INK,
            font=("Malgun Gothic", 14),
            wraplength=780,
            justify="center",
            padx=24,
        )
        self.body_label.pack(pady=(8, 16), fill="x")

        self.progress_canvas = tk.Canvas(
            self.main, height=16, bg=PANEL, highlightthickness=0
        )
        self.progress_canvas.pack(fill="x", padx=80, pady=(0, 12))
        self.progress_canvas.bind("<Configure>", self._redraw_bar_background)
        self.bar_rect = None
        self.bar_fraction = 0.0

        self.button_frame = tk.Frame(self.main, bg=PANEL)
        self.button_frame.pack(fill="both", expand=True, padx=70, pady=(8, 26))

        self.footer = tk.Label(
            self.root,
            text="",
            bg=BG,
            fg=MUTED,
            font=("Malgun Gothic", 10),
        )
        self.footer.pack(pady=(0, 12))

    def clear_buttons(self) -> None:
        for w in self.button_frame.winfo_children():
            w.destroy()

    def cancel_pending(self) -> None:
        for aid in self.after_ids:
            try:
                self.root.after_cancel(aid)
            except tk.TclError:
                pass
        self.after_ids.clear()

        if self.timer_after_id is not None:
            try:
                self.root.after_cancel(self.timer_after_id)
            except tk.TclError:
                pass
            self.timer_after_id = None

    def set_topbar(self) -> None:
        if 0 <= self.stage_index < len(self.stages):
            self.stage_label.config(
                text=f"STAGE {self.stage_index + 1}/{len(self.stages)} · "
                     f"{self.round_in_stage}/{ROUNDS_PER_STAGE}"
            )
        else:
            self.stage_label.config(text="")
        self.life_label.config(text="♥" * self.lives + "♡" * (START_LIVES - self.lives))

    def _redraw_bar_background(self, _event=None) -> None:
        self.update_progress(self.bar_fraction)

    def update_progress(self, fraction: float) -> None:
        self.bar_fraction = max(0.0, min(1.0, fraction))
        self.progress_canvas.delete("all")
        width = max(1, self.progress_canvas.winfo_width())
        height = max(1, self.progress_canvas.winfo_height())
        self.progress_canvas.create_rectangle(0, 0, width, height, fill=BAR_BG, outline="")
        self.progress_canvas.create_rectangle(
            0, 0, width * self.bar_fraction, height, fill=BAR_FG, outline=""
        )

    def hide_progress(self) -> None:
        self.update_progress(0)

    def add_button(self, text: str, command, big: bool = False) -> tk.Button:
        btn = tk.Button(
            self.button_frame,
            text=text,
            command=command,
            bg=ACCENT if big else BUTTON_BG,
            fg="white" if big else INK,
            activebackground=ACCENT_2 if big else BUTTON_ACTIVE,
            activeforeground="white" if big else INK,
            relief="flat",
            bd=0,
            font=("Malgun Gothic", 13, "bold" if big else "normal"),
            cursor="hand2",
            padx=16,
            pady=12,
            wraplength=620,
        )
        btn.pack(fill="x", pady=6)
        return btn

    # ---------- 화면 흐름 ----------
    def show_title_screen(self) -> None:
        self.cancel_pending()
        self.stage_index = 0
        self.round_in_stage = 0
        self.lives = START_LIVES
        self.set_topbar()
        self.stage_label.config(text="")
        self.life_label.config(text="")

        self.title_label.config(text="이상한 나라의 앨리스\n작업기억 어드벤처")
        self.body_label.config(
            text=(
                "흰 토끼를 따라 이상한 나라를 여행하며 작업기억 문제를 해결하세요.\n\n"
                f"각 스테이지에서 {ROUNDS_PER_STAGE}문제를 맞히면 다음 장으로 넘어갑니다.\n"
                f"틀릴 때마다 라이프가 1 감소하며, 라이프가 0이 되면 게임 오버입니다.\n"
                "오답 뒤에는 기억정보를 다시 보여 주고 같은 문제를 재도전합니다.\n\n"
                "난이도를 선택하세요."
            )
        )
        self.hide_progress()
        self.footer.config(text="외부 이미지나 파일 없이 Python 표준 라이브러리만으로 실행됩니다.")

        self.clear_buttons()
        self.difficulty_var.set(self.difficulty)

        radio_frame = tk.Frame(self.button_frame, bg=PANEL)
        radio_frame.pack(pady=(4, 18))

        for name in DIFFICULTIES:
            rb = tk.Radiobutton(
                radio_frame,
                text=name,
                variable=self.difficulty_var,
                value=name,
                command=lambda n=name: self.select_difficulty(n),
                bg=PANEL,
                fg=INK,
                activebackground=PANEL,
                activeforeground=ACCENT,
                selectcolor=BUTTON_BG,
                font=("Malgun Gothic", 13, "bold"),
                cursor="hand2",
                padx=14,
                pady=8,
            )
            rb.pack(side="left", padx=10)

        self.add_button("처음부터 플레이 ▶", self.start_game, big=True)
        self.add_button("에피소드 선택 / 테스트", self.show_episode_select, big=False)

    def select_difficulty(self, name: str) -> None:
        self.difficulty = name
        self.difficulty_var.set(name)

    def start_game(self) -> None:
        self.difficulty = self.difficulty_var.get()
        self.lives = START_LIVES
        self.stage_index = 0
        self.round_in_stage = 0
        self.current_task = None
        self.show_story()

    def show_episode_select(self) -> None:
        """개발/테스트용 에피소드 바로가기 화면.

        원하는 스테이지부터 즉시 시작할 수 있고, 클리어하면 그 다음
        스테이지로 정상적으로 이어진다. 난이도는 시작 화면에서 고른 값을 사용한다.
        """
        self.cancel_pending()
        self.clear_buttons()
        self.hide_progress()

        self.difficulty = self.difficulty_var.get()
        self.stage_label.config(text="EPISODE SELECT")
        self.life_label.config(text="")
        self.title_label.config(text="에피소드 선택 / 테스트 모드")
        self.body_label.config(
            text=(
                "수정하거나 시험할 에피소드를 바로 선택하세요.\n"
                "선택한 에피소드부터 라이프 5개로 시작하며, 클리어하면 다음 에피소드로 계속 진행됩니다.\n\n"
                f"현재 난이도: {self.difficulty}"
            ),
            font=("Malgun Gothic", 14),
        )
        self.footer.config(text="테스트용 바로가기입니다. 진행 기록이나 잠금 조건은 없습니다.")

        # 14개 에피소드가 한 화면에 안정적으로 들어오도록 2열로 배치한다.
        episode_grid = tk.Frame(self.button_frame, bg=PANEL)
        episode_grid.pack(fill="both", expand=True, pady=(0, 8))
        episode_grid.grid_columnconfigure(0, weight=1)
        episode_grid.grid_columnconfigure(1, weight=1)

        for idx, stage in enumerate(self.stages):
            row = idx // 2
            col = idx % 2
            btn = tk.Button(
                episode_grid,
                text=f"{idx + 1:02d}. {stage.title}",
                command=lambda i=idx: self.start_episode(i),
                bg=BUTTON_BG,
                fg=INK,
                activebackground=BUTTON_ACTIVE,
                activeforeground=INK,
                relief="flat",
                bd=0,
                font=("Malgun Gothic", 11, "bold"),
                cursor="hand2",
                padx=10,
                pady=8,
                wraplength=300,
                justify="center",
            )
            btn.grid(row=row, column=col, sticky="ew", padx=6, pady=4)

        back_btn = tk.Button(
            self.button_frame,
            text="← 시작 화면으로",
            command=self.show_title_screen,
            bg=ACCENT,
            fg="white",
            activebackground=ACCENT_2,
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Malgun Gothic", 12, "bold"),
            cursor="hand2",
            padx=14,
            pady=9,
        )
        back_btn.pack(fill="x", pady=(4, 0))

    def start_episode(self, index: int) -> None:
        """선택한 에피소드부터 새 테스트 세션을 시작한다."""
        if not 0 <= index < len(self.stages):
            return

        self.cancel_pending()
        self.difficulty = self.difficulty_var.get()
        self.lives = START_LIVES
        self.stage_index = index
        self.round_in_stage = 0
        self.current_task = None
        self.show_story()

    def show_story(self) -> None:
        self.cancel_pending()
        self.clear_buttons()
        self.hide_progress()
        self.set_topbar()

        stage = self.stages[self.stage_index]
        self.title_label.config(text=stage.title)
        self.body_label.config(text=stage.story, font=("Malgun Gothic", 14))
        self.footer.config(
            text=f"난이도: {self.difficulty} · 다음 문제에서 기억할 정보가 잠시 제시됩니다."
        )
        self.add_button("이야기 계속 →", self.begin_round, big=True)

    def begin_round(self) -> None:
        self.current_task = self.stages[self.stage_index].generator(self)
        self.show_memory(self.current_task)

    def show_memory(self, task: Task) -> None:
        if task.presentation == "sequence" and task.sequence:
            self.show_sequence_memory(task)
            return

        self.cancel_pending()
        self.clear_buttons()
        self.set_topbar()

        self.title_label.config(text="기억하세요")
        self.body_label.config(text=task.memory_text, font=("Malgun Gothic", 14))
        self.footer.config(
            text=(task.tip + "  " if task.tip else "")
            + "시간이 끝나면 기억정보가 사라집니다."
        )

        duration = task.memory_ms
        self.run_progress_timer(duration, lambda: self.show_question(task))

    def show_sequence_memory(self, task: Task) -> None:
        """N-Back처럼 항목을 한 번에 하나씩 보여 주는 기억 제시 방식."""
        self.cancel_pending()
        self.clear_buttons()
        self.set_topbar()

        sequence = task.sequence or []
        if not sequence:
            self.show_question(task)
            return

        n_back = DIFFICULTIES[self.difficulty]["nback"]
        self.title_label.config(text=f"숫자를 기억하세요 · {n_back}-Back")
        self.body_label.config(text=task.memory_text, font=("Malgun Gothic", 14))
        self.footer.config(text=task.tip or "숫자는 한 번에 하나씩 표시됩니다.")
        self.update_progress(1.0)

        # 먼저 규칙을 읽을 짧은 시간을 준 뒤 숫자열을 시작한다.
        intro_ms = 1700

        def show_item(index: int) -> None:
            if index >= len(sequence):
                self.body_label.config(text="", font=("Malgun Gothic", 14))
                self.update_progress(0.0)
                aid = self.root.after(350, lambda: self.show_question(task))
                self.after_ids.append(aid)
                return

            self.body_label.config(
                text=sequence[index],
                font=("Malgun Gothic", 48, "bold"),
            )
            self.update_progress((len(sequence) - index) / len(sequence))
            self.footer.config(
                text=f"{index + 1} / {len(sequence)}   ·   {n_back}칸 전 숫자를 계속 유지하세요."
            )

            def blank_then_next() -> None:
                self.body_label.config(text="", font=("Malgun Gothic", 48, "bold"))
                aid2 = self.root.after(task.gap_ms, lambda: show_item(index + 1))
                self.after_ids.append(aid2)

            aid1 = self.root.after(task.item_ms, blank_then_next)
            self.after_ids.append(aid1)

        aid0 = self.root.after(intro_ms, lambda: show_item(0))
        self.after_ids.append(aid0)

    def run_progress_timer(self, duration_ms: int, on_done) -> None:
        self.update_progress(1.0)
        step_ms = 50
        elapsed = 0

        def tick():
            nonlocal elapsed
            elapsed += step_ms
            remain = max(0.0, 1.0 - elapsed / duration_ms)
            self.update_progress(remain)
            if elapsed >= duration_ms:
                self.timer_after_id = None
                on_done()
            else:
                self.timer_after_id = self.root.after(step_ms, tick)

        self.timer_after_id = self.root.after(step_ms, tick)

    def show_question(self, task: Task) -> None:
        self.cancel_pending()
        self.clear_buttons()
        self.hide_progress()
        self.set_topbar()

        self.title_label.config(text="문제")
        self.body_label.config(text=task.question_text, font=("Malgun Gothic", 14))
        self.footer.config(text="기억을 떠올려 정답을 선택하세요.")

        for idx, option in enumerate(task.options):
            self.add_button(
                option,
                lambda i=idx: self.answer(i),
                big=False,
            )

    def answer(self, index: int) -> None:
        if self.current_task is None:
            return

        if index == self.current_task.correct_index:
            self.handle_correct()
        else:
            self.handle_wrong()

    def handle_correct(self) -> None:
        self.cancel_pending()
        self.clear_buttons()
        self.round_in_stage += 1
        self.set_topbar()

        self.title_label.config(text="정답!")
        self.body_label.config(text="앨리스는 기억을 놓치지 않았습니다.", font=("Malgun Gothic", 14))
        self.footer.config(text="")

        if self.round_in_stage >= ROUNDS_PER_STAGE:
            self.add_button("스테이지 완료 →", self.complete_stage, big=True)
        else:
            self.add_button(
                f"다음 문제 ({self.round_in_stage + 1}/{ROUNDS_PER_STAGE})",
                self.begin_round,
                big=True,
            )

    def handle_wrong(self) -> None:
        self.cancel_pending()
        self.clear_buttons()
        self.lives -= 1
        self.set_topbar()

        if self.lives <= 0:
            self.show_game_over()
            return

        self.title_label.config(text="기억이 흔들렸습니다")
        self.body_label.config(
            text=(
                "라이프가 1 감소했습니다.\n\n"
                "정답을 바로 공개하지 않습니다.\n"
                "대신 방금 기억해야 했던 정보를 처음부터 다시 보여 줍니다."
            )
        )
        self.footer.config(text="틀린 뒤 다음 정보가 곧바로 밀려오지 않도록 잠깐 끊어 줍니다.")
        self.add_button("기억정보 다시 보기", self.retry_same_task, big=True)

    def retry_same_task(self) -> None:
        if self.current_task is not None:
            self.show_memory(self.current_task)

    def complete_stage(self) -> None:
        self.round_in_stage = 0

        if self.stage_index >= len(self.stages) - 1:
            self.show_ending()
            return

        self.stage_index += 1
        self.show_story()

    def show_game_over(self) -> None:
        self.cancel_pending()
        self.clear_buttons()
        self.hide_progress()
        self.life_label.config(text="♡" * START_LIVES)

        self.title_label.config(text="GAME OVER")
        self.body_label.config(
            text=(
                "앨리스는 이상한 나라의 혼란 속에서 길을 잃었습니다.\n\n"
                "처음부터 다시 시작하거나 현재 스테이지에서 재도전할 수 있습니다."
            )
        )
        self.footer.config(text="")
        self.add_button("현재 스테이지 다시 시작", self.restart_stage, big=True)
        self.add_button("처음부터", self.show_title_screen, big=False)

    def restart_stage(self) -> None:
        self.lives = START_LIVES
        self.round_in_stage = 0
        self.current_task = None
        self.show_story()

    def show_ending(self) -> None:
        self.cancel_pending()
        self.clear_buttons()
        self.hide_progress()
        self.stage_label.config(text="CLEAR")
        self.life_label.config(text="♥" * self.lives)

        self.title_label.config(text="이상한 나라에서 깨어나다")
        self.body_label.config(
            text=(
                "앨리스가 외칩니다.\n\n"
                "“너희들은 카드 한 벌일 뿐이야!”\n\n"
                "카드들이 한꺼번에 앨리스에게 날아듭니다.\n"
                "그리고 바로 그 순간, 앨리스는 언니의 곁에서 눈을 뜹니다.\n\n"
                "이상한 나라에서 겪은 모든 일은 꿈이었습니다.\n\n"
                f"남은 라이프: {self.lives}/{START_LIVES}\n"
                "축하합니다. 모든 작업기억 스테이지를 통과했습니다!"
            )
        )
        self.footer.config(text="THE END")
        self.add_button("다시 플레이", self.show_title_screen, big=True)


def main() -> None:
    root = tk.Tk()
    AliceMemoryGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()