#!/usr/bin/env python3
# ============================================================
#  ALMAHRAABResearchEngine — Academic Research Integration
#  Model ID: see manifest.json
#  Purpose: Citation Graphs, Equation Extraction, Peer Review
# ============================================================
import json, re, math
from datetime import datetime
from collections import defaultdict

class ALMAHRAABResearchEngine:
    """
    محرك AL-MAHRAAB البحثي
    يحاكي: استخراج المعادلات، بناء شبكة الاستشهادات، محاكاة المراجعة
    """
    def __init__(self):
        self.papers = {}
        self.citation_graph = defaultdict(list)
        self.equations = []
        self.review_pool = []
        self.impact_scores = {}
        self.timestamp = datetime.now().isoformat()
        
    def add_paper(self, title, authors, year, equations=None, citations=None):
        """إضافة ورقة بحثية للمحرك"""
        paper_id = f"paper_{len(self.papers):04d}"
        self.papers[paper_id] = {
            "id": paper_id,
            "title": title,
            "authors": authors,
            "year": year,
            "equations": equations or [],
            "citations": citations or [],
            "citation_count": 0,
            "review_score": 0.0
        }
        # Build citation graph
        for cited in (citations or []):
            self.citation_graph[cited].append(paper_id)
            self.papers[paper_id]["citation_count"] += 1
        # Extract equations
        for eq in (equations or []):
            self.equations.append({"paper": paper_id, "equation": eq})
        return paper_id
        
    def extract_equations(self, text):
        """استخراج معادلات رياضية من نص (regex simulation)"""
        # Match patterns like: E = mc^2, ψ(x,t), H|ψ⟩ = E|ψ⟩
        patterns = [
            r"[A-Z][\s]*=[\s]*[a-zA-Z0-9\^\s\+\-\*/]+",
            r"\\[a-zA-Z]+\([^)]*\)",
            r"\|[^⟩]+⟩",
            r"G_[\{]?\w+[\}]?[\s]*=[\s]*[\d\.\s\+\-\\\*/^]+"
        ]
        found = []
        for p in patterns:
            found.extend(re.findall(p, text))
        return found
        
    def simulate_peer_review(self, paper_id, reviewers=3):
        """محاكاة مراجعة الأقران"""
        if paper_id not in self.papers:
            return None
        scores = []
        for _ in range(reviewers):
            # Simulate: score ~ N(0.75, 0.1)
            score = min(1.0, max(0.0, 0.75 + 0.1 * (2 * (hash(paper_id + str(_)) % 1000) / 1000 - 1)))
            scores.append(score)
        avg_score = sum(scores) / len(scores)
        self.papers[paper_id]["review_score"] = round(avg_score, 4)
        self.review_pool.append({
            "paper": paper_id,
            "scores": [round(s, 4) for s in scores],
            "average": round(avg_score, 4),
            "decision": "ACCEPT" if avg_score > 0.6 else "REJECT"
        })
        return self.review_pool[-1]
        
    def compute_impact(self, paper_id):
        """حساب معامل التأثير (Impact Factor simulation)"""
        if paper_id not in self.papers:
            return 0.0
        p = self.papers[paper_id]
        age = max(1, 2026 - p["year"])
        citations = len(self.citation_graph.get(paper_id, []))
        # h-index inspired
        impact = citations / math.sqrt(age) + p["review_score"] * 2
        self.impact_scores[paper_id] = round(impact, 4)
        return round(impact, 4)
        
    def get_citation_network(self, paper_id, depth=2):
        """استخراج شبكة الاستشهادات حتى عمق معين"""
        if depth <= 0 or paper_id not in self.papers:
            return []
        direct = self.citation_graph.get(paper_id, [])
        network = [{"paper": d, "depth": 1} for d in direct]
        for d in direct:
            network.extend([{"paper": dd, "depth": 2} for dd in self.citation_graph.get(d, [])])
        return network
        
    def to_cosmic_state(self):
        """تحويل لصيغة UCA Cosmic Fusion"""
        total_papers = len(self.papers)
        avg_review = sum(p["review_score"] for p in self.papers.values()) / max(1, total_papers)
        total_citations = sum(len(v) for v in self.citation_graph.values())
        return {
            "coherence": round(min(1.0, total_papers / 100), 6),
            "stability": round(avg_review, 6),
            "symbolic_mass": round(min(1.0, total_citations / 1000), 6),
            "dimension_switch_score": round(len(self.equations) / 100.0, 6),
            "frequency": "1.42",
            "mode": "research_engine",
            "papers": total_papers,
            "equations": len(self.equations),
            "citations": total_citations
        }

if __name__ == "__main__":
    engine = ALMAHRAABResearchEngine()
    print("[*] ALMAHRAABResearchEngine initialized")
    
    p1 = engine.add_paper(
        "Holographic Principle in Cosmology",
        ["A. Author", "B. Scientist"],
        2024,
        equations=["S = A / 4G", "O_i = P_i(R)"],
        citations=[]
    )
    p2 = engine.add_paper(
        "Quantum Noise in Observer Systems",
        ["C. Researcher"],
        2025,
        equations=["ψ = α|0⟩ + β|1⟩", "H|ψ⟩ = E|ψ⟩"],
        citations=[p1]
    )
    
    eqs = engine.extract_equations("E = mc^2 and G_{μν} = 8πT_{μν}")
    print(f"[+] Extracted Equations: {eqs}")
    
    review = engine.simulate_peer_review(p2)
    print(f"[+] Peer Review: {review['decision']} (score: {review['average']})")
    
    impact = engine.compute_impact(p1)
    print(f"[+] Impact Factor: {impact}")
    
    network = engine.get_citation_network(p1)
    print(f"[+] Citation Network: {len(network)} connections")
    print(f"[+] Cosmic State: {json.dumps(engine.to_cosmic_state(), indent=2)}")
