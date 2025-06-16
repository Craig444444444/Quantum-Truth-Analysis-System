import random
import time
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from .frameworks import AxiomaticFramework
from .agents import DebateAgent

class ChatbotEngine:
    def __init__(self):
        self.debate_history = defaultdict(list)
        self.truth_graph = nx.Graph()
        self.frameworks = {
            "Scientific_Empirical": AxiomaticFramework("Scientific_Empirical", [
                "Earth_Orbits_Sun",
                "Energy_Conservation",
                "Natural_Selection",
                "Gravity"
            ]),
            "Historical_Consensus": AxiomaticFramework("Historical_Consensus", [
                "Pyramids_Built_by_Egyptians",
                "Moon_Landing_Occurred",
                "Industrial_Revolution_Origin"
            ]),
            "Ethical_Framework": AxiomaticFramework("Ethical_Framework", [
                "Truthfulness_Required",
                "Greater_Good_Priority",
                "Individual_Rights"
            ])
        }
        
    def calculate_certainty(self, evidence):
        try:
            if not evidence:
                return random.uniform(0.3, 0.6)
                
            quality = sum(ev['reliability'] for ev in evidence) / len(evidence)
            support_count = sum(1 for ev in evidence if ev['supports_claim'])
            consensus = support_count / len(evidence)
            
            first_support = evidence[0]['supports_claim']
            contradictions = sum(1 for ev in evidence if ev['supports_claim'] != first_support)
            consistency = 1.0 - (contradictions / len(evidence))
            
            certainty = (quality * 0.6) + (consensus * 0.3) + (consistency * 0.1)
            return max(0.01, min(0.99, certainty * random.uniform(0.95, 0.99)))
        except:
            return random.uniform(0.3, 0.6)
    
    def conduct_debate(self, claim, evidence, cycle, framework_name="Scientific_Empirical", verbose=True):
        framework = self.frameworks.get(framework_name, self.frameworks["Scientific_Empirical"])
        
        agents = [
            DebateAgent("FactChecker", "Evidence Verification"),
            DebateAgent("Scientist", "Scientific Consensus", bias_factor=-0.1),
            DebateAgent("Logician", "Logical Analysis"),
            DebateAgent("Historian", "Historical Context"),
            DebateAgent("AxiomRegulator", "Truth Framework", bias_factor=0.0)
        ]
        
        if verbose and cycle == 0:
            print(f"\n=== Debate: '{claim}' ===")
            print(f"Framework: {framework.name}")
            print("Debating agents:")
            for agent in agents:
                print(f"- {agent.role} ({agent.expertise})")
        
        debate_rounds = []
        for agent in agents:
            args = agent.formulate_argument(claim, evidence, framework)
            debate_rounds.append({
                "agent": agent.role,
                "arguments": args,
                "confidence": agent.confidence
            })
            if verbose and cycle == 0:
                print(f"\n{agent.role}: {args[0]}")
                if len(args) > 1:
                    for arg in args[1:]:
                        print(f"  - {arg}")
                print(f"Confidence: {agent.confidence:.0%}")
                time.sleep(0.3)
        
        confidence_scores = [agent.confidence for agent in agents]
        weights = [0.30, 0.25, 0.20, 0.15, 0.10]  # AxiomRegulator added
        weighted_confidence = sum(c * w for c, w in zip(confidence_scores, weights))
        truth_percentage = self.calculate_certainty(evidence)
        
        # Incorporate framework truth percentage
        framework_truth, _ = framework.evaluate_statement(claim)
        combined_truth = (truth_percentage * 0.7) + (framework_truth/100 * 0.3)
        
        truth_percentage = max(0.01, min(0.99, combined_truth))
        
        if verbose and cycle == 0:
            print(f"\n=== Debate Conclusion ===")
            print(f"Claim: '{claim}'")
            print(f"TRUTH PERCENTAGE: {truth_percentage:.4%}")
            print(f"FICTION PERCENTAGE: {1 - truth_percentage:.4%}")
        
        return truth_percentage, debate_rounds, agents, framework
    
    def visualize_debate(self, claim, debate_rounds, truth_percentage, cycle, framework):
        try:
            plt.figure(figsize=(14, 10))
            G = nx.DiGraph()
            positions = {}
            node_colors = []
            claim_label = claim[:25] + "..." if len(claim) > 25 else claim
            
            # Framework node
            G.add_node(framework.name, type='framework')
            positions[framework.name] = (0.5, 0.95)
            node_colors.append('purple')
            
            # Claim node
            G.add_node(claim_label, type='claim')
            positions[claim_label] = (0.5, 0.85)
            node_colors.append('red')
            G.add_edge(framework.name, claim_label)
            
            y_pos = 0.75
            for i, round_data in enumerate(debate_rounds):
                agent = round_data['agent']
                arg = round_data['arguments'][0][:40] + "..." if len(round_data['arguments'][0]) > 40 else round_data['arguments'][0]
                confidence = round_data['confidence']
                
                G.add_node(agent, type='agent')
                positions[agent] = (0.3, y_pos)
                node_colors.append('skyblue')
                G.add_edge(claim_label, agent)
                
                arg_node = f"{agent}_arg"
                G.add_node(arg_node, type='argument')
                positions[arg_node] = (0.7, y_pos)
                node_colors.append('lightgreen' if confidence > 0.5 else 'lightcoral')
                G.add_edge(agent, arg_node)
                
                y_pos -= 0.15
            
            truth_node = f"Truth: {truth_percentage:.2%}"
            G.add_node(truth_node, type='conclusion')
            positions[truth_node] = (0.5, 0.05)
            node_colors.append('gold')
            G.add_edge(claim_label, truth_node)
            
            # Transformation pathway
            pathway = framework.transformation_pathway(claim)
            pathway_node = "Transformation Pathway"
            G.add_node(pathway_node, type='pathway')
            positions[pathway_node] = (0.5, 0.15)
            node_colors.append('orange')
            G.add_edge(truth_node, pathway_node)
            
            nx.draw(G, positions, with_labels=True, node_size=3000, 
                    node_color=node_colors, font_size=9, 
                    arrowsize=20, arrowstyle='->')
            
            plt.title(f"Analysis: '{claim_label}'\nCycle {cycle+1} | Framework: {framework.name}", fontsize=16)
            plt.tight_layout()
            plt.savefig(f"analysis_{claim[:10]}_cycle_{cycle+1}.png")
            plt.close()
            
            # Save transformation pathway
            with open(f"pathway_{claim[:10]}_cycle_{cycle+1}.txt", "w") as f:
                f.write(pathway)
                
            return True
        except Exception as e:
            print(f"Visualization error: {str(e)}")
            return False

