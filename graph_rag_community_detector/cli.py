"""CLI for graph-rag-community-detector."""
import sys
import argparse
from .detector import GraphCommunityDetector


def main():
    parser = argparse.ArgumentParser(description="Graph RAG Community Detector CLI")
    parser.add_argument("--demo", action="store_true", help="Run community detection demo")
    args = parser.parse_args()

    if args.demo:
        detector = GraphCommunityDetector()
        # Community 1: Auth cluster
        detector.add_edge("OAuth", "JWT", 2.0)
        detector.add_edge("JWT", "AuthService", 3.0)
        detector.add_edge("OAuth", "AuthService", 2.0)

        # Community 2: Database cluster
        detector.add_edge("PostgreSQL", "Prisma", 3.0)
        detector.add_edge("Prisma", "DatabasePool", 2.0)
        detector.add_edge("PostgreSQL", "DatabasePool", 2.0)

        # Weak bridge
        detector.add_edge("AuthService", "PostgreSQL", 0.5)

        clusters = detector.detect_communities()
        print(f"Detected {len(clusters)} Distinct Graph Communities:")
        for c in clusters:
            print(f"  Community #{c.community_id} (Hub: {c.central_hub}): {c.members}")
    else:
        parser.print_help()
    sys.exit(0)


if __name__ == "__main__":
    main()
