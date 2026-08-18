# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from typing import List, Optional

from config import PRESENT_STATIC
from difficulty import memory_ms
from models import Task
from problems.common import make_unique_options


def make_association_task(
    difficulty: str,
    *,
    left_pool: List[str],
    right_pool: List[str],
    sample_count: int,
    intro: str,
    question_template: str = "{target}와 연결되어 있던 것은 무엇인가요?",
    base_memory_ms: int = 5000,
    option_count: int = 4,
    pair_symbol: str = "↔",
    extra_lines: Optional[List[str]] = None,
) -> Task:
    """A-B 대응 관계를 기억하는 문제."""
    left = random.sample(left_pool, sample_count)
    right = random.sample(right_pool, sample_count)

    pairs = list(zip(left, right))
    target, correct = random.choice(pairs)

    memory = intro + "\n\n"
    memory += "\n".join(f"{a:<8} {pair_symbol} {b}" for a, b in pairs)

    if extra_lines:
        memory += "\n\n" + random.choice(extra_lines)

    options, correct_index = make_unique_options(
        correct,
        right_pool,
        count=option_count,
    )

    return Task(
        memory_text=memory,
        question_text=question_template.format(target=target),
        options=options,
        correct_index=correct_index,
        memory_ms=memory_ms(difficulty, base_memory_ms),
        presentation=PRESENT_STATIC,
    )
