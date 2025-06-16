"""Batch analysis example"""
from quantum_truth import TruthAnalyzer

claims = [
    "The Earth is flat",
    "Vaccines cause autism",
    "The moon landing was faked",
    "Global warming is a hoax"
]

analyzer = TruthAnalyzer(pages=30, cycles=30)

for claim in claims:
    print(f"\n{'='*60}")
    print(f"ANALYZING: {claim}")
    result = analyzer.analyze(claim, verbose=False)
    print(f"RESULT: {result:.2%} truth probability")
    print("="*60)
