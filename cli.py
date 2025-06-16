#!/usr/bin/env python3
"""
Quantum Truth Analysis System - Command Line Interface
Copyright (c) 2023 Craig Huckerby. All Rights Reserved.
"""

import argparse
import sys
from quantum_truth.analyzer import TruthAnalyzer

def main():
    parser = argparse.ArgumentParser(
        description="Quantum Truth Analysis System CLI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("claim", type=str, help="Claim to analyze")
    parser.add_argument("-p", "--pages", type=int, default=100,
                        help="Number of evidence pages to generate")
    parser.add_argument("-c", "--cycles", type=int, default=100,
                        help="Number of debate cycles")
    parser.add_argument("-f", "--framework", type=str, default="Scientific_Empirical",
                        choices=["Scientific_Empirical", "Historical_Consensus", "Ethical_Framework"],
                        help="Analysis framework to use")
    parser.add_argument("-o", "--output", type=str, default="results",
                        help="Output directory for results")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Enable verbose output")
    parser.add_argument("--version", action="version", version="Quantum Truth Analyzer 1.0.0")

    args = parser.parse_args()

    print(f"🔍 Starting Quantum Truth Analysis for: '{args.claim}'")
    print(f"   Pages: {args.pages}, Cycles: {args.cycles}, Framework: {args.framework}")

    analyzer = TruthAnalyzer(pages=args.pages, cycles=args.cycles)
    analyzer.output_dir = args.output
    try:
        result = analyzer.analyze(args.claim, framework=args.framework, verbose=args.verbose)
    except Exception as e:
        print(f"❌ Error during analysis: {e}", file=sys.stderr)
        sys.exit(1)

    print("\n✅ Analysis complete!")
    print(f"   Results saved to: {args.output}/")
    print(f"   Final Truth Probability: {result:.4%}")

if __name__ == "__main__":
    main()
