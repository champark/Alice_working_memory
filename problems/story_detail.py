# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from typing import Dict, List

from config import PRESENT_STATIC
from difficulty import memory_ms
from models import Task
from problems.common import make_unique_options


def make_story_detail_task(
    difficulty: str,
    *,
    category_pools: Dict[str, List[str]],
    intro_template: str,
    question_templates: Dict[str, str],
    base_memory_ms: int = 6000,
) -> Task:
    """짧은 이야기 속 여러 속성을 기억하는 문제."""
    facts = {
        key: random.choice(pool)
        for key, pool in category_pools.items()
    }

    memory_text = intro_template.format(**facts)

    target_key = random.choice(list(category_pools.keys()))
    correct = facts[target_key]

    options, correct_index = make_unique_options(
        correct,
        category_pools[target_key],
    )

    return Task(
        memory_text=memory_text,
        question_text=question_templates[target_key],
        options=options,
        correct_index=correct_index,
        memory_ms=memory_ms(difficulty, base_memory_ms),
        presentation=PRESENT_STATIC,
    )
