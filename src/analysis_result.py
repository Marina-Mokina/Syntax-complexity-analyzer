class AnalysisResult:
    """Represents and displays analysis results"""

    def __init__(self, text: str, metrics: dict, features: dict):
        self.text = text
        self.metrics = metrics
        self.features = features

    def determine_complexity(self, fres: float) -> str:
        """Assess the level of difficulty in understanding the text."""
        if fres <= 30.0:
            return 'Level: College Graduate. Very difficult to read'
        elif 30.0 < fres <= 50.0:
            return 'Level: College Student. Difficult to read'
        elif 50.0 < fres <= 60.0:
            return 'Level: High School Student. Fairly difficult to read'
        elif 60.0 < fres <= 70.0:
            return 'Level: 8th-9th Grade Student. Standard text'
        elif 70.0 < fres <= 80.0:
            return 'Level: 7th Grade Student. Fairly easy to read'
        elif 80.0 < fres <= 90.0:
            return 'Level: 6th Grade Student. Easy to read'
        else:
            return 'Level: 5th Grade Student. Very easy to read'

    def display(self):
        """Displays analysis results in console"""
        print(f'Text: {self.text}')
        print('Complexity metrics:')
        for metric, value in self.metrics.items():
            print(f'  {metric}: {value:.2f}' if isinstance(value, float) else f'  {metric}: {value}')

        complexity_level = self.determine_complexity(self.metrics['readability_score'])
        print(f"\n{complexity_level}")
