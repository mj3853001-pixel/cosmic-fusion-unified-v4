#!/usr/bin/env python3
import unittest, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'structural_core'))
from cosmic_audit_ledger import CosmicAuditLedger

class TestCosmicAuditLedger(unittest.TestCase):
    def setUp(self):
        self.ledger = CosmicAuditLedger()
        
    def test_genesis_block(self):
        self.assertEqual(len(self.ledger.chain), 1)
        self.assertEqual(self.ledger.chain[0]["index"], 0)
        print("  [✓] Genesis Block — PASS")
        
    def test_append_and_verify(self):
        for i in range(3):
            self.ledger.append_state({"coherence": 0.5}, {"status": "PASS"})
        result = self.ledger.verify_chain()
        self.assertTrue(result["valid"])
        self.assertEqual(result["blocks"], 4)
        print(f"  [✓] Chain Append & Verify — PASS ({result['blocks']} blocks)")
        
    def test_hash_linkage(self):
        self.ledger.append_state({"test": True}, {"status": "PASS"})
        b1, b2 = self.ledger.chain[-2], self.ledger.chain[-1]
        self.assertEqual(b2["prev_hash"], b1["hash"])
        print("  [✓] Hash Linkage — PASS")
        
    def test_tamper_detection(self):
        self.ledger.append_state({"val": 100}, {"status": "PASS"})
        tamper = self.ledger.detect_tampering(1, {"val": 999})
        self.assertTrue(tamper["tampered"])
        print("  [✓] Tamper Detection — PASS")
        
    def test_merkle_root(self):
        root = self.ledger.merkle_root()
        self.assertEqual(len(root), 64)
        print(f"  [✓] Merkle Root — PASS ({root[:8]}...)")
        
    def test_cosmic_state(self):
        state = self.ledger.to_cosmic_state()
        self.assertEqual(state["mode"], "audit_ledger")
        self.assertIn("merkle_root", state)
        print("  [✓] UCA State Conversion — PASS")

if __name__ == '__main__':
    unittest.main(verbosity=2)
