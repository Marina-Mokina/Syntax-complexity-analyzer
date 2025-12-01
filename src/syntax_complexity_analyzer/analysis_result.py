class AnalysisResult:
    """Represents and displays analysis results"""

    def __init__(self, text: str, metrics: dict, features: dict):
        self.text = text
        self.metrics = metrics
        self.features = features

    def determine_complexity(self, fres: float) -> str:
        """Assess the level of difficulty in understanding the text."""
        very_difficult = 30.0
        difficult = 50.0
        fairly_difficult = 60.0
        standard = 70.0
        fairly_easy = 80.0
        easy = 90.0

        if fres <= very_difficult:
            result = "Level: College Graduate. Very difficult to read"
        elif fres <= difficult:
            result = "Level: College Student. Difficult to read"
        elif fres <= fairly_difficult:
            result = "Level: High School Student. Fairly difficult to read"
        elif fres <= standard:
            result = "Level: 8th-9th Grade Student. Standard text"
        elif fres <= fairly_easy:
            result = "Level: 7th Grade Student. Fairly easy to read"
        elif fres <= easy:
            result = "Level: 6th Grade Student. Easy to read"
        else:
            result = "Level: 5th Grade Student. Very easy to read"

        return result

    def display(self) -> None:
        """Displays analysis results in console"""
        print(f"Text: {self.text}")
        print("Complexity metrics:")
        for metric, value in self.metrics.items():
            print(
                f"  {metric}: {value:.2f}"
                if isinstance(value, float)
                else f"  {metric}: {value}"
            )

        complexity_level = self.determine_complexity(self.metrics["readability_score"])
        print(f"\n{complexity_level}")
