# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from typing import List

from config import PRESENT_SEQUENCE, PRESENT_STATIC
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
    presentation: str = PRESENT_STATIC,
    item_ms: int = 900,
    gap_ms: int = 250,
) -> Task:
    """순서 기억 문제.

    PRESENT_STATIC:
        전체 항목을 한 화면에 동시에 표시.

    PRESENT_SEQUENCE:
        항목 하나 표시 -> 공백 -> 다음 항목의 순차 표시.
        이 경우 준비 화면에는 실제 항목 순서를 노출하지 않는다.
    """
    count = item_count(
        difficulty,
        base_count,
        low_count,
        high_count,
    )
    sequence = random.sample(items, count)

    target_index = random.randrange(count)
    correct = sequence[target_index]

    options, correct_index = make_unique_options(
        correct,
        items,
        count=option_count,
    )

    if presentation == PRESENT_SEQUENCE:
        memory_text = intro
        shown_sequence = sequence
        task_memory_ms = 0
    else:
        memory_text = intro + "\n\n" + separator.join(sequence)
        shown_sequence = None
        task_memory_ms = memory_ms(
            difficulty,
            base_memory_ms,
        )

    return Task(
        memory_text=memory_text,
        question_text=question_template.format(
            position=target_index + 1
        ),
        options=options,
        correct_index=correct_index,
        memory_ms=task_memory_ms,
        tip=tip,
        presentation=presentation,
        sequence=shown_sequence,
        item_ms=item_ms,
        gap_ms=gap_ms,
    )