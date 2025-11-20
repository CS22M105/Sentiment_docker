"""
Interactive Python script to test the API
"""
import requests
import json

API_URL = "http://localhost:8000"

def analyze_text(text):
    """Analyze sentiment of text"""
    response = requests.post(
        f"{API_URL}/analyze-sentiment",
        json={"text": text}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n{'='*60}")
        print(f"Text: {text}")
        print(f"{'='*60}")
        print(f"Sentiment: {result['sentiment'].upper()}")
        print(f"Confidence: {result['confidence']:.1%}")
        print(f"Explanation: {result['explanation']}")
        print(f"{'='*60}\n")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

# Test various inputs
if __name__ == "__main__":
    print("🎭 Sentiment Analysis Testing Tool\n")
    
    # Option 1: Pre-defined tests
    print("Running pre-defined tests...\n")
    
    test_cases = [
        "I love this product!",
        "This is terrible.",
        "The weather is okay today.",
        "Amazing service! Highly recommend!",
        "Worst experience ever. Never again.",
    ]
    
    for text in test_cases:
        analyze_text(text)
    
    # Option 2: Interactive mode
    print("\n" + "="*60)
    print("Interactive Mode - Enter your own text")
    print("="*60)
    print("(Press Ctrl+C to exit)\n")
    
    try:
        while True:
            user_input = input("Enter text to analyze: ").strip()
            if user_input:
                analyze_text(user_input)
            else:
                print("Please enter some text.\n")
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")