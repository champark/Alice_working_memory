# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from typing import List

from config import PRESENT_STATIC
from difficulty import item_count, memory_ms
from models import Task
from problems.common import make_unique_options


def make_sequence_task(
    difficulty: str,
    *,
    items: List[str],
    base_count: int,
    low_count: int,
    high_count: int,
    intro: str,
    question_template: str = "{position}번째 물건은 무엇이었나요?",
    separator: str = "  →  ",
    base_memory_ms: int = 4500,
    option_count: int = 4,
    tip: str = "",
) -> Task:
    """여러 항목의 순서를 동시에 보여주고 특정 위치의 항목을 묻는다."""
    count = item_count(difficulty, base_count, low_count, high_count)
    sequence = random.sample(items, count)

    target_index = random.randrange(count)
    correct = sequence[target_index]

    options, correct_index = make_unique_options(
        correct,
        items,
        count=option_count,
    )

    return Task(
        memory_text=intro + "\n\n" + separator.join(sequence),
        question_text=question_template.format(position=target_index + 1),
        options=options,
        correct_index=correct_index,
        memory_ms=memory_ms(difficulty, base_memory_ms),
        tip=tip,
        presentation=PRESENT_STATIC,
    )
