import importlib
import pkgutil
from typing import List
from fasthtml.core import FastHTML, APIRouter
import logging

logger = logging.getLogger(__name__)

def collect_rt_instances(package_name: str = "modules") -> List[APIRouter]:
    rt_list = []
    
    # Import the modules package
    try:
        modules_package = importlib.import_module(package_name)
    except ImportError as e:
        logger.error(f"Failed to import {package_name} package: {e}")
        return rt_list
    
    for loader, module_name, is_pkg in pkgutil.walk_packages(
        modules_package.__path__, modules_package.__name__ + "."
    ):
        try:
            # Try to import the module
            module = importlib.import_module(module_name)
            
            # Check for direct rt attribute
            if hasattr(module, "rt"):
                rt_attr = getattr(module, "rt")
                rt_list.append(rt_attr)
                logger.info(f"Imported routes from {module_name}")
            
            # If it's a package and has 'routes' in its name, walk through all its modules
            elif is_pkg and 'routes' in module_name:
                package_path = module.__path__
                for sub_loader, sub_module_name, _ in pkgutil.walk_packages(
                    package_path, module_name + "."
                ):
                    try:
                        sub_module = importlib.import_module(sub_module_name)
                        if hasattr(sub_module, "rt"):
                            rt_attr = getattr(sub_module, "rt")
                            rt_list.append(rt_attr)
                            logger.info(f"Imported routes from {sub_module_name}")
                    except Exception as e:
                        logger.error(f"Failed to import {sub_module_name}: {e}")
                
        except Exception as e:
            logger.error(f"Failed to import {module_name}: {e}")
    
    return rt_list

def add_routes(app: FastHTML) -> FastHTML:
    routes = collect_rt_instances()
    for rt in routes:
        rt.to_app(app)
    return app
