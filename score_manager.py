import json
import os

from const import DEFAULT_PLAYER_NAME


class ScoreManager:
    def __init__(self, file_path="data/scores.json"):
        self.file_path = file_path
        self.scores = []
        self.load_scores()

    def load_scores(self):
        if not os.path.exists("data"):
            os.makedirs("data")

        if not os.path.exists(self.file_path):
            self.scores = []
            self.save_scores()
            return

        with open(self.file_path, "r", encoding="utf-8") as file:
            self.scores = json.load(file)

        self.normalize_old_scores()

    def normalize_old_scores(self):
        normalized_scores = []

        for item in self.scores:
            if isinstance(item, int):
                normalized_scores.append({
                    "name": DEFAULT_PLAYER_NAME,
                    "score": item
                })
            else:
                normalized_scores.append(item)

        self.scores = normalized_scores
        self.save_scores()

    def save_scores(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.scores, file, indent=4)

    def add_score(self, score, player_name):
        name = player_name.strip().upper()

        if name == "":
            name = DEFAULT_PLAYER_NAME

        self.scores.append({
            "name": name,
            "score": score
        })

        self.scores = sorted(
            self.scores,
            key=lambda item: item["score"],
            reverse=True
        )[:10]

        self.save_scores()

    def get_scores(self):
        return self.scores

    def get_best_score(self):
        if not self.scores:
            return 0

        return max(item["score"] for item in self.scores)