class SearchEngine:
    def __init__(self, pages=100):
        self.pages = pages
        self.base_knowledge = {
            "flat_earth": [
                {"source": "NASA", "summary": "Space missions show Earth's spherical shape", "type": "scientific", "reliability": 0.99, "supports_claim": False},
                {"source": "Historical Records", "summary": "Earth known to be spherical since ancient times", "type": "historical", "reliability": 0.95, "supports_claim": False},
                {"source": "Conspiracy Site", "summary": "NASA images are fabrications", "type": "conspiracy", "reliability": 0.05, "supports_claim": True}
            ],
            "vaccine_microchips": [
                {"source": "WHO", "summary": "Vaccines contain no microchips", "type": "scientific", "reliability": 0.97, "supports_claim": False},
                {"source": "Tech Journal", "summary": "Microchips impossible to inject via vaccines", "type": "scientific", "reliability": 0.96, "supports_claim": False},
                {"source": "Social Media", "summary": "Tracking chips admitted by executives", "type": "conspiracy", "reliability": 0.01, "supports_claim": True}
            ],
            "moon_landing": [
                {"source": "NASA Archives", "summary": "Complete documentation of Apollo missions", "type": "historical", "reliability": 0.98, "supports_claim": True},
                {"source": "Physics Review", "summary": "Analysis confirms feasibility of moon landing", "type": "scientific", "reliability": 0.96, "supports_claim": True},
                {"source": "Conspiracy Forum", "summary": "Studio lighting visible in photos", "type": "conspiracy", "reliability": 0.02, "supports_claim": False}
            ],
            "pyramids_aliens": [
                {"source": "Archaeology Journal", "summary": "Evidence shows pyramids built by ancient Egyptians", "type": "historical", "reliability": 0.92, "supports_claim": False},
                {"source": "Alternative History", "summary": "Advanced technology required for pyramid construction", "type": "conspiracy", "reliability": 0.15, "supports_claim": True}
            ]
        }
    
    def generate_evidence(self, base_evidence):
        evidence = []
        for _ in range(self.pages):
            template = random.choice(base_evidence).copy()
            
            # Modify reliability
            template['reliability'] = max(0.01, min(0.99, template['reliability'] * random.uniform(0.9, 1.1)))
            
            # Flip support with probability
            if random.random() < 0.15:
                template['supports_claim'] = not template['supports_claim']
                
            # Modify summary
            if random.random() < 0.4:
                synonyms = {
                    "show": ["demonstrate", "prove", "confirm"],
                    "impossible": ["not feasible", "impractical", "unachievable"],
                    "evidence": ["proof", "data", "findings"],
                    "ancient": ["historical", "archaic", "prehistoric"]
                }
                for word, replacements in synonyms.items():
                    if word in template['summary']:
                        template['summary'] = template['summary'].replace(word, random.choice(replacements))
                        break
                        
            evidence.append(template)
        return evidence
    
    def search_claim(self, claim):
        claim_key = claim.lower().replace("?", "").replace("'", "").replace(",", "").replace(" ", "_")
        
        if claim_key in self.base_knowledge:
            return self.generate_evidence(self.base_knowledge[claim_key])
        
        # For unknown claims
        print(f"\n🔍 Generating {self.pages} synthetic evidence pages...")
        evidence = []
        for i in range(self.pages):
            reliability = random.triangular(0.3, 0.95, 0.8)
            supports = random.random() < 0.3
            evidence.append({
                "source": f"Source {i+1}",
                "summary": f"Evidence point {i+1} about '{claim}'",
                "type": random.choice(["scientific", "historical", "news", "social", "official"]),
                "reliability": reliability,
                "supports_claim": supports
            })
        return evidence
    
    def analyze_evidence(self, evidence):
        analysis = {
            "total": len(evidence),
            "scientific": sum(1 for e in evidence if e['type'] == 'scientific'),
            "reliable": sum(1 for e in evidence if e['reliability'] > 0.8),
            "unreliable": sum(1 for e in evidence if e['reliability'] < 0.3),
            "historical": sum(1 for e in evidence if e['type'] == 'historical'),
            "conspiracy": sum(1 for e in evidence if e['type'] == 'conspiracy'),
            "support": sum(1 for e in evidence if e['supports_claim']),
            "oppose": sum(1 for e in evidence if not e['supports_claim'])
        }
        return analysis
