"""
High score management system
"""

import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from .logger import logger


class HighScoreManager:
    """High score manager with persistent storage"""

    def __init__(
        self, file_path: str = "high_scores.json", max_scores: int = 10
    ):
        self.file_path = Path(file_path)
        self.max_scores = max_scores
        self.scores: List[Dict] = self._load_scores()

    def _load_scores(self) -> List[Dict]:
        """Load scores from file"""
        if not self.file_path.exists():
            logger.info(
                "High score file not found, starting with empty scores"
            )
            return []

        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                scores = json.load(f)
                logger.info(f"Loaded {len(scores)} high scores")
                return scores
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load high scores: {e}")
            return []

    def _save_scores(self) -> bool:
        """Save scores to file"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.scores, f, indent=2, ensure_ascii=False)
            logger.info(f"Saved {len(self.scores)} high scores")
            return True
        except IOError as e:
            logger.error(f"Failed to save high scores: {e}")
            return False

    def add_score(self, score: int, player_name: str = "Anonymous") -> bool:
        """Add new score and return True if it's a new high score"""
        is_new_high_score = self.is_high_score(score)

        new_score_entry = {
            "score": score,
            "player": player_name,
            "date": datetime.now().isoformat(),
            "timestamp": datetime.now().timestamp(),
        }

        self.scores.append(new_score_entry)

        # Sort by score (descending) and keep only top scores
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        self.scores = self.scores[: self.max_scores]

        # Save to file
        self._save_scores()

        logger.info(f"Added score: {score} by {player_name}")

        return is_new_high_score

    def is_high_score(self, score: int) -> bool:
        """Check if score qualifies as a high score"""
        if len(self.scores) < self.max_scores:
            return True

        return score > self.get_lowest_high_score()

    def get_high_score(self) -> int:
        """Get the highest score"""
        return self.scores[0]["score"] if self.scores else 0

    def get_lowest_high_score(self) -> int:
        """Get the lowest high score"""
        return self.scores[-1]["score"] if self.scores else 0

    def get_top_scores(self, limit: Optional[int] = None) -> List[Dict]:
        """Get top scores with optional limit"""
        if limit is None:
            limit = self.max_scores

        return self.scores[:limit]

    def get_player_best_score(self, player_name: str) -> int:
        """Get best score for a specific player"""
        player_scores = [
            s["score"] for s in self.scores if s["player"] == player_name
        ]
        return max(player_scores) if player_scores else 0

    def clear_scores(self) -> None:
        """Clear all scores"""
        self.scores = []
        self._save_scores()
        logger.info("Cleared all high scores")
