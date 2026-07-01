#!/usr/bin/env python3
import sys
import traceback

try:
    import importlib.util
    spec = importlib.util.spec_from_file_location("admin_server", "admin_server.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    print("admin_server.py OK")
    print(f"Handler: {module.Handler}")
except Exception as e:
    print(f"FAIL: {e}")
    traceback.print_exc()
