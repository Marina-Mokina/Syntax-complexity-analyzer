import spacy


class DependencyParser:
    """Builds syntactic dependency trees for text analysis"""

    def __init__(self):
        self.nlp = spacy.load("ru_core_news_sm")

    def get_features(self, text: str) -> dict:
        """Extracts syntactic features from text using dependency parsing"""
        doc = self.nlp(text)

        return {
            'tree_depth': self._calculate_tree_depth(doc),
            'subordinate_clauses': self._count_subordinate_clauses(doc),
            'max_dependency_distance': self._calculate_max_dependency_distance(doc),
            'avg_children_per_node': self._calculate_avg_children(doc)
        }

    def _calculate_tree_depth(self, doc) -> int:
        """Calculate maximum syntactic tree depth across sentences"""
        depths = []
        for sent in doc.sents:
            sent_depths = [self._get_token_depth(token) for token in sent]
            depths.append(max(sent_depths) if sent_depths else 0)
        return max(depths) if depths else 0

    def _get_token_depth(self, token) -> int:
        """Calculate depth of a token in dependency tree"""
        depth = 0
        while token.head != token:
            depth += 1
            token = token.head
        return depth

    def _count_subordinate_clauses(self, doc) -> int:
        """Count subordinate clauses based on syntactic relations"""
        subordinate_relations = ['acl', 'advcl', 'ccomp', 'csubj']
        count = 0
        for token in doc:
            if token.dep_ in subordinate_relations:
                count += 1
        return count

    def _calculate_max_dependency_distance(self, doc) -> int:
        """Calculate maximum distance between head and dependent tokens"""
        max_distance = 0
        for token in doc:
            if token.head != token:  # Skip root token
                distance = abs(token.i - token.head.i)
                max_distance = max(max_distance, distance)
        return max_distance

    def _calculate_avg_children(self, doc) -> float:
        """Calculate average number of children per token"""
        if len(doc) == 0:
            return 0.0

        total_children = sum(len(list(token.children)) for token in doc)
        return total_children / len(doc)
