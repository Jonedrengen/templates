"""
Basic Python Class Template

This template provides a skeleton for creating a Python class with common patterns.
"""


class ClassName:
    """
    Brief description of what this class does.
    
    Attributes:
        attribute_name (type): Description of the attribute
    """
    
    def __init__(self, param1, param2=None):
        """
        Initialize the class instance.
        
        Args:
            param1: Description of param1
            param2: Description of param2 (optional)
        """
        self.param1 = param1
        self.param2 = param2
    
    def method_name(self, arg):
        """
        Description of what this method does.
        
        Args:
            arg: Description of the argument
            
        Returns:
            Description of return value
            
        Raises:
            ExceptionType: Description of when this exception is raised
        """
        # Implementation here
        pass
    
    def __str__(self):
        """Return string representation of the object."""
        return f"ClassName(param1={self.param1}, param2={self.param2})"
    
    def __repr__(self):
        """Return unambiguous representation of the object."""
        return f"ClassName({self.param1!r}, {self.param2!r})"


# Example usage
if __name__ == "__main__":
    instance = ClassName("value1", "value2")
    print(instance)
