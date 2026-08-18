# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional


@dataclass
class Task:
    """문제 엔진이 UI에 넘기는 공통 문제 데이터."""
    memory_text: str
    question_text: str
    options: List[str]
    correct_index: int
    memory_ms: int

    tip: str = ""
    presentation: str = "static"

    # 순차 표시형(N-Back 등)에서 사용
    sequence: Optional[List[str]] = None
    item_ms: int = 900
    gap_ms: int = 250


@dataclass
class Stage:
    """에피소드 하나의 스토리와 문제 생성 함수를 묶는다."""
    title: str
    story: str
    generator: Callable[[str], Task]
