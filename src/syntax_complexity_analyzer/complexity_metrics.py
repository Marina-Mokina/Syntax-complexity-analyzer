import re
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


class ComplexityMetrics:
    """Calculates text complexity metrics including readability scores."""

    def __init__(self, text: str):
        """
        Initialize ComplexityMetrics with input text.

        Args:
            text (str): Input text to analyze
        """
        logger.info(f"Starting text analysis (text length: {len(text)} characters)")
        self.config = self.load_config()
        self.text = text

    def load_config(self) -> dict:
        """
        Load configuration from pyproject.toml file.

        Returns:
            dict: Configuration dictionary with text complexity settings
        """
        import tomllib
        from pathlib import Path

        logger.debug("Loading configuration from pyproject.toml")
        pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"

        with open(pyproject_path, "rb") as f:
            data = tomllib.load(f)

        return data["tool"]["text-complexity"]

    def _avg_sentence_length(self) -> float:
        """
        Calculate average sentence length in words.

        Returns:
            float: Average number of words per sentence
        """
        logger.debug("Calculating average sentence length")

        normalized_text = self.text
        for ending in self.config.get("sentence_endings", [".", "!", "?", "…"]):
            normalized_text = normalized_text.replace(ending, ".")

        sentences = [s.strip() for s in normalized_text.split(". ") if s.strip()]

        if not sentences:
            logger.warning("No sentences found in text")
            return 0.0

        total_words = 0
        for sentence in sentences:
            words_in_sentence = len(sentence.split())
            total_words += words_in_sentence

        average_sentence_length = total_words / len(sentences)
        logger.info(f"Average sentence length: {average_sentence_length:.2f} words")
        return average_sentence_length

    def _avg_word_length(self) -> float:
        """
        Calculate average word length in syllables.

        Returns:
            float: Average number of syllables per word
        """
        logger.debug("Calculating average word length in syllables")

        vowel_pattern = self.config.get("vowel_pattern", "[аеёиоуыэюя]")
        russian_vowels = self.config.get("russian_vowels", "аеёиоуыэюя")

        words = [
            word.lower()
            for word in self.text.split()
            if re.search(vowel_pattern, word.lower())
        ]

        if not words:
            logger.warning("No valid words found for syllable calculation")
            return 0.0

        total_syllables = 0
        for word in words:
            syllables_in_word = len(
                [letter for letter in word if letter in russian_vowels]
            )
            total_syllables += syllables_in_word

        average_syllables = total_syllables / len(words)
        logger.info(f"Average syllables per word: {average_syllables:.2f}")
        return average_syllables

    def _calculate_readability_score(self, avg_sentence_length: float, avg_syllables: float) -> float:
        """
        Calculate readability score using Flesch reading ease formula.

        Args:
            avg_sentence_length (float): Average sentence length in words
            avg_syllables (float): Average syllables per word

        Returns:
            float: Flesch Reading Ease Score (FRES)
        """
        logger.debug("Calculating readability score (FRES)")

        readability_config = self.config.get("readability", {})

        fres = (
                readability_config.get("base", 206.835)
                - readability_config.get("sentence_length", 1.3) * avg_sentence_length
                - readability_config.get("word_length", 60.1) * avg_syllables
        )

        logger.info(f"Flesch Reading Ease Score: {fres:.2f}")
        return fres

    def determine_complexity(self, fres: float) -> str:
        """
        Determine text complexity level based on Flesch reading ease score.

        Args:
            fres (float): Flesch Reading Ease Score

        Returns:
            str: Text complexity level description in Russian
        """
        logger.debug(f"Determining complexity level for FRES={fres:.2f}")

        very_difficult = 30.0
        difficult = 50.0
        fairly_difficult = 60.0
        standard = 70.0
        fairly_easy = 80.0
        easy = 90.0

        if fres <= very_difficult:
            result = "Уровень: Выпускник вуза. Очень сложный для чтения"
        elif fres <= difficult:
            result = "Уровень: Студент вуза. Сложный для чтения"
        elif fres <= fairly_difficult:
            result = "Уровень: Старшеклассник. Довольно сложный для чтения"
        elif fres <= standard:
            result = "Уровень: Ученик 8-9 класса. Стандартный текст"
        elif fres <= fairly_easy:
            result = "Уровень: Ученик 7 класса. Довольно легкий для чтения"
        elif fres <= easy:
            result = "Уровень: Ученик 6 класса. Легко читается"
        else:
            result = "Уровень: Ученик 5 класса. Очень легко читается"

        logger.info(f"Complexity level determined: {result}")
        return result
