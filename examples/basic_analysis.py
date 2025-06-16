"""Basic analysis example"""
from quantum_truth import TruthAnalyzer

analyzer = TruthAnalyzer(pages=50, cycles=50)
result = analyzer.analyze("Climate change is primarily caused by human activity")
print(f"Truth probability: {result:.2%}")
