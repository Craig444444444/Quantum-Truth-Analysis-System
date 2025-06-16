import unittest
from unittest.mock import patch
from io import StringIO
import sys

class TestCLI(unittest.TestCase):

    @patch('sys.argv', ['quantum-truth', 'Test claim'])
    @patch('quantum_truth.analyzer.TruthAnalyzer.analyze')
    def test_basic_cli(self, mock_analyze):
        mock_analyze.return_value = 0.85
        from cli import main
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()
            self.assertIn("Test claim", output)
            self.assertIn("Final Truth Probability", output)
    
    @patch('sys.argv', ['quantum-truth', 'Test claim', '--pages', '50', '--cycles', '30'])
    @patch('quantum_truth.analyzer.TruthAnalyzer.analyze')
    def test_custom_parameters(self, mock_analyze):
        from cli import main
        main()
        mock_analyze.assert_called_with("Test claim", framework="Scientific_Empirical", verbose=False)
    
    @patch('sys.argv', ['quantum-truth', 'Test claim', '-o', 'custom_output'])
    def test_output_directory(self):
        from cli import main
        with patch('quantum_truth.analyzer.TruthAnalyzer') as mock_analyzer:
            instance = mock_analyzer.return_value
            instance.analyze.return_value = 0.75
            main()
            self.assertEqual(instance.output_dir, "custom_output")

if __name__ == '__main__':
    unittest.main()
