# -*- coding: utf-8 -*-
from __future__ import annotations

import tkinter as tk
from typing import Callable, Optional

from config import (
    ACCENT,
    ACCENT_2,
    APP_TITLE,
    BAD,
    BAR_BG,
    BAR_FG,
    BG,
    BUTTON_ACTIVE,
    BUTTON_BG,
    INK,
    MUTED,
    PANEL,
    ROUNDS_PER_STAGE,
    START_LIVES,
    WINDOW_MIN_HEIGHT,
    WINDOW_MIN_WIDTH,
    WINDOW_SIZE,
)
from difficulty import DIFFICULTIES
from episodes import build_stages
from models import Task
from presentation import TaskPresenter


class AliceMemoryGame:
    def __init__(self, root: tk.Tk):
        self.root = root

        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.minsize(
            WINDOW_MIN_WIDTH,
            WINDOW_MIN_HEIGHT,
        )
        self.root.configure(bg=BG)

        self.difficulty = "보통"
        self.difficulty_var = tk.StringVar(
            value=self.difficulty
        )

        self.lives = START_LIVES
        self.stage_index = 0
        self.round_in_stage = 0
        self.current_task: Optional[Task] = None

        self.enter_action: Optional[
            Callable[[], None]
        ] = None

        self.stages = build_stages()

        self.build_shell()

        self.presenter = TaskPresenter(
            root=self.root,
            body_label=self.body_label,
            footer_label=self.footer,
            progress_updater=self.update_progress,
            clear_buttons=self.clear_buttons,
        )

        self.root.bind(
            "<Return>",
            self._on_enter,
        )
        self.root.bind(
            "<KP_Enter>",
            self._on_enter,
        )

        self.show_title_screen()

    # ========================================================
    # 공통 UI
    # ========================================================

    def build_shell(self) -> None:
        self.topbar = tk.Frame(
            self.root,
            bg=BG,
        )
        self.topbar.pack(
            fill="x",
            padx=24,
            pady=(18, 8),
        )

        self.stage_label = tk.Label(
            self.topbar,
            text="",
            bg=BG,
            fg=INK,
            font=("Malgun Gothic", 12, "bold"),
        )
        self.stage_label.pack(side="left")

        self.life_label = tk.Label(
            self.topbar,
            text="",
            bg=BG,
            fg=BAD,
            font=("Malgun Gothic", 12, "bold"),
        )
        self.life_label.pack(side="right")

        self.main = tk.Frame(
            self.root,
            bg=PANEL,
            highlightbackground="#d8cde9",
            highlightthickness=1,
        )
        self.main.pack(
            fill="both",
            expand=True,
            padx=24,
            pady=(0, 16),
        )

        self.title_label = tk.Label(
            self.main,
            text="",
            bg=PANEL,
            fg=INK,
            font=("Malgun Gothic", 24, "bold"),
            wraplength=800,
            justify="center",
        )
        self.title_label.pack(
            pady=(36, 16)
        )

        self.body_label = tk.Label(
            self.main,
            text="",
            bg=PANEL,
            fg=INK,
            font=("Malgun Gothic", 14),
            wraplength=780,
            justify="center",
            padx=24,
        )
        self.body_label.pack(
            pady=(8, 16),
            fill="x",
        )

        self.progress_canvas = tk.Canvas(
            self.main,
            height=16,
            bg=PANEL,
            highlightthickness=0,
        )
        self.progress_canvas.pack(
            fill="x",
            padx=80,
            pady=(0, 12),
        )
        self.progress_canvas.bind(
            "<Configure>",
            self._redraw_bar_background,
        )

        self.bar_fraction = 0.0

        self.button_frame = tk.Frame(
            self.main,
            bg=PANEL,
        )
        self.button_frame.pack(
            fill="both",
            expand=True,
            padx=70,
            pady=(8, 26),
        )

        self.footer = tk.Label(
            self.root,
            text="",
            bg=BG,
            fg=MUTED,
            font=("Malgun Gothic", 10),
        )
        self.footer.pack(
            pady=(0, 12)
        )

    def clear_buttons(self) -> None:
        for widget in self.button_frame.winfo_children():
            widget.destroy()

    def cancel_pending(self) -> None:
        self.presenter.cancel()

    def set_topbar(self) -> None:
        if 0 <= self.stage_index < len(self.stages):
            self.stage_label.config(
                text=(
                    f"STAGE {self.stage_index + 1}/"
                    f"{len(self.stages)} · "
                    f"{self.round_in_stage}/"
                    f"{ROUNDS_PER_STAGE}"
                )
            )
        else:
            self.stage_label.config(text="")

        self.life_label.config(
            text=(
                "♥" * self.lives
                + "♡" * (
                    START_LIVES - self.lives
                )
            )
        )

    def _redraw_bar_background(
        self,
        _event=None,
    ) -> None:
        self.update_progress(
            self.bar_fraction
        )

    def update_progress(
        self,
        fraction: float,
    ) -> None:
        self.bar_fraction = max(
            0.0,
            min(1.0, fraction),
        )

        self.progress_canvas.delete("all")

        width = max(
            1,
            self.progress_canvas.winfo_width(),
        )
        height = max(
            1,
            self.progress_canvas.winfo_height(),
        )

        self.progress_canvas.create_rectangle(
            0,
            0,
            width,
            height,
            fill=BAR_BG,
            outline="",
        )
        self.progress_canvas.create_rectangle(
            0,
            0,
            width * self.bar_fraction,
            height,
            fill=BAR_FG,
            outline="",
        )

    def hide_progress(self) -> None:
        self.update_progress(0)

    def add_button(
        self,
        text: str,
        command: Callable[[], None],
        *,
        big: bool = False,
    ) -> tk.Button:
        button = tk.Button(
            self.button_frame,
            text=text,
            command=command,
            bg=ACCENT if big else BUTTON_BG,
            fg="white" if big else INK,
            activebackground=(
                ACCENT_2
                if big
                else BUTTON_ACTIVE
            ),
            activeforeground=(
                "white"
                if big
                else INK
            ),
            relief="flat",
            bd=0,
            font=(
                "Malgun Gothic",
                13,
                "bold" if big else "normal",
            ),
            cursor="hand2",
            padx=16,
            pady=12,
            wraplength=620,
        )
        button.pack(
            fill="x",
            pady=6,
        )
        return button

    # ========================================================
    # Enter 키
    # ========================================================

    def set_enter_action(
        self,
        action: Optional[
            Callable[[], None]
        ],
    ) -> None:
        self.enter_action = action

    def _on_enter(self, _event=None):
        action = self.enter_action

        if action is not None:
            action()
            return "break"

        return None

    # ========================================================
    # 시작 화면 / 에피소드 선택
    # ========================================================

    def show_title_screen(self) -> None:
        self.cancel_pending()
        self.set_enter_action(None)

        self.stage_index = 0
        self.round_in_stage = 0
        self.lives = START_LIVES
        self.current_task = None

        self.stage_label.config(text="")
        self.life_label.config(text="")

        self.title_label.config(
            text=(
                "이상한 나라의 앨리스\n"
                "작업기억 어드벤처"
            )
        )
        self.body_label.config(
            text=(
                "흰 토끼를 따라 이상한 나라를 여행하며 "
                "작업기억 문제를 해결하세요.\n\n"
                f"각 스테이지에서 {ROUNDS_PER_STAGE}문제를 "
                "맞히면 다음 장으로 넘어갑니다.\n"
                "틀릴 때마다 라이프가 1 감소하며, "
                "라이프가 0이 되면 게임 오버입니다.\n"
                "오답 뒤에는 같은 기억정보를 다시 보여 주고 "
                "같은 문제를 재도전합니다.\n\n"
                "난이도를 선택하세요."
            ),
            font=("Malgun Gothic", 14),
        )

        self.hide_progress()
        self.footer.config(
            text=(
                "외부 이미지나 파일 없이 Python "
                "표준 라이브러리만으로 실행됩니다."
            )
        )

        self.clear_buttons()
        self.difficulty_var.set(
            self.difficulty
        )

        radio_frame = tk.Frame(
            self.button_frame,
            bg=PANEL,
        )
        radio_frame.pack(
            pady=(4, 18)
        )

        for name in DIFFICULTIES:
            radio = tk.Radiobutton(
                radio_frame,
                text=name,
                variable=self.difficulty_var,
                value=name,
                command=(
                    lambda n=name:
                    self.select_difficulty(n)
                ),
                bg=PANEL,
                fg=INK,
                activebackground=PANEL,
                activeforeground=ACCENT,
                selectcolor=BUTTON_BG,
                font=(
                    "Malgun Gothic",
                    13,
                    "bold",
                ),
                cursor="hand2",
                padx=14,
                pady=8,
            )
            radio.pack(
                side="left",
                padx=10,
            )

        self.add_button(
            "처음부터 플레이 ▶",
            self.start_game,
            big=True,
        )
        self.add_button(
            "에피소드 선택 / 테스트",
            self.show_episode_select,
        )

        self.set_enter_action(
            self.start_game
        )

    def select_difficulty(
        self,
        name: str,
    ) -> None:
        self.difficulty = name
        self.difficulty_var.set(name)

    def start_game(self) -> None:
        self.difficulty = (
            self.difficulty_var.get()
        )
        self.lives = START_LIVES
        self.stage_index = 0
        self.round_in_stage = 0
        self.current_task = None
        self.show_story()

    def show_episode_select(self) -> None:
        self.cancel_pending()
        self.set_enter_action(None)
        self.clear_buttons()
        self.hide_progress()

        self.difficulty = (
            self.difficulty_var.get()
        )

        self.stage_label.config(
            text="EPISODE SELECT"
        )
        self.life_label.config(text="")

        self.title_label.config(
            text="에피소드 선택 / 테스트 모드"
        )
        self.body_label.config(
            text=(
                "수정하거나 시험할 에피소드를 바로 선택하세요.\n"
                "선택한 에피소드부터 라이프 5개로 시작하며, "
                "클리어하면 다음 에피소드로 계속 진행됩니다.\n\n"
                f"현재 난이도: {self.difficulty}"
            ),
            font=("Malgun Gothic", 14),
        )
        self.footer.config(
            text=(
                "테스트용 바로가기입니다. "
                "진행 기록이나 잠금 조건은 없습니다."
            )
        )

        episode_grid = tk.Frame(
            self.button_frame,
            bg=PANEL,
        )
        episode_grid.pack(
            fill="both",
            expand=True,
            pady=(0, 8),
        )
        episode_grid.grid_columnconfigure(
            0,
            weight=1,
        )
        episode_grid.grid_columnconfigure(
            1,
            weight=1,
        )

        for index, stage in enumerate(
            self.stages
        ):
            row = index // 2
            column = index % 2

            button = tk.Button(
                episode_grid,
                text=(
                    f"{index + 1:02d}. "
                    f"{stage.title}"
                ),
                command=(
                    lambda i=index:
                    self.start_episode(i)
                ),
                bg=BUTTON_BG,
                fg=INK,
                activebackground=BUTTON_ACTIVE,
                activeforeground=INK,
                relief="flat",
                bd=0,
                font=(
                    "Malgun Gothic",
                    11,
                    "bold",
                ),
                cursor="hand2",
                padx=10,
                pady=8,
                wraplength=300,
                justify="center",
            )
            button.grid(
                row=row,
                column=column,
                sticky="ew",
                padx=6,
                pady=4,
            )

        back_button = tk.Button(
            self.button_frame,
            text="← 시작 화면으로",
            command=self.show_title_screen,
            bg=ACCENT,
            fg="white",
            activebackground=ACCENT_2,
            activeforeground="white",
            relief="flat",
            bd=0,
            font=(
                "Malgun Gothic",
                12,
                "bold",
            ),
            cursor="hand2",
            padx=14,
            pady=9,
        )
        back_button.pack(
            fill="x",
            pady=(4, 0),
        )

    def start_episode(
        self,
        index: int,
    ) -> None:
        if not 0 <= index < len(
            self.stages
        ):
            return

        self.cancel_pending()
        self.difficulty = (
            self.difficulty_var.get()
        )
        self.lives = START_LIVES
        self.stage_index = index
        self.round_in_stage = 0
        self.current_task = None
        self.show_story()

    # ========================================================
    # 스토리 → 준비 → 기억정보 → 문제
    # ========================================================

    def show_story(self) -> None:
        self.cancel_pending()
        self.set_enter_action(None)
        self.clear_buttons()
        self.hide_progress()
        self.set_topbar()

        stage = self.stages[
            self.stage_index
        ]

        self.title_label.config(
            text=stage.title
        )
        self.body_label.config(
            text=stage.story,
            font=("Malgun Gothic", 14),
        )
        self.footer.config(
            text=(
                f"난이도: {self.difficulty} · "
                "Enter 키로도 계속할 수 있습니다."
            )
        )

        self.add_button(
            "이야기 계속 →",
            self.begin_round,
            big=True,
        )
        self.set_enter_action(
            self.begin_round
        )

    def begin_round(self) -> None:
        self.set_enter_action(None)

        stage = self.stages[
            self.stage_index
        ]
        self.current_task = stage.generator(
            self.difficulty
        )

        self.show_task_ready(
            self.current_task
        )

    def show_task_ready(
        self,
        task: Task,
        *,
        retry: bool = False,
    ) -> None:
        self.cancel_pending()
        self.set_enter_action(None)
        self.clear_buttons()
        self.hide_progress()
        self.set_topbar()

        if retry:
            self.title_label.config(
                text="재도전 준비"
            )
            intro = (
                "방금 문제의 기억정보를 처음부터 다시 보여 줍니다.\n\n"
                "준비가 되었을 때 시작하세요."
            )
        else:
            self.title_label.config(
                text="문제 준비"
            )
            intro = (
                f"{self.round_in_stage + 1}/"
                f"{ROUNDS_PER_STAGE}번째 문제입니다.\n\n"
                "준비가 되었을 때 시작하세요."
            )

        if (
            task.presentation == "sequence"
        ):
            intro += (
                "\n\n"
                + task.memory_text
            )
        else:
            intro += (
                "\n\n시작하면 기억정보가 제한된 시간 동안 "
                "표시된 뒤 자동으로 사라집니다."
            )

        self.body_label.config(
            text=intro,
            font=("Malgun Gothic", 14),
        )
        self.footer.config(
            text=(
                (task.tip + "  " if task.tip else "")
                + "마우스로 버튼을 누르거나 "
                "Enter 키를 누르세요."
            )
        )

        def start_action() -> None:
            self.show_memory(task)

        self.add_button(
            "준비 완료 · 시작 ▶",
            start_action,
            big=True,
        )
        self.set_enter_action(
            start_action
        )

    def show_memory(
        self,
        task: Task,
    ) -> None:
        self.set_enter_action(None)
        self.clear_buttons()
        self.set_topbar()

        self.title_label.config(
            text="기억하세요"
        )

        self.presenter.present(
            task,
            on_done=(
                lambda:
                self.show_question(task)
            ),
        )

    def show_question(
        self,
        task: Task,
    ) -> None:
        self.cancel_pending()
        self.set_enter_action(None)
        self.clear_buttons()
        self.hide_progress()
        self.set_topbar()

        self.title_label.config(
            text="문제"
        )
        self.body_label.config(
            text=task.question_text,
            font=("Malgun Gothic", 14),
        )
        self.footer.config(
            text="기억을 떠올려 정답을 선택하세요."
        )

        for index, option in enumerate(
            task.options
        ):
            self.add_button(
                option,
                lambda i=index:
                self.answer(i),
            )

    # ========================================================
    # 정답/오답
    # ========================================================

    def answer(
        self,
        index: int,
    ) -> None:
        if self.current_task is None:
            return

        if (
            index
            == self.current_task.correct_index
        ):
            self.handle_correct()
        else:
            self.handle_wrong()

    def handle_correct(self) -> None:
        self.cancel_pending()
        self.set_enter_action(None)
        self.clear_buttons()

        self.round_in_stage += 1
        self.set_topbar()

        self.title_label.config(
            text="정답!"
        )
        self.body_label.config(
            text="앨리스는 기억을 놓치지 않았습니다.",
            font=("Malgun Gothic", 14),
        )
        self.footer.config(text="")

        if (
            self.round_in_stage
            >= ROUNDS_PER_STAGE
        ):
            self.add_button(
                "스테이지 완료 →",
                self.complete_stage,
                big=True,
            )
            self.set_enter_action(
                self.complete_stage
            )
        else:
            self.add_button(
                (
                    "다음 문제 준비 "
                    f"({self.round_in_stage + 1}/"
                    f"{ROUNDS_PER_STAGE})"
                ),
                self.begin_round,
                big=True,
            )
            self.set_enter_action(
                self.begin_round
            )

    def handle_wrong(self) -> None:
        self.cancel_pending()
        self.set_enter_action(None)
        self.clear_buttons()

        self.lives -= 1
        self.set_topbar()

        if self.lives <= 0:
            self.show_game_over()
            return

        self.title_label.config(
            text="기억이 흔들렸습니다"
        )
        self.body_label.config(
            text=(
                "라이프가 1 감소했습니다.\n\n"
                "정답을 바로 공개하지 않습니다.\n"
                "대신 방금 기억해야 했던 정보를 "
                "처음부터 다시 보여 줍니다."
            ),
            font=("Malgun Gothic", 14),
        )
        self.footer.config(
            text=(
                "준비가 되면 버튼 또는 Enter로 "
                "같은 문제를 다시 시작하세요."
            )
        )

        self.add_button(
            "재도전 준비 →",
            self.retry_same_task,
            big=True,
        )
        self.set_enter_action(
            self.retry_same_task
        )

    def retry_same_task(self) -> None:
        if self.current_task is not None:
            self.show_task_ready(
                self.current_task,
                retry=True,
            )

    # ========================================================
    # 스테이지 진행 / 게임오버 / 엔딩
    # ========================================================

    def complete_stage(self) -> None:
        self.round_in_stage = 0

        if (
            self.stage_index
            >= len(self.stages) - 1
        ):
            self.show_ending()
            return

        self.stage_index += 1
        self.current_task = None
        self.show_story()

    def show_game_over(self) -> None:
        self.cancel_pending()
        self.set_enter_action(None)
        self.clear_buttons()
        self.hide_progress()

        self.life_label.config(
            text="♡" * START_LIVES
        )

        self.title_label.config(
            text="GAME OVER"
        )
        self.body_label.config(
            text=(
                "앨리스는 이상한 나라의 혼란 속에서 "
                "길을 잃었습니다.\n\n"
                "처음부터 다시 시작하거나 현재 스테이지에서 "
                "재도전할 수 있습니다."
            ),
            font=("Malgun Gothic", 14),
        )
        self.footer.config(text="")

        self.add_button(
            "현재 스테이지 다시 시작",
            self.restart_stage,
            big=True,
        )
        self.add_button(
            "처음부터",
            self.show_title_screen,
        )

    def restart_stage(self) -> None:
        self.lives = START_LIVES
        self.round_in_stage = 0
        self.current_task = None
        self.show_story()

    def show_ending(self) -> None:
        self.cancel_pending()
        self.set_enter_action(None)
        self.clear_buttons()
        self.hide_progress()

        self.stage_label.config(
            text="CLEAR"
        )
        self.life_label.config(
            text="♥" * self.lives
        )

        self.title_label.config(
            text="이상한 나라에서 깨어나다"
        )
        self.body_label.config(
            text=(
                "앨리스가 외칩니다.\n\n"
                "“너희들은 카드 한 벌일 뿐이야!”\n\n"
                "카드들이 한꺼번에 앨리스에게 날아듭니다.\n"
                "그리고 바로 그 순간, 앨리스는 언니의 곁에서 "
                "눈을 뜹니다.\n\n"
                "이상한 나라에서 겪은 모든 일은 꿈이었습니다.\n\n"
                f"남은 라이프: {self.lives}/{START_LIVES}\n"
                "축하합니다. 모든 작업기억 스테이지를 통과했습니다!"
            ),
            font=("Malgun Gothic", 14),
        )
        self.footer.config(
            text="THE END"
        )

        self.add_button(
            "다시 플레이",
            self.show_title_screen,
            big=True,
        )