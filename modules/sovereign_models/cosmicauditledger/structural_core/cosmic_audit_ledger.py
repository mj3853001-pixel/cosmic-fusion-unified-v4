#!/usr/bin/env python3
# ============================================================
#  CosmicAuditLedger — Blockchain-Style SHA-256 Hash Chain
#  Model ID: see manifest.json
#  Purpose: Tamper-Evident Cosmic State History
# ============================================================
import hashlib, json
from datetime import datetime

class CosmicAuditLedger:
    """
    سجل التدقيق الكوني
    كل حالة كونية = block
    كل block يحتوي: hash, prev_hash, timestamp, state, audit
    """
    def __init__(self):
        self.timestamp = datetime.now().isoformat()
        self.chain = []
        self.pending_states = []
        self.genesis_hash = "0" * 64
        self._create_genesis_block()
        
    def _create_genesis_block(self):
        """إنشاء البلوك الأول (Genesis)"""
        genesis = {
            "index": 0,
            "timestamp": self.timestamp,
            "state": {"coherence": 0.5, "stability": 0.5, "mode": "genesis"},
            "audit": {"status": "GENESIS", "residual": 0.0},
            "prev_hash": self.genesis_hash,
            "nonce": 0
        }
        genesis["hash"] = self._compute_hash(genesis)
        self.chain.append(genesis)
        
    def _compute_hash(self, block):
        """حساب SHA-256 للبلوك"""
        block_string = json.dumps({
            "index": block["index"],
            "timestamp": block["timestamp"],
            "state": block["state"],
            "audit": block["audit"],
            "prev_hash": block["prev_hash"],
            "nonce": block["nonce"]
        }, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(block_string.encode()).hexdigest()
        
    def append_state(self, state, audit):
        """إضافة حالة كونية جديدة للسلسلة"""
        prev_block = self.chain[-1]
        block = {
            "index": len(self.chain),
            "timestamp": datetime.now().isoformat(),
            "state": state,
            "audit": audit,
            "prev_hash": prev_block["hash"],
            "nonce": 0
        }
        block["hash"] = self._compute_hash(block)
        self.chain.append(block)
        return block["hash"]
        
    def verify_chain(self):
        """التحقق من سلامة السلسلة بالكامل"""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current["hash"] != self._compute_hash(current):
                return {"valid": False, "error": f"Hash mismatch at block {i}"}
            if current["prev_hash"] != previous["hash"]:
                return {"valid": False, "error": f"Chain broken at block {i}"}
        return {"valid": True, "blocks": len(self.chain), "integrity": "100%"}
        
    def detect_tampering(self, block_index, fake_state):
        """اكتشاف محاولة العبث"""
        if block_index >= len(self.chain):
            return {"tampered": False, "reason": "Index out of range"}
        original = self.chain[block_index]
        original_hash = original["hash"]
        original["state"] = fake_state
        new_hash = self._compute_hash(original)
        original["state"] = original["state"]
        return {
            "tampered": new_hash != original_hash,
            "original_hash": original_hash,
            "new_hash": new_hash,
            "block_index": block_index
        }
        
    def merkle_root(self):
        """حساب جذر شجرة Merkle"""
        hashes = [b["hash"] for b in self.chain]
        while len(hashes) > 1:
            if len(hashes) % 2 == 1:
                hashes.append(hashes[-1])
            new_level = []
            for i in range(0, len(hashes), 2):
                combined = hashlib.sha256((hashes[i] + hashes[i+1]).encode()).hexdigest()
                new_level.append(combined)
            hashes = new_level
        return hashes[0] if hashes else self.genesis_hash
        
    def to_cosmic_state(self):
        """تحويل لصيغة UCA Cosmic Fusion"""
        verification = self.verify_chain()
        return {
            "coherence": round(1.0 if verification["valid"] else 0.0, 6),
            "stability": round(0.9 + 0.1 * (len(self.chain) / 1000), 6),
            "symbolic_mass": round(0.95, 6),
            "dimension_switch_score": round(len(self.chain) / 1000.0, 6),
            "frequency": "1.42",
            "mode": "audit_ledger",
            "blocks": len(self.chain),
            "merkle_root": self.merkle_root(),
            "integrity": verification["integrity"]
        }

if __name__ == "__main__":
    ledger = CosmicAuditLedger()
    print("[*] CosmicAuditLedger initialized")
    print(f"[*] Genesis Hash: {ledger.chain[0]['hash'][:16]}...")
    for i in range(3):
        h = ledger.append_state({"coherence": 0.5 + i*0.05}, {"status": "PASS"})
        print(f"[+] Block {i+1}: {h[:16]}...")
    print(f"[+] Valid: {ledger.verify_chain()['valid']}")
    print(f"[+] Merkle Root: {ledger.merkle_root()[:16]}...")
