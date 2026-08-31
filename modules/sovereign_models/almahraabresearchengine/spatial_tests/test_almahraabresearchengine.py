#!/usr/bin/env python3
import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'structural_core'))
from almahraab_research_engine import ALMAHRAABResearchEngine

class TestALMAHRAABResearchEngine(unittest.TestCase):
    def setUp(self):
        self.engine = ALMAHRAABResearchEngine()
        
    def test_add_paper(self):
        pid = self.engine.add_paper("Test", ["A"], 2024)
        self.assertIn(pid, self.engine.papers)
        print("  [✓] Add Paper — PASS")
        
    def test_extract_equations(self):
        text = "E = mc^2 and S = k log W"
        eqs = self.engine.extract_equations(text)
        self.assertGreater(len(eqs), 0)
        print(f"  [✓] Equation Extraction — PASS ({len(eqs)} found)")
        
    def test_peer_review(self):
        pid = self.engine.add_paper("Review Test", ["B"], 2024)
        review = self.engine.simulate_peer_review(pid)
        self.assertIn("decision", review)
        self.assertIn(review["decision"], ["ACCEPT", "REJECT"])
        print(f"  [✓] Peer Review — PASS ({review['decision']})")
        
    def test_citation_graph(self):
        p1 = self.engine.add_paper("A", ["X"], 2020)
        p2 = self.engine.add_paper("B", ["Y"], 2021, citations=[p1])
        network = self.engine.get_citation_network(p1)
        self.assertGreaterEqual(len(network), 1)
        print(f"  [✓] Citation Graph — PASS ({len(network)} links)")
        
    def test_impact_factor(self):
        p1 = self.engine.add_paper("Impact", ["Z"], 2020)
        impact = self.engine.compute_impact(p1)
        self.assertGreaterEqual(impact, 0)
        print(f"  [✓] Impact Factor — PASS ({impact})")
        
    def test_cosmic_state(self):
        state = self.engine.to_cosmic_state()
        self.assertEqual(state["mode"], "research_engine")
        self.assertIn("papers", state)
        print("  [✓] UCA State Conversion — PASS")

if __name__ == '__main__':
    unittest.main(verbosity=2)
