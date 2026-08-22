# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Dict, Tuple


DIFFICULTIES: Dict[str, dict] = {
    "편안하게": {
        "memory_ms_mul": 1.35,
        "item_delta": -1,
        "nback": 1,
        "nback_item_ms": 1200,
        "nback_gap_ms": 320,
        "swap_count": 1,
        "grid_moves": 3,
        "question_time_ms": 12000,
    },
    "보통": {
        "memory_ms_mul": 1.00,
        "item_delta": 0,
        "nback": 2,
        "nback_item_ms": 900,
        "nback_gap_ms": 250,
        "swap_count": 2,
        "grid_moves": 4,
        "question_time_ms": 9000,
    },
    "도전": {
        "memory_ms_mul": 0.78,
        "item_delta": 1,
        "nback": 2,
        "nback_item_ms": 650,
        "nback_gap_ms": 200,
        "swap_count": 3,
        "grid_moves": 5,
        "question_time_ms": 7000,
    },
}


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def memory_ms(difficulty: str, base_ms: int) -> int:
    mul = DIFFICULTIES[difficulty]["memory_ms_mul"]
    return int(base_ms * mul)


def item_count(
    difficulty: str,
    base: int,
    low: int = 3,
    high: int = 8,
) -> int:
    delta = DIFFICULTIES[difficulty]["item_delta"]
    return clamp(base + delta, low, high)


def nback_timing(difficulty: str) -> Tuple[int, int]:
    profile = DIFFICULTIES[difficulty]
    return profile["nback_item_ms"], profile["nback_gap_ms"]


def nback_level(difficulty: str) -> int:
    return DIFFICULTIES[difficulty]["nback"]


def swap_count(difficulty: str) -> int:
    return DIFFICULTIES[difficulty]["swap_count"]


def grid_move_count(difficulty: str) -> int:
    return DIFFICULTIES[difficulty]["grid_moves"]



def question_time_limit(difficulty: str) -> int:
    """모든 일반 기억 문제의 기본 답변 제한시간(ms).

    개별 Task가 별도 제한시간을 지정하지 않은 경우 이 값을 사용한다.
    """
    return DIFFICULTIES[difficulty]["question_time_ms"]