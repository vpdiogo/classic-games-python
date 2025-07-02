"""
Unit tests for high score system
"""

import unittest
import tempfile
import os
from pathlib import Path
from snake_game.high_score import HighScoreManager


class TestHighScoreManager(unittest.TestCase):
    """Tests for HighScoreManager class"""

    def setUp(self):
        """Setup for each test with temporary file"""
        self.temp_file = tempfile.NamedTemporaryFile(
            mode='w', delete=False, suffix='.json'
        )
        self.temp_file.close()
        self.temp_path = self.temp_file.name
        self.manager = HighScoreManager(file_path=self.temp_path, max_scores=3)

    def tearDown(self):
        """Cleanup temporary file"""
        if os.path.exists(self.temp_path):
            os.unlink(self.temp_path)

    def test_empty_high_scores(self):
        """Test initial state with no high scores"""
        self.assertEqual(self.manager.get_high_score(), 0)
        self.assertEqual(len(self.manager.get_top_scores()), 0)
        self.assertEqual(self.manager.get_lowest_high_score(), 0)

    def test_add_first_score(self):
        """Test adding first score"""
        is_high_score = self.manager.add_score(100, "Player1")

        self.assertTrue(is_high_score)
        self.assertEqual(self.manager.get_high_score(), 100)
        self.assertEqual(len(self.manager.get_top_scores()), 1)

    def test_add_multiple_scores(self):
        """Test adding multiple scores"""
        scores = [(100, "Player1"), (200, "Player2"), (150, "Player3")]

        for score, player in scores:
            self.manager.add_score(score, player)

        # Check order (highest first)
        top_scores = self.manager.get_top_scores()
        self.assertEqual(len(top_scores), 3)
        self.assertEqual(top_scores[0]["score"], 200)
        self.assertEqual(top_scores[1]["score"], 150)
        self.assertEqual(top_scores[2]["score"], 100)

    def test_max_scores_limit(self):
        """Test that only max_scores are kept"""
        # Add more scores than the limit
        for i in range(5):
            self.manager.add_score(i * 10, f"Player{i}")

        # Should only keep top 3
        top_scores = self.manager.get_top_scores()
        self.assertEqual(len(top_scores), 3)
        self.assertEqual(top_scores[0]["score"], 40)  # Highest
        self.assertEqual(top_scores[-1]["score"], 20)  # Lowest in top 3

    def test_is_high_score(self):
        """Test high score qualification"""
        # Empty list - any score is high score
        self.assertTrue(self.manager.is_high_score(1))

        # Add some scores
        self.manager.add_score(100, "Player1")
        self.manager.add_score(200, "Player2")
        self.manager.add_score(150, "Player3")

        # Now list is full (max_scores = 3)
        # Score must be > 100 (lowest) to qualify
        self.assertTrue(self.manager.is_high_score(101))
        self.assertFalse(self.manager.is_high_score(99))
        self.assertFalse(
            self.manager.is_high_score(100)
        )  # Equal doesn't qualify

    def test_get_player_best_score(self):
        """Test getting best score for specific player"""
        self.manager.add_score(100, "Alice")
        self.manager.add_score(150, "Bob")
        self.manager.add_score(120, "Alice")  # Alice's better score

        self.assertEqual(self.manager.get_player_best_score("Alice"), 120)
        self.assertEqual(self.manager.get_player_best_score("Bob"), 150)
        self.assertEqual(
            self.manager.get_player_best_score("Charlie"), 0
        )  # Doesn't exist

    def test_clear_scores(self):
        """Test clearing all scores"""
        self.manager.add_score(100, "Player1")
        self.manager.add_score(200, "Player2")

        self.assertEqual(len(self.manager.get_top_scores()), 2)

        self.manager.clear_scores()

        self.assertEqual(len(self.manager.get_top_scores()), 0)
        self.assertEqual(self.manager.get_high_score(), 0)

    def test_persistence(self):
        """Test that scores are saved and loaded from file"""
        # Add scores
        self.manager.add_score(100, "Player1")
        self.manager.add_score(200, "Player2")

        # Create new manager with same file
        new_manager = HighScoreManager(file_path=self.temp_path)

        # Should load existing scores
        self.assertEqual(new_manager.get_high_score(), 200)
        self.assertEqual(len(new_manager.get_top_scores()), 2)

    def test_corrupted_file_handling(self):
        """Test handling of corrupted score file"""
        # Write invalid JSON to file
        with open(self.temp_path, 'w') as f:
            f.write("invalid json content")

        # Should handle gracefully and start fresh
        manager = HighScoreManager(file_path=self.temp_path)
        self.assertEqual(len(manager.get_top_scores()), 0)


if __name__ == '__main__':
    unittest.main()
