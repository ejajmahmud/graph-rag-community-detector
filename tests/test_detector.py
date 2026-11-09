"""Unit tests for graph-rag-community-detector."""
import unittest
from graph_rag_community_detector.detector import GraphCommunityDetector


class TestGraphCommunityDetector(unittest.TestCase):
    def setUp(self):
        self.detector = GraphCommunityDetector()

    def test_distinct_clusters(self):
        # Cluster 1
        self.detector.add_edge("a1", "a2", 5.0)
        self.detector.add_edge("a2", "a3", 5.0)

        # Cluster 2
        self.detector.add_edge("b1", "b2", 5.0)
        self.detector.add_edge("b2", "b3", 5.0)

        clusters = self.detector.detect_communities()
        self.assertEqual(len(clusters), 2)
