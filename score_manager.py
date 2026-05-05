import json
import os


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

    def save_scores(self):
        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(self.scores, file, indent=4)

    def add_score(self, score):
        self.scores.append(score)
        self.scores = sorted(self.scores, reverse=True)[:10]
        self.save_scores()

    def get_scores(self):
        return self.scores

    def get_best_score(self):
        if not self.scores:
            return 0
        return max(self.scores)