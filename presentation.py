# -*- coding: utf-8 -*-
from __future__ import annotations

import tkinter as tk
from typing import Callable, List, Optional

from config import PRESENT_SEQUENCE
from models import Task


class TaskPresenter:
    """기억정보의 '표시 방식'만 담당한다.

    static:
        전체 기억정보를 일정 시간 동시에 보여 준다.

    sequence:
        항목을 하나씩 표시하고 사이에 빈 화면을 넣는다.

    문제 규칙은 전혀 알지 못한다.
    """

    def __init__(
        self,
        root: tk.Tk,
        body_label: tk.Label,
        footer_label: tk.Label,
        progress_updater: Callable[[float], None],
        clear_buttons: Callable[[], None],
    ):
        self.root = root
        self.body_label = body_label
        self.footer_label = footer_label
        self.progress_updater = progress_updater
        self.clear_buttons = clear_buttons

        self.after_ids: List[str] = []
        self.timer_after_id: Optional[str] = None

    def cancel(self) -> None:
        for after_id in self.after_ids:
            try:
                self.root.after_cancel(after_id)
            except tk.TclError:
                pass
        self.after_ids.clear()

        if self.timer_after_id is not None:
            try:
                self.root.after_cancel(self.timer_after_id)
            except tk.TclError:
                pass
            self.timer_after_id = None

    def present(
        self,
        task: Task,
        *,
        on_done: Callable[[], None],
    ) -> None:
        self.cancel()
        self.clear_buttons()

        if task.presentation == PRESENT_SEQUENCE and task.sequence:
            self._present_sequence(task, on_done)
        else:
            self._present_static(task, on_done)

    def _present_static(
        self,
        task: Task,
        on_done: Callable[[], None],
    ) -> None:
        self.body_label.config(
            text=task.memory_text,
            font=("Malgun Gothic", 14),
        )
        self.footer_label.config(
            text=(
                (task.tip + "  " if task.tip else "")
                + "시간이 끝나면 기억정보가 사라집니다."
            )
        )

        duration = max(1, task.memory_ms)
        self._run_progress_timer(duration, on_done)

    def _run_progress_timer(
        self,
        duration_ms: int,
        on_done: Callable[[], None],
    ) -> None:
        self.progress_updater(1.0)

        step_ms = 50
        elapsed = 0

        def tick() -> None:
            nonlocal elapsed

            elapsed += step_ms
            remain = max(
                0.0,
                1.0 - elapsed / duration_ms,
            )
            self.progress_updater(remain)

            if elapsed >= duration_ms:
                self.timer_after_id = None
                on_done()
            else:
                self.timer_after_id = self.root.after(
                    step_ms,
                    tick,
                )

        self.timer_after_id = self.root.after(
            step_ms,
            tick,
        )

    def _sequence_font(self, text: str):
        """순차 표시 텍스트 길이에 따라 폰트 크기를 조절한다."""
        stripped = text.strip()

        if "\n" in stripped:
            return ("Malgun Gothic", 24, "bold")
        if len(stripped) >= 14:
            return ("Malgun Gothic", 24, "bold")
        if len(stripped) >= 8:
            return ("Malgun Gothic", 30, "bold")
        return ("Malgun Gothic", 42, "bold")

    def _present_sequence(
        self,
        task: Task,
        on_done: Callable[[], None],
    ) -> None:
        sequence = task.sequence or []
        self.progress_updater(0.0)

        def show_item(index: int) -> None:
            if index >= len(sequence):
                self.body_label.config(
                    text="",
                    font=("Malgun Gothic", 14),
                )
                on_done()
                return

            current_text = str(sequence[index])

            self.body_label.config(
                text=current_text,
                font=self._sequence_font(current_text),
                justify="center",
            )
            self.footer_label.config(
                text=f"{index + 1} / {len(sequence)}"
            )
            self.progress_updater(
                (index + 1) / len(sequence)
            )

            after_show = self.root.after(
                task.item_ms,
                lambda i=index: show_gap(i),
            )
            self.after_ids.append(after_show)

        def show_gap(index: int) -> None:
            self.body_label.config(
                text="",
                font=("Malgun Gothic", 14),
            )

            after_gap = self.root.after(
                task.gap_ms,
                lambda: show_item(index + 1),
            )
            self.after_ids.append(after_gap)

        # 준비 화면에서 이미 사용자가 시작을 눌렀으므로 즉시 시작
        show_item(0)