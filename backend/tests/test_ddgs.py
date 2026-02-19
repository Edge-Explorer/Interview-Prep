from ddgs import DDGS
import json

def test_search():
    print("Testing DDGS...")
    try:
        with DDGS() as ddgs:
            results = [r for r in ddgs.text("Python programming", max_results=3)]
            print(f"Found {len(results)} results")
            for r in results:
                print(f"Result: {r}")
    except Exception as e:
        print(f"Search failed: {e}")

if __name__ == "__main__":
    test_search()
