import argparse
import evidence_retrieval as evidence_retrieval

def generate_crawler_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', type=str, help='websearch query to scrape', required=True)
    return parser


def gather_evidence(query):
    results = evidence_retrieval.run_spider(query)
    return results


if __name__ == "__main__":
    parser = generate_crawler_parser()
    args = parser.parse_args()
    query = args.query
    results = gather_evidence(query)
    print(f"\n\n\n\n\n\n\n\n {results}")
    # evidence_retrieval_object = evidence_retrieval(query)