from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
import random
from typing import List


class LetterState(str, Enum):
    CORRECT = "correct"
    PRESENT = "present"
    ABSENT = "absent"


@dataclass(frozen=True)
class GuessFeedback:
    guess: str
    states: List[LetterState]


@dataclass
class GameResult:
    won: bool
    target_word: str
    attempts_used: int


class LetterTreasureGame:
    def __init__(self, target_word: str, max_attempts: int = 6) -> None:
        target_word = target_word.lower().strip()
        if not target_word.isalpha():
            raise ValueError("target_word must contain only letters")
        if max_attempts <= 0:
            raise ValueError("max_attempts must be positive")

        self.target_word = target_word
        self.max_attempts = max_attempts
        self.word_length = len(target_word)
        self.attempts_used = 0
        self.is_won = False

    def guess(self, candidate: str) -> GuessFeedback:
        if self.is_finished:
            raise RuntimeError("game is already finished")

        candidate = candidate.lower().strip()
        if len(candidate) != self.word_length:
            raise ValueError(f"guess must be {self.word_length} letters")
        if not candidate.isalpha():
            raise ValueError("guess must contain only letters")

        self.attempts_used += 1
        states = self._evaluate_guess(candidate)
        if candidate == self.target_word:
            self.is_won = True

        return GuessFeedback(guess=candidate, states=states)

    @property
    def attempts_left(self) -> int:
        return self.max_attempts - self.attempts_used

    @property
    def is_finished(self) -> bool:
        return self.is_won or self.attempts_used >= self.max_attempts

    def result(self) -> GameResult:
        return GameResult(
            won=self.is_won,
            target_word=self.target_word,
            attempts_used=self.attempts_used,
        )

    def _evaluate_guess(self, candidate: str) -> List[LetterState]:
        # Two-pass evaluation to handle duplicated letters.
        states: List[LetterState | None] = [None] * self.word_length
        remaining_target_chars: dict[str, int] = {}

        for i, (g_char, t_char) in enumerate(zip(candidate, self.target_word)):
            if g_char == t_char:
                states[i] = LetterState.CORRECT
            else:
                remaining_target_chars[t_char] = remaining_target_chars.get(t_char, 0) + 1

        for i, g_char in enumerate(candidate):
            if states[i] is not None:
                continue

            count = remaining_target_chars.get(g_char, 0)
            if count > 0:
                states[i] = LetterState.PRESENT
                remaining_target_chars[g_char] = count - 1
            else:
                states[i] = LetterState.ABSENT

        return [s for s in states if s is not None]


DEFAULT_WORDS = [
    "apple",
    "brave",
    "charm",
    "dunes",
    "eagle",
]


def create_random_game(max_attempts: int = 6) -> LetterTreasureGame:
    return LetterTreasureGame(target_word=random.choice(DEFAULT_WORDS), max_attempts=max_attempts)


def _render_feedback(feedback: GuessFeedback) -> str:
    mapping = {
        LetterState.CORRECT: "🟩",
        LetterState.PRESENT: "🟨",
        LetterState.ABSENT: "⬜",
    }
    return "".join(mapping[state] for state in feedback.states)


def run_cli() -> None:
    game = create_random_game()
    print(f"Welcome to Letter Treasure! Target word length: {game.word_length}")
    print(f"You have {game.max_attempts} attempts. Good luck!\n")

    while not game.is_finished:
        guess = input(f"Enter your guess ({game.word_length} letters): ")
        try:
            feedback = game.guess(guess)
        except ValueError as exc:
            print(f"Invalid guess: {exc}\n")
            continue

        print(_render_feedback(feedback))
        print(f"Attempts left: {game.attempts_left}\n")

    result = game.result()
    if result.won:
        print(f"🎉 You found the treasure word '{result.target_word}' in {result.attempts_used} attempts!")
    else:
        print(f"💡 Out of attempts! The treasure word was '{result.target_word}'.")


if __name__ == "__main__":
    run_cli()
