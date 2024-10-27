import importlib
import pkgutil

import app.pages as pages
from fasthtml.core import FastHTML


def collect_rt_instances(package):
    rt_list = []
    for loader, module_name, is_pkg in pkgutil.walk_packages(
        package.__path__, package.__name__ + "."
    ):
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, "rt"):
                rt_attr = getattr(module, "rt")
                rt_list.append(rt_attr)
                print(f"Imported {module_name} routes")
        except Exception as e:
            print(f"Failed to import {module_name}: {e}")
    return rt_list


routes = collect_rt_instances(pages)


def add_routes(app: FastHTML) -> FastHTML:
    for rt in routes:
        rt.to_app(app)
    return app
