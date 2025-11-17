import re
from .config import VOWEL_PATTERN, SENTENCE_ENDINGS, RUSSIAN_VOWELS, READABILITY_COEFFICIENTS


class ComplexityMetrics:
    """Calculates syntactic complexity metrics"""

    def calculate_metrics(self, text: str) -> dict:
        """Returns dictionary with complexity metrics"""
        avg_sentence_length = self._avg_sentence_length(text)
        avg_syllables = self._avg_word_length(text)
        readability = self._calculate_readability_score(avg_sentence_length, avg_syllables)

        return {
            "avg_sentence_length": avg_sentence_length,
            "avg_syllables_per_word": avg_syllables,
            "readability_score": readability
        }

    def _avg_sentence_length(self, text: str) -> float:
        """Calculates average sentence length in words"""
        normalized_text = text
        for ending in SENTENCE_ENDINGS:
            normalized_text = normalized_text.replace(ending, '.')
        sentences = [s.strip() for s in normalized_text.split('. ') if s.strip()]

        average_sentence_length = 0.0
        if sentences:
            for sentence in sentences:
                words_in_sentence = len(sentence.split())
                average_sentence_length += words_in_sentence / len(sentences)

        return average_sentence_length

    def _avg_word_length(self, text: str) -> float:
        """Calculates average word length in syllabls"""
        words = [word.lower() for word in text.split() if re.search(VOWEL_PATTERN, word.lower())]

        average_syllables = 0.0
        if words:
            for word in words:
                syllables_in_word = len([letter for letter in word if letter in RUSSIAN_VOWELS])
                average_syllables += syllables_in_word / len(words)

        return average_syllables

    def _calculate_readability_score(self, avg_sentence_length: float, avg_syllables: float) -> float:
        """Calculates readability score using fres formula"""
        return (READABILITY_COEFFICIENTS['base']
                - READABILITY_COEFFICIENTS['sentence_length'] * avg_sentence_length
                - READABILITY_COEFFICIENTS['word_length'] * avg_syllables)
