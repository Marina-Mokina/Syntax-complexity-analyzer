import re


class ComplexityMetrics:
    """Calculates complexity metrics"""

    def __init__(self):
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Load configuration from pyproject.toml"""
        import tomllib
        from pathlib import Path

        pyproject_path = Path(__file__).parent.parent / "pyproject.toml"

        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

        return data["tool"]["text-complexity"]

    def calculate_metrics(self, text: str) -> dict:
        """Returns dictionary with complexity metrics"""
        avg_sentence_length = self._avg_sentence_length(text)
        avg_syllables = self._avg_word_length(text)
        readability = self._calculate_readability_score(
            avg_sentence_length, avg_syllables
        )

        return {
            "avg_sentence_length": avg_sentence_length,
            "avg_syllables_per_word": avg_syllables,
            "readability_score": readability,
        }

    def _avg_sentence_length(self, text: str) -> float:
        """Calculates average sentence length in words"""
        normalized_text = text
        for ending in self.config.get("sentence_endings", [".", "!", "?", "…"]):
            normalized_text = normalized_text.replace(ending, ".")

        sentences = [s.strip() for s in normalized_text.split(". ") if s.strip()]
        average_sentence_length = 0.0

        if sentences:
            for sentence in sentences:
                words_in_sentence = len(sentence.split())
                average_sentence_length += words_in_sentence / len(sentences)

        return average_sentence_length

    def _avg_word_length(self, text: str) -> float:
        """Calculates average word length in syllables"""
        vowel_pattern = self.config.get("vowel_pattern", "[аеёиоуыэюя]")
        russian_vowels = self.config.get("russian_vowels", "аеёиоуыэюя")

        words = [
            word.lower()
            for word in text.split()
            if re.search(vowel_pattern, word.lower())
        ]
        average_syllables = 0.0

        if words:
            for word in words:
                syllables_in_word = len(
                    [letter for letter in word if letter in russian_vowels]
                )
                average_syllables += syllables_in_word / len(words)

        return average_syllables

    def _calculate_readability_score(
        self, avg_sentence_length: float, avg_syllables: float
    ) -> float:
        """Calculates readability score using fres formula"""
        readability_config = self.config.get("readability", {})
        return (
            readability_config.get("base", 206.835)
            - readability_config.get("sentence_length", 1.3) * avg_sentence_length
            - readability_config.get("word_length", 60.1) * avg_syllables
        )
