import unittest
from quantum_truth.agents import DebateAgent
from quantum_truth.frameworks import AxiomaticFramework

class TestDebateAgent(unittest.TestCase):
    def setUp(self):
        self.framework = AxiomaticFramework("Science", ["Gravity", "Evolution"])
        self.evidence = [{
            "source": "Test", 
            "summary": "Test evidence", 
            "type": "scientific", 
            "reliability": 0.9, 
            "supports_claim": True
        }]
    
    def test_fact_checker(self):
        agent = DebateAgent("FactChecker", "Evidence Verification")
        args = agent.formulate_argument("Test claim", self.evidence, self.framework)
        self.assertIsInstance(args, list)
        self.assertGreater(len(args), 0)
        self.assertGreater(agent.confidence, 0.0)
    
    def test_scientist(self):
        agent = DebateAgent("Scientist", "Scientific Consensus")
        args = agent.formulate_argument("Test claim", self.evidence, self.framework)
        self.assertIn("Scientific consensus", args[0])
    
    def test_axiom_regulator(self):
        agent = DebateAgent("AxiomRegulator", "Truth Framework")
        args = agent.formulate_argument("Gravity", self.evidence, self.framework)
        self.assertIn("Axiomatic Truth", args[0])
        self.assertIn("100.00%", args[0])
        
        args = agent.formulate_argument("FlatEarth", self.evidence, self.framework)
        self.assertIn("Conflicts", args[1])

if __name__ == '__main__':
    unittest.main()
