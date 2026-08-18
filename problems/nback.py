# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from typing import List

from config import PRESENT_SEQUENCE
from difficulty import item_count, nback_level, nback_timing
from models import Task


def make_nback_task(
    difficulty: str,
    *,
    item_pool: List[str] | None = None,
    base_length: int = 7,
    low_length: int = 6,
    high_length: int = 9,
    intro: str = "항목이 하나씩 지나갑니다.",
    noun: str = "항목",
) -> Task:
    """N칸 전 정보와 마지막 정보를 비교하는 순차 표시 문제."""
    if item_pool is None:
        item_pool = [str(i) for i in range(1, 10)]

    n_back = nback_level(difficulty)
    length = item_count(
        difficulty,
        base_length,
        low_length,
        high_length,
    )

    sequence = [
        random.choice(item_pool)
        for _ in range(length)
    ]

    want_same = random.choice([True, False])

    if want_same:
        sequence[-1] = sequence[-1 - n_back]
    else:
        forbidden = sequence[-1 - n_back]
        choices = [x for x in item_pool if x != forbidden]
        sequence[-1] = random.choice(choices)

    item_ms, gap_ms = nback_timing(difficulty)

    return Task(
        memory_text=(
            f"{intro}\n\n"
            f"각 {noun}을 보면서 {n_back}칸 전 {noun}을 계속 기억하세요.\n"
            "마지막 항목이 사라진 뒤 질문이 나옵니다."
        ),
        question_text=f"마지막 {noun}은 {n_back}칸 전 {noun}과 같았나요?",
        options=["같다", "다르다"],
        correct_index=0 if want_same else 1,
        memory_ms=0,
        tip=(
            "한 번에 하나씩만 표시됩니다. "
            "오답 시 같은 순서를 처음부터 다시 보여 줍니다."
        ),
        presentation=PRESENT_SEQUENCE,
        sequence=sequence,
        item_ms=item_ms,
        gap_ms=gap_ms,
    )
