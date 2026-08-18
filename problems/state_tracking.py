# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from typing import Dict, List

from config import PRESENT_STATIC
from difficulty import item_count, memory_ms, swap_count
from models import Task
from problems.common import make_unique_options


def make_delta_task(
    difficulty: str,
    *,
    positive_label: str,
    negative_label: str,
    positive_result: str,
    negative_result: str,
    zero_result: str,
    intro: str,
    base_count: int = 5,
    low_count: int = 4,
    high_count: int = 7,
    base_memory_ms: int = 5200,
) -> Task:
    """+1/-1 같은 규칙을 누적하여 현재 상태를 추적한다."""
    count = item_count(difficulty, base_count, low_count, high_count)

    moves = [
        random.choice([positive_label, negative_label])
        for _ in range(count)
    ]

    score = sum(
        1 if move == positive_label else -1
        for move in moves
    )

    if score > 0:
        correct = positive_result
    elif score < 0:
        correct = negative_result
    else:
        correct = zero_result

    options = [positive_result, negative_result, zero_result]

    return Task(
        memory_text=(
            intro
            + "\n\n"
            + "  →  ".join(moves)
        ),
        question_text="처음과 비교하면 최종 상태는 어떻게 되었나요?",
        options=options,
        correct_index=options.index(correct),
        memory_ms=memory_ms(difficulty, base_memory_ms),
        presentation=PRESENT_STATIC,
    )


def make_swap_task(
    difficulty: str,
    *,
    people: List[str],
    items: List[str],
    intro: str,
    base_memory_ms: int = 6200,
) -> Task:
    """사람-물건 매칭을 기억한 뒤 여러 차례 교환 결과를 추적한다."""
    shuffled_items = items[:]
    random.shuffle(shuffled_items)

    initial_map: Dict[str, str] = dict(zip(people, shuffled_items))
    current_map = initial_map.copy()

    swaps = []
    for _ in range(swap_count(difficulty)):
        a, b = random.sample(people, 2)
        swaps.append((a, b))
        current_map[a], current_map[b] = current_map[b], current_map[a]

    target = random.choice(people)
    correct = current_map[target]

    memory = intro + "\n\n처음 자리:\n"
    memory += "\n".join(
        f"{person:<8} : {initial_map[person]}"
        for person in people
    )

    memory += "\n\n교환:\n"
    memory += "\n".join(
        f"{a} ↔ {b}"
        for a, b in swaps
    )

    options, correct_index = make_unique_options(
        correct,
        items,
        count=min(4, len(items)),
    )

    return Task(
        memory_text=memory,
        question_text=f"모든 교환이 끝난 뒤 {target}가 가진 것은 무엇인가요?",
        options=options,
        correct_index=correct_index,
        memory_ms=memory_ms(difficulty, base_memory_ms),
        presentation=PRESENT_STATIC,
    )
