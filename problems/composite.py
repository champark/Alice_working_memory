# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from typing import Callable, List

from models import Task


TaskGenerator = Callable[[str], Task]


def make_composite_task(
    difficulty: str,
    *,
    generators: List[TaskGenerator],
    memory_prefix: str = "",
    question_prefix: str = "",
) -> Task:
    """다른 문제 엔진들 중 하나를 무작위 선택하는 종합 문제."""
    generator = random.choice(generators)
    task = generator(difficulty)

    if memory_prefix:
        task.memory_text = memory_prefix + task.memory_text

    if question_prefix:
        task.question_text = question_prefix + task.question_text

    return task
