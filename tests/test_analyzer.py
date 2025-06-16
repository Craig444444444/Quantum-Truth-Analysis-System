import unittest
from quantum_truth.analyzer import TruthAnalyzer
from unittest.mock import patch, MagicMock

class TestTruthAnalyzer(unittest.TestCase):
    @patch('quantum_truth.analyzer.TruthAnalyzer._plot_confidence')
    @patch('quantum_truth.analyzer.TruthAnalyzer._plot_truth_evolution')
    @patch('quantum_truth.analyzer.TruthAnalyzer._save_results')
    def test_analyze(self, mock_save, mock_plot_truth, mock_plot_conf):
        analyzer = TruthAnalyzer(pages=5, cycles=3)
        analyzer.search_engine.search_claim = MagicMock(return_value=[
            {"source": "Test", "summary": "Test evidence", "type": "scientific", 
             "reliability": 0.9, "supports_claim": True}
        ] * 5)
        
        analyzer.chatbot_engine.conduct_debate = MagicMock(return_value=(
            0.85, [], [], MagicMock()
        ))
        
        result = analyzer.analyze("Test claim", verbose=False)
        self.assertIsInstance(result, float)
        self.assertGreaterEqual(result, 0.0)
        self.assertLessEqual(result, 1.0)
        
    def test_determine_verdict(self):
        analyzer = TruthAnalyzer()
        
        self.assertEqual(analyzer._determine_verdict(0.04), "HIGHLY UNLIKELY")
        self.assertEqual(analyzer._determine_verdict(0.20), "UNLIKELY")
        self.assertEqual(analyzer._determine_verdict(0.45), "POSSIBLY MISLEADING")
        self.assertEqual(analyzer._determine_verdict(0.70), "LIKELY TRUE")
        self.assertEqual(analyzer._determine_verdict(0.95), "HIGHLY LIKELY")

if __name__ == '__main__':
    unittest.main()
