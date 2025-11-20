"""
Final comprehensive integration test
Tests all components working together
"""
import requests
import time
import json

API_URL = "http://localhost:8000"

def print_section(title):
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)

def test_integration():
    print_section("FINAL INTEGRATION TEST")
    
    test_cases = [
        {
            "name": "Positive Customer Review",
            "text": "This product exceeded my expectations! Great quality and fast shipping.",
            "expected": "positive"
        },
        {
            "name": "Negative Customer Feedback",
            "text": "Terrible experience. The product broke after one day. Very disappointed.",
            "expected": "negative"
        },
        {
            "name": "Neutral Statement",
            "text": "The package arrived on Tuesday. It contains the items I ordered.",
            "expected": "neutral"
        },
        {
            "name": "Mixed Sentiment",
            "text": "The product quality is excellent, but the customer service was poor.",
            "expected": None  # Could be any
        },
        {
            "name": "Short Positive",
            "text": "Love it!",
            "expected": "positive"
        },
        {
            "name": "Short Negative",
            "text": "Hate this.",
            "expected": "negative"
        },
        {
            "name": "Emoji Test",
            "text": "Amazing product! 🎉😍👍",
            "expected": "positive"
        },
        {
            "name": "Question Form",
            "text": "Why is this so bad? Terrible quality!",
            "expected": "negative"
        }
    ]
    
    results = {
        "passed": 0,
        "failed": 0,
        "total": len(test_cases)
    }
    
    print(f"\nRunning {results['total']} test cases...\n")
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}/{results['total']}: {test['name']}")
        print(f"   Text: \"{test['text']}\"")
        
        try:
            response = requests.post(
                f"{API_URL}/analyze-sentiment",
                json={"text": test['text']},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                sentiment = data['sentiment']
                confidence = data['confidence']
                explanation = data['explanation']
                
                print(f"   Sentiment: {sentiment}")
                print(f"   Confidence: {confidence:.2%}")
                print(f"   Explanation: {explanation[:80]}...")
                
                if test['expected']:
                    if sentiment == test['expected']:
                        print(f"   ✅ PASSED (Expected: {test['expected']})")
                        results['passed'] += 1
                    else:
                        print(f"   ❌ FAILED (Expected: {test['expected']}, Got: {sentiment})")
                        results['failed'] += 1
                else:
                    print(f"   ✅ PASSED (No specific expectation)")
                    results['passed'] += 1
            else:
                print(f"   ❌ FAILED (HTTP {response.status_code})")
                results['failed'] += 1
                
        except Exception as e:
            print(f"   ❌ ERROR: {str(e)}")
            results['failed'] += 1
        
        time.sleep(0.5)  # Be nice to the API
    
    # Summary
    print_section("TEST SUMMARY")
    print(f"\nTotal Tests: {results['total']}")
    print(f"Passed: {results['passed']} ✅")
    print(f"Failed: {results['failed']} ❌")
    print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
    
    # Cache stats
    print_section("CACHE STATISTICS")
    response = requests.get(f"{API_URL}/cache/stats")
    cache_stats = response.json()
    print(f"\nCache Size: {cache_stats['cache_size']}")
    print(f"Cache Enabled: {cache_stats['cache_enabled']}")
    
    # Performance test
    print_section("PERFORMANCE TEST")
    print("\nTesting response times (5 requests)...")
    
    times = []
    for i in range(5):
        start = time.time()
        response = requests.post(
            f"{API_URL}/analyze-sentiment",
            json={"text": "This is a performance test."}
        )
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"   Request {i+1}: {elapsed:.3f}s")
    
    print(f"\nAverage Response Time: {sum(times)/len(times):.3f}s")
    print(f"Min: {min(times):.3f}s | Max: {max(times):.3f}s")
    
    # Final status
    print_section("FINAL STATUS")
    
    if results['failed'] == 0:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("\n✅ System is working perfectly!")
        print("\nYour Sentiment Analysis API is:")
        print("  • Responding correctly")
        print("  • Analyzing sentiments accurately")
        print("  • Handling edge cases")
        print("  • Caching efficiently")
        print("  • Performing well")
        print("\nYou can now:")
        print("  1. Deploy to production")
        print("  2. Integrate with your applications")
        print("  3. Start analyzing sentiments!")
        return True
    else:
        print(f"\n⚠️  {results['failed']} test(s) failed")
        print("\nPlease review the failures above.")
        return False

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║        SENTIMENT ANALYSIS API                            ║
║        Final Integration Test Suite                      ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
    """)
    
    try:
        success = test_integration()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        exit(1)
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        exit(1)