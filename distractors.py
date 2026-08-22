# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from typing import List

from models import Distractor


def _math_time_limit(difficulty: str) -> int:
    """산수 방해 과제 제한시간(ms).

    너무 촉박하면 산수 속도를 평가하게 되므로
    '간섭은 주되 충분히 풀 수 있는 시간'으로 설정한다.
    """
    if difficulty == "편안하게":
        return 9000

    if difficulty == "도전":
        return 6000

    # 보통
    return 7500


def _make_options(correct: int, spread: int = 4) -> tuple[List[str], int]:
    """정답 주변 숫자로 4지선다 보기를 만든다."""
    candidates = {correct}

    offsets = [-spread, -3, -2, -1, 1, 2, 3, spread]
    random.shuffle(offsets)

    for offset in offsets:
        value = correct + offset
        if value >= 0:
            candidates.add(value)
        if len(candidates) >= 4:
            break

    # 혹시 정답이 0 근처라 후보가 부족한 경우 보충
    value = 0
    while len(candidates) < 4:
        candidates.add(value)
        value += 1

    options_int = list(candidates)
    random.shuffle(options_int)

    options = [str(x) for x in options_int]
    return options, options_int.index(correct)


def make_simple_math_distractor(difficulty: str) -> Distractor:
    """프롤로그 등에 사용할 짧은 산수 방해 과제.

    이 문제 자체를 어렵게 만드는 것이 목적이 아니다.
    사용자가 기억해 둔 정보를 잠시 내려놓고 다른 처리를 하게 만든 뒤
    다시 원래 기억을 꺼내도록 하는 것이 목적이다.
    """

    if difficulty == "편안하게":
        # 한 자리수 덧셈 위주
        a = random.randint(2, 8)
        b = random.randint(1, 7)
        answer = a + b
        expression = f"{a} + {b}"

    elif difficulty == "도전":
        # 그래도 프롤로그이므로 복잡한 암산은 피한다.
        if random.choice([True, False]):
            a = random.randint(11, 24)
            b = random.randint(3, 9)
            answer = a + b
            expression = f"{a} + {b}"
        else:
            a = random.randint(14, 29)
            b = random.randint(3, min(9, a))
            answer = a - b
            expression = f"{a} - {b}"

    else:
        # 보통: 20 안팎의 간단한 덧셈/뺄셈
        if random.choice([True, False]):
            a = random.randint(5, 14)
            b = random.randint(2, 9)
            answer = a + b
            expression = f"{a} + {b}"
        else:
            a = random.randint(9, 20)
            b = random.randint(2, min(8, a))
            answer = a - b
            expression = f"{a} - {b}"

    options, correct_index = _make_options(answer)

    return Distractor(
        question_text=(
            "잠깐 다른 생각을 해봅시다.\n\n"
            f"{expression} = ?"
        ),
        options=options,
        correct_index=correct_index,
        duration_ms=_math_time_limit(difficulty),
    )