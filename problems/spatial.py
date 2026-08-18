# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from typing import Dict, Tuple

from config import PRESENT_STATIC
from difficulty import grid_move_count, item_count, memory_ms
from models import Task


DIRECTIONS: Dict[str, Tuple[int, int]] = {
    "위": (0, -1),
    "아래": (0, 1),
    "왼쪽": (-1, 0),
    "오른쪽": (1, 0),
}


def make_route_task(
    difficulty: str,
    *,
    intro: str,
    base_count: int = 5,
    low_count: int = 4,
    high_count: int = 7,
    base_memory_ms: int = 5200,
) -> Task:
    """제한 없는 좌표계에서 이동 명령을 추적한다."""
    count = item_count(difficulty, base_count, low_count, high_count)
    moves = [
        random.choice(list(DIRECTIONS.keys()))
        for _ in range(count)
    ]

    x = y = 0
    for move in moves:
        dx, dy = DIRECTIONS[move]
        x += dx
        y += dy

    if x == 0 and y == 0:
        correct = "출발점"
    elif abs(x) >= abs(y):
        correct = "오른쪽" if x > 0 else "왼쪽"
    else:
        correct = "아래쪽" if y > 0 else "위쪽"

    options = [
        "위쪽",
        "아래쪽",
        "왼쪽",
        "오른쪽",
        "출발점",
    ]

    return Task(
        memory_text=(
            intro
            + "\n\n"
            + "  →  ".join(moves)
        ),
        question_text="이동이 끝났을 때 출발점에서 대체로 어느 쪽에 있나요?",
        options=options,
        correct_index=options.index(correct),
        memory_ms=memory_ms(difficulty, base_memory_ms),
        presentation=PRESENT_STATIC,
    )


def make_grid_task(
    difficulty: str,
    *,
    intro: str,
    subject_name: str = "대상",
    base_memory_ms: int = 5200,
) -> Task:
    """3×3 격자 안에서 이동 경로를 추적한다."""
    labels = {
        (0, 0): "왼쪽 위",
        (1, 0): "가운데 위",
        (2, 0): "오른쪽 위",
        (0, 1): "왼쪽",
        (1, 1): "가운데",
        (2, 1): "오른쪽",
        (0, 2): "왼쪽 아래",
        (1, 2): "가운데 아래",
        (2, 2): "오른쪽 아래",
    }

    x = y = 1
    moves = []

    for _ in range(grid_move_count(difficulty)):
        valid = []

        if y > 0:
            valid.append(("위", 0, -1))
        if y < 2:
            valid.append(("아래", 0, 1))
        if x > 0:
            valid.append(("왼쪽", -1, 0))
        if x < 2:
            valid.append(("오른쪽", 1, 0))

        name, dx, dy = random.choice(valid)
        moves.append(name)
        x += dx
        y += dy

    correct = labels[(x, y)]

    all_options = list(labels.values())
    wrongs = [x for x in all_options if x != correct]
    random.shuffle(wrongs)

    options = [correct] + wrongs[:4]
    random.shuffle(options)

    return Task(
        memory_text=(
            intro
            + "\n\n"
            + "이동:\n"
            + "  →  ".join(moves)
        ),
        question_text=f"{subject_name}은 마지막에 어디에 있나요?",
        options=options,
        correct_index=options.index(correct),
        memory_ms=memory_ms(difficulty, base_memory_ms),
        presentation=PRESENT_STATIC,
    )
