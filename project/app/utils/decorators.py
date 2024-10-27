from functools import wraps
from typing import Any, Callable

def template(wrapper_component: Callable, *wrapper_args: Any, **wrapper_kwargs: Any) -> Callable:
    """
    A decorator factory that wraps a component function with another component.
    
    Args:
        wrapper_component: The component function to use as a wrapper
        *wrapper_args: Additional positional arguments to pass to the wrapper component
        **wrapper_kwargs: Additional keyword arguments to pass to the wrapper component
    
    Returns:
        A decorator function that wraps the target component
    
    Example:
        @component_wrapper(Main, cls="dashboard")
        def my_component(*args, **kwargs):
            return Div(*args, **kwargs)
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Call the original function to get its content
            inner_content = func(*args, **kwargs)
            # Wrap the content with the wrapper component
            return wrapper_component(
                inner_content,
                *wrapper_args,
                **wrapper_kwargs
            )
        return wrapper
    return decorator
