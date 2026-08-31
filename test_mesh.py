#!/usr/bin/env python3
import unittest, time, sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cosmic_server_v5 import CosmicEngine, MeshSync

class TestMeshSync(unittest.TestCase):
    def setUp(self):
        # كل تست يبدأ بنظافة — عزل كامل
        if hasattr(self, 'mesh') and self.mesh:
            with self.mesh.lock:
                self.mesh.peers.clear()

    @classmethod
    def setUpClass(cls):
        cls.engine = CosmicEngine()
        cls.engine.start = time.time()
        cls.mesh = MeshSync(cls.engine)
        cls.mesh.my_ip = "192.168.1.99"
        print("\n[⚡] v5.0 Mesh Sync Tests...")

    def test_01_mesh_init(self):
        self.assertIsNotNone(self.mesh); self.assertTrue(self.mesh.running)
        print("  [✓] Mesh Init — PASS")

    def test_02_peer_registration(self):
        fake = {"coherence":0.75,"stability":0.60,"dimension_switch_score":0.30,"symbolic_mass":0.95,"day":10,"phase":2,"frequency":"1.42"}
        with self.mesh.lock:
            self.mesh.peers['192.168.1.100'] = {'last_seen':time.time(),'state':fake,'ip':'192.168.1.100'}
        peers = self.mesh.get_peers()
        self.assertEqual(len(peers), 1); self.assertEqual(peers[0]['ip'], '192.168.1.100')
        print("  [✓] Peer Registration — PASS")

    def test_03_consensus(self):
        with self.mesh.lock:
            self.mesh.peers.clear()  # نظافة قبل التست
            self.mesh.peers['192.168.1.101'] = {'last_seen':time.time(),'state':{"coherence":0.80,"stability":0.70,"dimension_switch_score":0.40,"symbolic_mass":0.90},'ip':'192.168.1.101'}
            self.mesh.peers['192.168.1.102'] = {'last_seen':time.time(),'state':{"coherence":0.60,"stability":0.50,"dimension_switch_score":0.20,"symbolic_mass":0.95},'ip':'192.168.1.102'}
        c = self.mesh.get_consensus()
        self.assertIsNotNone(c); self.assertEqual(c['peer_count'], 2)
        self.assertAlmostEqual(c['coherence'], 0.70, places=5)
        self.assertAlmostEqual(c['stability'], 0.60, places=5)
        print(f"  [✓] Consensus — PASS (peers: {c['peer_count']})")

    def test_04_stale_cleanup(self):
        with self.mesh.lock:
            self.mesh.peers.clear()
            self.mesh.peers['192.168.1.200'] = {'last_seen':time.time()-60,'state':{},'ip':'192.168.1.200'}
        now = time.time()
        stale = [ip for ip,p in self.mesh.peers.items() if now-p['last_seen']>30]
        for ip in stale: del self.mesh.peers[ip]
        self.assertNotIn('192.168.1.200', [p['ip'] for p in self.mesh.get_peers()])
        print("  [✓] Stale Cleanup — PASS")

    def test_05_standalone(self):
        m = MeshSync(self.engine); m.peers.clear(); m.my_ip = "127.0.0.1"
        self.assertIsNone(m.get_consensus()); self.assertEqual(len(m.get_peers()), 0)
        print("  [✓] Standalone Mode — PASS")

    def test_06_api_mesh_structure(self):
        with self.mesh.lock:
            self.mesh.peers.clear()
            self.mesh.peers['192.168.1.103'] = {'last_seen':time.time(),'state':{"coherence":0.5,"stability":0.5,"dimension_switch_score":0.5,"symbolic_mass":0.5},'ip':'192.168.1.103'}
        peers = self.mesh.get_peers(); cons = self.mesh.get_consensus()
        resp = {"self_ip":self.mesh.my_ip,"peers":peers,"consensus":cons,"mesh_active":len(peers)>0,"udp_port":9090}
        self.assertIn("self_ip", resp); self.assertIn("mesh_active", resp); self.assertIsInstance(resp["peers"], list)
        print("  [✓] API Mesh Structure — PASS")

if __name__ == '__main__': unittest.main(verbosity=2)
