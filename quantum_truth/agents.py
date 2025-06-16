class DebateAgent:
    def __init__(self, role, expertise, bias_factor=0.0):
        self.role = role
        self.expertise = expertise
        self.bias_factor = bias_factor
        self.arguments = []
        self.influence = 1.0
        self.confidence = 0.0
        self.confidence_history = []
        self.framework = None

    def formulate_argument(self, claim, evidence, framework):
        self.framework = framework
        try:
            if self.role == "FactChecker":
                verified = [ev for ev in evidence if ev['reliability'] > 0.7]
                self.arguments = [f"Verified {len(verified)} sources" + 
                                 (f": {verified[0]['source']} states '{verified[0]['summary'][:30]}...'" 
                                  if verified else "")]
                self.confidence = min(1.0, len(verified) * 0.3)
                
            elif self.role == "Scientist":
                scientific_evidence = [ev for ev in evidence if ev['type'] == 'scientific']
                if scientific_evidence:
                    consensus = sum(ev['reliability'] for ev in scientific_evidence)/len(scientific_evidence)
                    self.arguments = [f"Scientific consensus ({len(scientific_evidence)} studies, {consensus:.0%} reliability)"]
                    self.confidence = consensus
                else:
                    self.arguments = ["No scientific evidence"]
                    self.confidence = 0.1
                    
            elif self.role == "Logician":
                if evidence:
                    first_support = evidence[0]['supports_claim']
                    contradictions = sum(1 for ev in evidence if ev['supports_claim'] != first_support)
                    consistency = 1.0 - (contradictions / max(1, len(evidence)))
                    self.arguments = [f"Logical consistency: {consistency:.0%}"]
                    self.confidence = consistency
                else:
                    self.arguments = ["Insufficient data"]
                    self.confidence = 0.1
                    
            elif self.role == "Historian":
                historical_evidence = [ev for ev in evidence if ev['type'] == 'historical']
                if historical_evidence:
                    support = sum(1 for ev in historical_evidence if ev['supports_claim']) / len(historical_evidence)
                    self.arguments = [f"Historical precedent: {len(historical_evidence)} cases, {support:.0%} similar"]
                    self.confidence = support
                else:
                    self.arguments = ["No historical precedent"]
                    self.confidence = 0.1
                    
            elif self.role == "AxiomRegulator":
                truth_percent, conflicts = framework.evaluate_statement(claim)
                self.arguments = [f"Axiomatic Truth: {truth_percent:.2f}% in '{framework.name}' framework"]
                self.confidence = truth_percent / 100
                if conflicts:
                    self.arguments.append(f"Conflicts: {', '.join(conflicts)}")
            
            self.confidence = max(0.01, min(1.0, self.confidence + self.bias_factor))
            self.confidence_history.append(self.confidence)
            return self.arguments
        except Exception as e:
            print(f"Error in {self.role} agent: {str(e)}")
            self.arguments = ["Analysis error"]
            self.confidence = 0.1
            return self.arguments
