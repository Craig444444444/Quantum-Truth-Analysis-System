import unittest
from quantum_truth.frameworks import AxiomaticFramework

class TestAxiomaticFramework(unittest.TestCase):
    def setUp(self):
        self.framework = AxiomaticFramework("Science", ["Gravity", "Evolution"])
    
    def test_evaluate_statement(self):
        # Compatible statement
        truth, conflicts = self.framework.evaluate_statement("Gravity")
        self.assertEqual(truth, 100.0)
        self.assertEqual(len(conflicts), 0)
        
        # Incompatible statement
        truth, conflicts = self.framework.evaluate_statement("FlatEarth")
        self.assertLess(truth, 100.0)
        self.assertGreater(len(conflicts), 0)
    
    def test_transformation_pathway(self):
        # Compatible statement
        pathway = self.framework.transformation_pathway("Gravity")
        self.assertIn("No transformation needed", pathway)
        
        # Incompatible statement
        self.framework.evaluate_statement("FlatEarth")
        pathway = self.framework.transformation_pathway("FlatEarth")
        self.assertIn("Resolve conflicts", pathway)
        self.assertIn("Constructual Diplomacy", pathway)
        self.assertIn("Axiomogenesis", pathway)

if __name__ == '__main__':
    unittest.main()
