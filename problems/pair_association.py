# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from typing import List, Tuple

from config import PRESENT_SEQUENCE
from models import Task
from problems.common import make_unique_options


def _pair_settings(difficulty: str) -> Tuple[int, int, int]:
    """등장 쌍 수, 한 쌍 표시시간, 공백시간."""
    if difficulty == "편안하게":
        return 3, 1900, 350
    if difficulty == "도전":
        return 4, 1300, 250
    return 4, 1600, 300


def make_pair_association_task(
    difficulty: str,
    *,
    subjects: List[str],
    objects: List[str],
    intro: str,
    question_template: str = "{target}와 연결되어 있던 것은 무엇인가요?",
) -> Task:
    """대상-사물/개념 대응을 한 쌍씩 순차적으로 보여준다.

    공간 대응과 달리 격자를 사용하지 않는다. 한 화면에 여러 줄을 읽게 하지
    않고, 각 대응관계를 하나씩 보여줘 순수하게 짝을 기억하도록 한다.
    """
    count, item_ms, gap_ms = _pair_settings(difficulty)
    count = min(count, len(subjects), len(objects))

    active_subjects = random.sample(subjects, count)
    active_objects = random.sample(objects, count)
    random.shuffle(active_objects)

    pairs = list(zip(active_subjects, active_objects))
    target, correct = random.choice(pairs)

    sequence = [
        f"{subject}\n\n↕\n\n{obj}"
        for subject, obj in pairs
    ]

    options, correct_index = make_unique_options(
        correct,
        active_objects,
        count=len(active_objects),
    )

    return Task(
        memory_text=(
            intro
            + "\n\n각 인물과 연결된 물건이 한 쌍씩 나타납니다. "
            + "모든 쌍을 기억하세요."
        ),
        question_text=question_template.format(target=target),
        options=options,
        correct_index=correct_index,
        memory_ms=0,
        tip="한 화면에는 한 쌍만 표시됩니다.",
        presentation=PRESENT_SEQUENCE,
        sequence=sequence,
        item_ms=item_ms,
        gap_ms=gap_ms,
    )