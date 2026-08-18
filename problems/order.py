# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from typing import List

from config import PRESENT_STATIC
from difficulty import item_count, memory_ms
from models import Task
from problems.common import make_unique_options


def make_order_task(
    difficulty: str,
    *,
    items: List[str],
    base_count: int = 5,
    low_count: int = 4,
    high_count: int = 6,
    intro: str = "순서를 기억하세요.",
    base_memory_ms: int = 5000,
) -> Task:
    """순위/전후 관계를 기억하는 문제."""
    ordered = random.sample(
        items,
        item_count(difficulty, base_count, low_count, high_count),
    )

    # 현재는 '바로 앞' 질문을 기본으로 사용한다.
    # 추후 before / after / position / between 모드를 쉽게 추가할 수 있다.
    target_index = random.randrange(1, len(ordered))
    target = ordered[target_index]
    correct = ordered[target_index - 1]

    options, correct_index = make_unique_options(correct, ordered)

    memory = intro + "\n\n"
    memory += "\n".join(
        f"{index + 1}위  {name}"
        for index, name in enumerate(ordered)
    )

    return Task(
        memory_text=memory,
        question_text=f"{target} 바로 앞에 있던 참가자는 누구였나요?",
        options=options,
        correct_index=correct_index,
        memory_ms=memory_ms(difficulty, base_memory_ms),
        presentation=PRESENT_STATIC,
    )
