# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from typing import List

from config import ANSWER_GRID_3X3, PRESENT_GRID
from difficulty import memory_ms
from models import Task


POSITION_LABELS = [
    "왼쪽 위", "가운데 위", "오른쪽 위",
    "왼쪽", "가운데", "오른쪽",
    "왼쪽 아래", "가운데 아래", "오른쪽 아래",
]


def _spatial_count(difficulty: str) -> int:
    if difficulty == "편안하게":
        return 3
    if difficulty == "도전":
        return 5
    return 4


def make_spatial_association_task(
    difficulty: str,
    *,
    subjects: List[str],
    intro: str,
    question_template: str = "{target}가 있던 칸을 선택하세요.",
    base_memory_ms: int = 5200,
) -> Task:
    """대상과 '공간 위치'의 대응을 실제 3×3 격자로 기억한다.

    위치 이름을 글자로 읽어서 변환하지 않도록, 기억 단계에서는 대상이
    실제 칸 안에 배치되고 답변 단계에서도 3×3 칸 자체를 클릭한다.
    """
    count = min(_spatial_count(difficulty), len(subjects), 9)
    active_subjects = random.sample(subjects, count)
    active_positions = random.sample(range(9), count)

    grid_cells = [None] * 9
    subject_to_position = {}

    for subject, position in zip(active_subjects, active_positions):
        grid_cells[position] = subject
        subject_to_position[subject] = position

    target = random.choice(active_subjects)
    correct_index = subject_to_position[target]

    return Task(
        memory_text=intro,
        question_text=question_template.format(target=target),
        options=POSITION_LABELS[:],
        correct_index=correct_index,
        memory_ms=memory_ms(difficulty, base_memory_ms),
        tip="이름을 위치 단어로 바꾸지 말고, 보였던 칸 자체를 기억해 보세요.",
        presentation=PRESENT_GRID,
        grid_cells=grid_cells,
        answer_layout=ANSWER_GRID_3X3,
    )