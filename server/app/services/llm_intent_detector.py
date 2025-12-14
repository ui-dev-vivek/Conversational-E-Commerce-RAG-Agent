"""
LLM-based Intent Detection Service.

Uses the LLM to intelligently understand user intent and decide:
1. Should a tool be called?
2. Which tool should be called?
3. What are the parameters for the tool?
"""

import json
import logging
from typing import Dict, Optional, List
from langchain_core.prompts import ChatPromptTemplate
from ..config.llm_config import LLM

logger = logging.getLogger(__name__)

# Initialize LLM
llm = LLM.invoke()


INTENT_DETECTION_PROMPT = """You are an expert shopping assistant for AJ Creations e-commerce store.

Available Tools:
1. search_products - Search for products by keywords or category
2. list_categories - List all product categories
3. view_cart - Show items in user's shopping cart
4. add_to_cart - Add a product to cart
5. remove_from_cart - Remove a product from cart
6. clear_cart - Empty the entire cart
7. list_orders - Show user's order history
8. track_order - Track a specific order
9. get_product_details - Get detailed info about a product

User Message: {user_message}

IMPORTANT: You must respond with ONLY a JSON object (no markdown, no extra text).

Analyze the user message and decide:
1. Should a tool be called? (yes/no)
2. If yes, which tool?
3. What are the extracted parameters?

Return JSON in this exact format:
{{
    "should_use_tool": true/false,
    "tool_name": "tool_name_or_null",
    "parameters": {{}},
    "reasoning": "brief explanation"
}}

Examples:
- "show me candles" → {{"should_use_tool": true, "tool_name": "search_products", "parameters": {{"query": "candles"}}, "reasoning": "User wants to search products"}}
- "add blue kurti to my cart" → {{"should_use_tool": true, "tool_name": "add_to_cart", "parameters": {{"product_name": "blue kurti"}}, "reasoning": "User wants to add product to cart"}}
- "what's in my cart" → {{"should_use_tool": true, "tool_name": "view_cart", "parameters": {{}}, "reasoning": "User wants to view cart contents"}}
- "where is my order" → {{"should_use_tool": true, "tool_name": "track_order", "parameters": {{}}, "reasoning": "User wants to track order"}}
- "hello, how are you?" → {{"should_use_tool": false, "tool_name": null, "parameters": {{}}, "reasoning": "Casual greeting, no tool needed"}}
- "do you have any candles?" → {{"should_use_tool": true, "tool_name": "search_products", "parameters": {{"query": "candles"}}, "reasoning": "User inquiring about product availability"}}

Now analyze this message and respond with ONLY the JSON object."""


def detect_intent_with_llm(user_message: str) -> Dict:
    """
    Use LLM to intelligently detect user intent and decide if tool should be called.
    
    Args:
        user_message: User's message
        
    Returns:
        Dict with:
        - should_use_tool: bool
        - tool_name: str or None
        - parameters: dict
        - reasoning: str
    """
    try:
        # Create prompt
        prompt = ChatPromptTemplate.from_template(INTENT_DETECTION_PROMPT)
        
        # Invoke LLM
        response = llm.invoke(
            prompt.format_messages(user_message=user_message)
        )
        
        # Extract text
        response_text = response.content.strip()
        
        logger.info(f"🤖 LLM Intent Response: {response_text}")
        
        # Parse JSON
        intent_data = json.loads(response_text)
        
        logger.info(f"✅ Parsed Intent: {intent_data}")
        
        return intent_data
        
    except json.JSONDecodeError as e:
        logger.error(f"❌ Failed to parse LLM response as JSON: {e}")
        logger.error(f"Raw response: {response_text}")
        # Fallback: return empty tool call
        return {
            "should_use_tool": False,
            "tool_name": None,
            "parameters": {},
            "reasoning": f"Failed to parse intent: {str(e)}"
        }
    except Exception as e:
        logger.error(f"❌ Error in LLM intent detection: {e}", exc_info=True)
        return {
            "should_use_tool": False,
            "tool_name": None,
            "parameters": {},
            "reasoning": f"Error in intent detection: {str(e)}"
        }


def extract_tool_parameters(tool_name: str, user_message: str, llm_params: Dict) -> Dict:
    """
    Extract and validate tool parameters from user message.
    
    Args:
        tool_name: Name of the tool to be called
        user_message: Original user message
        llm_params: Parameters suggested by LLM
        
    Returns:
        Dict with validated parameters for the tool
    """
    
    parameters = llm_params.copy()
    
    # Add default parameters based on tool type
    if tool_name == 'search_products':
        if 'query' not in parameters:
            parameters['query'] = user_message
        if 'limit' not in parameters:
            parameters['limit'] = 5
            
    elif tool_name == 'add_to_cart':
        # For add_to_cart, we need to look up the product in database
        from ..config.database import SessionLocal
        from ..models.models import Product
        
        product_name = parameters.get('product_name', user_message)
        
        # Search for product in database
        db = SessionLocal()
        try:
            product = db.query(Product).filter(
                Product.name.ilike(f"%{product_name}%")
            ).first()
            
            if product:
                parameters['product_id'] = product.sku
                if 'quantity' not in parameters:
                    parameters['quantity'] = 1
                logger.info(f"✅ Found product for cart: {product.name} (SKU: {product.sku})")
            else:
                logger.warning(f"⚠️ Product not found in database: {product_name}")
                # Keep the product_name so tool can handle the error
                
        except Exception as e:
            logger.error(f"❌ Error looking up product: {e}")
        finally:
            db.close()
            
    elif tool_name == 'remove_from_cart':
        if 'product_name' not in parameters:
            parameters['product_name'] = user_message
            
    elif tool_name in ['view_cart', 'clear_cart', 'list_categories', 'list_orders']:
        # These tools don't need additional parameters
        parameters = {}
        
    elif tool_name == 'track_order':
        # Try to extract order ID if provided
        if 'order_id' not in parameters:
            # Look for patterns like "order 123" or "#123"
            import re
            match = re.search(r'(?:order\s*[#]?)?(\d+)', user_message.lower())
            if match:
                parameters['order_id'] = match.group(1)
                
    elif tool_name == 'get_product_details':
        if 'product_id' not in parameters:
            parameters['product_id'] = user_message
    
    logger.info(f"✅ Extracted parameters for {tool_name}: {parameters}")
    
    return parameters
