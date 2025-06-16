import time
from datetime import datetime
import numpy as np
import json
import os
from tqdm import tqdm
from .engines import ChatbotEngine, SearchEngine

class TruthAnalyzer:
    def __init__(self, pages=100, cycles=100):
        self.chatbot_engine = ChatbotEngine()
        self.search_engine = SearchEngine(pages)
        self.claim_history = {}
        self.pages = pages
        self.cycles = cycles
        self.output_dir = "analysis_results"
        os.makedirs(self.output_dir, exist_ok=True)
    
    def analyze(self, claim, framework="Scientific_Empirical", verbose=True):
        start_time = time.time()
        print(f"\n{'='*60}")
        print(f"TRUTH ANALYSIS: {claim}")
        print(f"Pages: {self.pages} | Cycles: {self.cycles}")
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        evidence = self.search_engine.search_claim(claim)
        evidence_analysis = self.search_engine.analyze_evidence(evidence)
        
        if verbose:
            print("\n=== EVIDENCE ANALYSIS ===")
            print(f"Total sources: {evidence_analysis['total']}")
            print(f"Scientific: {evidence_analysis['scientific']}")
            print(f"Reliable sources: {evidence_analysis['reliable']}")
            print(f"Unreliable sources: {evidence_analysis['unreliable']}")
            print(f"Historical: {evidence_analysis['historical']}")
            print(f"Conspiracy: {evidence_analysis['conspiracy']}")
            print(f"Supporting: {evidence_analysis['support']} | Opposing: {evidence_analysis['oppose']}")
        
        truth_percentages = []
        all_agents = []
        framework_obj = None
        
        for cycle in tqdm(range(self.cycles), desc="Debate Cycles"):
            verbose_cycle = verbose and (cycle == 0 or cycle == self.cycles-1)
            tp, debate_rounds, agents, framework_obj = self.chatbot_engine.conduct_debate(
                claim, evidence, cycle, framework, verbose_cycle)
            truth_percentages.append(tp)
            all_agents = agents
            
            # Save visualization for key cycles
            if cycle in [0, self.cycles-1] or (cycle % max(1, self.cycles//10)) == 0:
                self.chatbot_engine.visualize_debate(claim, debate_rounds, tp, cycle, framework_obj)
        
        avg_truth = np.mean(truth_percentages)
        std_truth = np.std(truth_percentages)
        
        # Generate confidence plot
        self._plot_confidence(claim, all_agents)
        # Generate truth percentage plot
        self._plot_truth_evolution(claim, truth_percentages)
        
        # Save results
        result = {
            "claim": claim,
            "truth_percentage_avg": avg_truth,
            "truth_percentage_std": std_truth,
            "evidence_analysis": evidence_analysis,
            "cycles": self.cycles,
            "pages": self.pages,
            "timestamp": datetime.now().isoformat(),
            "execution_time": time.time() - start_time,
            "framework": framework
        }
        
        self._save_results(claim, result)
        
        # Determine verdict
        veracity = self._determine_verdict(avg_truth)
        
        # Get transformation pathway
        transformation_path = framework_obj.transformation_pathway(claim)
        
        print("\n" + "="*60)
        print(f"FINAL VERDICT AFTER {self.cycles} CYCLES: {veracity}")
        print(f"Average Truth Confidence: {avg_truth:.4%} ± {std_truth:.4%}")
        print(f"Evidence Processed: {self.pages} pages")
        print(f"Framework: {framework_obj.name}")
        print(f"Execution Time: {time.time() - start_time:.2f} seconds")
        print("\n=== TRANSFORMATION PATHWAY ===")
        print(transformation_path)
        print("="*60)
        
        return avg_truth

    def _plot_confidence(self, claim, agents):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(12, 6))
        for agent in agents:
            plt.plot(agent.confidence_history, label=agent.role, alpha=0.8)
        plt.title(f"Agent Confidence: '{claim[:30]}'")
        plt.xlabel("Debate Cycle")
        plt.ylabel("Confidence")
        plt.legend()
        plt.grid(True)
        conf_path = f"{self.output_dir}/confidence_{claim[:20]}.png"
        plt.savefig(conf_path)
        plt.close()

    def _plot_truth_evolution(self, claim, truth_percentages):
        import matplotlib.pyplot as plt
        plt.figure(figsize=(12, 6))
        plt.plot(truth_percentages, color='purple')
        plt.title(f"Truth Percentage Evolution: '{claim[:30]}'")
        plt.xlabel("Debate Cycle")
        plt.ylabel("Truth Percentage")
        plt.ylim(0, 1)
        plt.grid(True)
        truth_path = f"{self.output_dir}/truth_evolution_{claim[:20]}.png"
        plt.savefig(truth_path)
        plt.close()

    def _save_results(self, claim, result):
        json_path = f"{self.output_dir}/results_{claim[:20]}.json"
        with open(json_path, "w") as f:
            json.dump(result, f, indent=2)

    def _determine_verdict(self, avg_truth):
        if avg_truth < 0.05:
            return "HIGHLY UNLIKELY"
        elif avg_truth < 0.25:
            return "UNLIKELY"
        elif avg_truth < 0.5:
            return "POSSIBLY MISLEADING"
        elif avg_truth < 0.75:
            return "LIKELY TRUE"
        else:
            return "HIGHLY LIKELY"
