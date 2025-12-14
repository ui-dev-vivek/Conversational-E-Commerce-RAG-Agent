"""
Test LLM-based Intent Detection

Run this script to test if the LLM can correctly identify intents
for various user messages.
"""

import sys
import json
import asyncio
from pathlib import Path

# Add server path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.llm_intent_detector import detect_intent_with_llm


TEST_CASES = [
    # Cart queries - various ways to ask
    ("what is in my cart", "view_cart"),
    ("show my cart", "view_cart"),
    ("mere cart mein kya hai", "view_cart"),
    ("cart dikhao", "view_cart"),
    ("mera cart dekho", "view_cart"),
    
    # Add to cart - various ways
    ("add blue kurti to cart", "add_to_cart"),
    ("mere cart mein lavender candle daalo", "add_to_cart"),
    ("i want to buy this kurti", "search_products"),
    
    # Product search - various ways
    ("show me candles", "search_products"),
    ("do you have blue kurtis", "search_products"),
    ("dhundo candles ko", "search_products"),
    ("lavender soap hai kya", "search_products"),
    
    # Order tracking
    ("where is my order", "track_order"),
    ("track my order", "track_order"),
    ("mera order kaha hai", "track_order"),
    
    # Remove from cart
    ("remove kurti from cart", "remove_from_cart"),
    ("cart se soap nikalo", "remove_from_cart"),
    
    # Clear cart
    ("empty my cart", "clear_cart"),
    ("clear cart", "clear_cart"),
    
    # List orders
    ("show my orders", "list_orders"),
    ("mere orders dikhao", "list_orders"),
    
    # General questions - should NOT use tools
    ("hello how are you", None),
    ("what is your return policy", None),
    ("do you have shipping to delhi", None),
]


def test_intent_detection():
    """Test LLM intent detection with various messages"""
    
    print("=" * 80)
    print("🤖 Testing LLM-based Intent Detection")
    print("=" * 80)
    
    passed = 0
    failed = 0
    
    for user_message, expected_tool in TEST_CASES:
        print(f"\n📝 Message: '{user_message}'")
        print(f"   Expected Tool: {expected_tool or 'RAG (no tool)'}")
        
        try:
            intent_data = detect_intent_with_llm(user_message)
            
            detected_tool = intent_data.get('tool_name') if intent_data.get('should_use_tool') else None
            
            print(f"   Detected Tool: {detected_tool or 'RAG (no tool)'}")
            print(f"   Reasoning: {intent_data.get('reasoning')}")
            
            # Check if result matches expected
            if detected_tool == expected_tool:
                print("   ✅ PASS")
                passed += 1
            else:
                print(f"   ❌ FAIL - Expected {expected_tool}, got {detected_tool}")
                failed += 1
                
        except Exception as e:
            print(f"   ❌ ERROR: {e}")
            failed += 1
    
    print("\n" + "=" * 80)
    print(f"📊 Results: {passed} passed, {failed} failed out of {len(TEST_CASES)}")
    print("=" * 80)
    
    return failed == 0


if __name__ == "__main__":
    success = test_intent_detection()
    sys.exit(0 if success else 1)
