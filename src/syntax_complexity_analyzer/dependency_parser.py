from natasha import Doc, Segmenter, NewsEmbedding, NewsSyntaxParser, MorphVocab
from collections import Counter
import io
import sys
import logging

logger = logging.getLogger(__name__)


class DependencyParser:
    """
    Builds syntactic dependency trees for Russian text using Natasha library.

    Attributes:
        segmenter: Natasha segmenter for sentence segmentation
        emb: News embeddings for syntax parsing
        syntax_parser: Natasha syntax parser for dependency trees
        morph_vocab: Morphological vocabulary
        text: Input text to analyze
        doc: Parsed Natasha document object
    """

    def __init__(self, text: str):
        """
        Initialize Natasha components and parse input text.

        Args:
            text: Russian text to analyze for syntactic dependencies
        """
        logger.info(f"Initializing DependencyParser with text: '{text[:50]}...'")
        self.segmenter = Segmenter()
        self.emb = NewsEmbedding()
        self.syntax_parser = NewsSyntaxParser(self.emb)
        self.morph_vocab = MorphVocab()
        self.text = text
        self.doc = self.parse_text()

    def parse_text(self) -> Doc:
        """
        Parse text using Natasha pipeline.

        Returns:
            Doc: Natasha document object with segmented sentences and parsed syntax
        """
        doc = Doc(self.text)
        doc.segment(self.segmenter)
        doc.parse_syntax(self.syntax_parser)
        return doc

    def calculate_tree_depth(self) -> int:
        """
        Calculate maximum depth of dependency tree from Natasha tokens.

        Returns:
            int: Maximum depth of dependency tree
        """
        max_depth = 0

        token_dict = {token.id: token for token in self.doc.tokens}

        for token in self.doc.tokens:
            depth = 0
            current = token

            while current.head_id is not None and current.head_id in token_dict:
                depth += 1
                current = token_dict[current.head_id]

                if depth > 100:
                    break

            max_depth = max(max_depth, depth)

        return max_depth

    def count_subordinate_clauses(self) -> int:
        """
        Count subordinate clauses based on syntactic relations.

        Returns:
            int: Number of subordinate clauses detected
        """
        return sum(1 for sent in self.doc.sents
                   for token in sent.tokens
                   if token.rel in {'mark', 'nsubj'})

    def calculate_max_dependency_distance(self) -> int:
        """
        Calculate maximum distance between a token and its head in linear order.

        Returns:
            int: Maximum dependency distance in the document
        """
        distances = (
            abs(i - (int(token.head_id.split('_')[-1]) - 1))
            for sent in self.doc.sents
            for i, token in enumerate(sent.tokens)
            if token.head_id and '_' in token.head_id
        )

        return max(distances, default=0)

    def calculate_avg_children(self) -> float:
        """
        Calculate average number of children per token in dependency trees.

        Returns:
            float: Average number of children per token
        """
        head_counts = Counter(
            token.head_id
            for sent in self.doc.sents
            for token in sent.tokens
            if token.head_id
        )

        total_children = sum(
            head_counts.get(f"{i + 1}_{j}", 0)
            for i, sent in enumerate(self.doc.sents)
            for j in range(len(sent.tokens))
        )

        total_tokens = sum(len(sent.tokens) for sent in self.doc.sents)

        return total_children / total_tokens if total_tokens else 0.0

    def get_tree_visualization(self) -> str:
        """
        Generate ASCII tree visualization of dependency trees.

        Returns:
            str: String containing ASCII tree visualizations for all sentences
        """
        result = []
        for i, sent in enumerate(self.doc.sents[:2], 1):
            result.append(f"Sentence {i}: '{sent.text}'")

            try:
                old_stdout = sys.stdout
                sys.stdout = io.StringIO()

                sent.syntax.print()
                tree_output = sys.stdout.getvalue()

                sys.stdout = old_stdout
                result.append(tree_output)

            except Exception as e:
                result.append(f"Failed to display tree: {str(e)}")
                for token in sent.tokens:
                    result.append(f"  {token.text} ({token.rel}) → {token.head_id}")

        return '\n'.join(result)
