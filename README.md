# Quantum Truth Analysis System

[![License](https://img.shields.io/badge/License-AFL--3.0%20with%20restrictions-blue.svg)](LICENSE)

## Overview
The Quantum Truth Analysis System is an advanced framework for evaluating claims through multi-agent debate and axiomatic truth analysis. This system employs specialized agents (FactChecker, Scientist, Logician, Historian, and AxiomRegulator) to analyze evidence, debate perspectives, and determine truth probabilities with visual mapping of reasoning pathways.

## Features
- **Multi-Agent Debate Architecture**: Five specialized agents with unique analytical approaches
- **Axiomatic Framework Integration**: Evaluate claims against scientific, historical, and ethical frameworks
- **Evidence Evaluation Engine**: Analyze source reliability, scientific consensus, and historical patterns
- **Visual Reasoning Mapping**: Generate interactive debate visualization graphs
- **Transformation Pathways**: Identify steps to reconcile conflicting truths
- **Scalable Analysis**: Supports 100-page evidence analysis across 100 debate cycles

## Installation

```bash
# Install from source
git clone https://github.com/yourusername/quantum-truth.git
cd quantum-truth
pip install .

# Or install directly via pip (when available)
pip install quantum-truth
```

## Command Line Interface

After installation, you can run analyses directly from your terminal:

```bash
# Basic analysis
quantum-truth "Is the Earth flat?"

# Custom parameters
quantum-truth "Vaccines contain microchips" --pages 50 --cycles 50 --framework Scientific_Empirical

# Save to custom directory
quantum-truth "The moon landing was faked" -o moon_analysis

# Enable verbose output
quantum-truth "Aliens built the pyramids" -v
```

### Options:
| Parameter | Description | Default |
|-----------|-------------|---------|
| `claim` | Claim to analyze (required) | - |
| `-p, --pages` | Evidence pages to generate | 100 |
| `-c, --cycles` | Debate cycles to run | 100 |
| `-f, --framework` | Analysis framework | Scientific_Empirical |
| `-o, --output` | Output directory | results |
| `-v, --verbose` | Enable verbose output | False |
| `--version` | Show version | - |

## Python API Usage

```python
from quantum_truth import TruthAnalyzer

analyzer = TruthAnalyzer(pages=100, cycles=100)
result = analyzer.analyze("Is the Earth flat?")
print(f"Truth probability: {result:.2%}")
```

## Examples

See the `examples/` directory for usage examples.

## Documentation
Full documentation available at [https://github.com/yourusername/quantum-truth/docs]()

## License
Academic Free License v3.0 with additional restrictions - see [LICENSE](LICENSE) for details.

## Citation
If you use this software in research, please cite:
```
Huckerby, C. (2023). Quantum Truth Analysis System [Computer software]. https://github.com/yourusername/quantum-truth
```

## Contributing
Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.
