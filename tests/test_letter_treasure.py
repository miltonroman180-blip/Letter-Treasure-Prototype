import unittest

from src.letter_treasure import LetterState, LetterTreasureGame


class LetterTreasureGameTests(unittest.TestCase):
    def test_win_flow(self):
        game = LetterTreasureGame("apple", max_attempts=3)
        feedback = game.guess("apple")

        self.assertTrue(game.is_won)
        self.assertTrue(game.is_finished)
        self.assertEqual(game.attempts_left, 2)
        self.assertEqual(feedback.states, [LetterState.CORRECT] * 5)

    def test_duplicate_letter_evaluation(self):
        game = LetterTreasureGame("apple", max_attempts=6)
        feedback = game.guess("allee")

        self.assertEqual(
            feedback.states,
            [
                LetterState.CORRECT,
                LetterState.PRESENT,
                LetterState.ABSENT,
                LetterState.ABSENT,
                LetterState.CORRECT,
            ],
        )

    def test_invalid_guess_length(self):
        game = LetterTreasureGame("apple")
        with self.assertRaises(ValueError):
            game.guess("app")

    def test_game_cannot_continue_after_finish(self):
        game = LetterTreasureGame("apple", max_attempts=1)
        game.guess("brave")
        self.assertTrue(game.is_finished)
        with self.assertRaises(RuntimeError):
            game.guess("apple")


if __name__ == "__main__":
    unittest.main()
