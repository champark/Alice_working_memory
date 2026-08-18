# -*- coding: utf-8 -*-
from __future__ import annotations

import random
from typing import List, Tuple


def make_unique_options(
    correct: str,
    pool: List[str],
    count: int = 4,
) -> Tuple[List[str], int]:
    """정답 1개 + 중복 없는 오답을 섞어 반환한다."""
    wrongs = [x for x in pool if x != correct]
    random.shuffle(wrongs)

    options = [correct] + wrongs[: max(0, count - 1)]
    random.shuffle(options)

    return options, options.index(correct)
