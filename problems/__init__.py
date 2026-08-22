# -*- coding: utf-8 -*-
from .association import make_association_task
from .composite import make_composite_task
from .nback import make_nback_task
from .order import make_order_task
from .pair_association import make_pair_association_task
from .rule_memory import make_rule_memory_task
from .sequence import make_sequence_task
from .spatial import make_grid_task, make_route_task
from .spatial_association import make_spatial_association_task
from .state_tracking import make_delta_task, make_swap_task
from .story_detail import make_story_detail_task

__all__ = [
    "make_association_task",  # 기존 코드 호환용
    "make_composite_task",
    "make_nback_task",
    "make_order_task",
    "make_pair_association_task",
    "make_rule_memory_task",
    "make_sequence_task",
    "make_route_task",
    "make_grid_task",
    "make_spatial_association_task",
    "make_delta_task",
    "make_swap_task",
    "make_story_detail_task",
]