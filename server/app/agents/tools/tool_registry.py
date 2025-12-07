"""
Central registry of all available agent tools.
"""

from typing import Dict, List, Any
from .product_tools import SearchProductsTool, GetProductDetailsTool, ListCategoriesTool
from .cart_tools import AddToCartTool, ViewCartTool, RemoveFromCartTool, ClearCartTool
from .order_tools import GetOrderStatusTool, ListOrdersTool, CreateOrderTool, TrackOrderTool


class ToolRegistry:
    """
    Central registry for all agent tools.
    Provides easy access to tools and their metadata.
    """
    
    def __init__(self):
        """Initialize the tool registry with all available tools."""
        # Product tools
        self.search_products = SearchProductsTool()
        self.get_product_details = GetProductDetailsTool()
        self.list_categories = ListCategoriesTool()
        
        # Cart tools
        self.add_to_cart = AddToCartTool()
        self.view_cart = ViewCartTool()
        self.remove_from_cart = RemoveFromCartTool()
        self.clear_cart = ClearCartTool()
        
        # Order tools
        self.get_order_status = GetOrderStatusTool()
        self.list_orders = ListOrdersTool()
        self.create_order = CreateOrderTool()
        self.track_order = TrackOrderTool()
        
        # Build tool map
        self.tools = {
            "search_products": self.search_products,
            "get_product_details": self.get_product_details,
            "list_categories": self.list_categories,
            "add_to_cart": self.add_to_cart,
            "view_cart": self.view_cart,
            "remove_from_cart": self.remove_from_cart,
            "clear_cart": self.clear_cart,
            "get_order_status": self.get_order_status,
            "list_orders": self.list_orders,
            "create_order": self.create_order,
            "track_order": self.track_order,
        }
    
    def get_tool(self, tool_name: str):
        """
        Get a tool by name.
        
        Args:
            tool_name: Name of the tool
            
        Returns:
            Tool instance or None if not found
        """
        return self.tools.get(tool_name)
    
    def get_all_tools(self) -> Dict[str, Any]:
        """
        Get all registered tools.
        
        Returns:
            Dict of all tools
        """
        return self.tools
    
    def get_tool_names(self) -> List[str]:
        """
        Get list of all tool names.
        
        Returns:
            List of tool names
        """
        return list(self.tools.keys())
    
    def get_tool_descriptions(self) -> List[Dict[str, str]]:
        """
        Get descriptions of all tools for LLM context.
        
        Returns:
            List of tool descriptions
        """
        return [
            {
                "name": tool.name,
                "description": tool.description
            }
            for tool in self.tools.values()
        ]
    
    def execute_tool(self, tool_name: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a tool by name with given parameters.
        
        Args:
            tool_name: Name of the tool to execute
            **kwargs: Tool parameters
            
        Returns:
            Tool execution result
        """
        tool = self.get_tool(tool_name)
        if not tool:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            }
        
        return tool.run(**kwargs)


# Global tool registry instance
tool_registry = ToolRegistry()
