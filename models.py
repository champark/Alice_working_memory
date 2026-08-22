# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Optional


@dataclass
class Distractor:
    """기억정보와 본 질문 사이에 끼워 넣는 짧은 방해 과제.

    방해 과제는 작업기억을 잠시 다른 곳에 사용하게 만드는 용도이며,
    기본적으로 라이프나 본 문제 점수에는 영향을 주지 않는다.
    """
    question_text: str
    options: List[str]
    correct_index: int
    duration_ms: int = 7000


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

    # 순차 표시형(N-Back, 규칙 기억 등)에서 사용
    sequence: Optional[List[str]] = None
    item_ms: int = 900
    gap_ms: int = 250

    # 선택 사항:
    # 기억정보 제시가 끝난 뒤 본 질문 전에 수행할 방해 과제.
    distractor: Optional[Distractor] = None

    # 본 기억 질문의 답변 제한시간(ms).
    # None이면 difficulty.py의 공통 제한시간을 사용한다.
    # 특정 문제만 더 길거나 짧게 만들고 싶을 때 개별 지정 가능.
    question_duration_ms: Optional[int] = None


@dataclass
class Stage:
    """에피소드 하나의 스토리와 문제 생성 함수를 묶는다."""
    title: str
    story: str
    generator: Callable[[str], Task]