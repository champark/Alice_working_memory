# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from typing import Dict, List, Tuple

from config import PRESENT_SEQUENCE
from models import Task
from problems.common import make_unique_options


def _rule_memory_settings(
    difficulty: str,
) -> Tuple[int, int, int]:
    """규칙 기억 문제 난이도.

    반환:
        입력 순서 길이,
        한 화면 표시 시간(ms),
        화면 사이 공백(ms)
    """
    if difficulty == "편안하게":
        return 3, 1900, 400

    if difficulty == "도전":
        return 5, 1300, 260

    # 보통
    return 4, 1600, 320


def make_rule_memory_task(
    difficulty: str,
    *,
    rule_keys: List[str],
    rule_values: List[str],
    intro: str,
    question_template: str = (
        "{position}번째로 나온 선택은 "
        "어떤 변화를 일으키나요?"
    ),
) -> Task:
    """규칙을 먼저 기억한 뒤, 나중에 나온 입력에 적용하는 문제.

    진행:
        1. 규칙 A를 일정 시간 표시
        2. 규칙 B를 일정 시간 표시
        3. 규칙은 사라짐
        4. 입력들이 하나씩 표시
        5. 특정 순서의 입력이 어떤 결과를 만드는지 질문

    규칙과 입력을 동시에 볼 수 없기 때문에
    단순 계산이 아니라 '규칙 유지 + 순서 기억 + 규칙 적용'이 필요하다.
    """
    if len(rule_keys) != len(rule_values):
        raise ValueError("rule_keys와 rule_values의 길이는 같아야 합니다.")

    if len(rule_keys) < 2:
        raise ValueError("규칙 기억 문제에는 최소 2개의 규칙이 필요합니다.")

    sequence_length, item_ms, gap_ms = _rule_memory_settings(
        difficulty
    )

    # 매 문제마다 규칙의 대응관계를 섞는다.
    # 따라서 이전 문제의 규칙을 외워서 풀 수 없다.
    shuffled_values = rule_values[:]
    random.shuffle(shuffled_values)

    rule_map: Dict[str, str] = dict(
        zip(rule_keys, shuffled_values)
    )

    inputs = [
        random.choice(rule_keys)
        for _ in range(sequence_length)
    ]

    target_index = random.randrange(
        sequence_length
    )
    target_key = inputs[target_index]
    correct = rule_map[target_key]

    options, correct_index = make_unique_options(
        correct,
        rule_values,
        count=len(rule_values),
    )

    sequence_steps: List[str] = []

    # 규칙 자체도 한꺼번에 보여주지 않는다.
    for number, key in enumerate(
        rule_keys,
        start=1,
    ):
        sequence_steps.append(
            f"규칙 {number}/{len(rule_keys)}\n\n"
            f"{key}\n\n→\n\n"
            f"{rule_map[key]}"
        )

    sequence_steps.append(
        "규칙이 사라집니다\n\n"
        "이제 버섯 선택의 순서를 기억하세요"
    )

    # 실제 입력도 하나씩 보여준다.
    for number, key in enumerate(
        inputs,
        start=1,
    ):
        sequence_steps.append(
            f"{number}번째\n\n{key}"
        )

    return Task(
        memory_text=(
            intro
            + "\n\n"
            + "먼저 규칙이 하나씩 나타납니다.\n"
            + "규칙이 사라진 뒤 버섯 선택이 하나씩 나타납니다.\n"
            + "규칙과 순서를 함께 기억하세요."
        ),
        question_text=question_template.format(
            position=target_index + 1
        ),
        options=options,
        correct_index=correct_index,
        memory_ms=0,
        tip=(
            "이번 문제의 규칙은 매번 달라질 수 있습니다. "
            "이전 문제의 규칙을 그대로 적용하지 마세요."
        ),
        presentation=PRESENT_SEQUENCE,
        sequence=sequence_steps,
        item_ms=item_ms,
        gap_ms=gap_ms,
    )