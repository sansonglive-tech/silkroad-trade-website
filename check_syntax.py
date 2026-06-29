import sys
sys.path.insert(0, r'C:\Users\ASDCF\.qclaw\workspace')
# Import the admin_server module to syntax check
import importlib.util
spec = importlib.util.spec_from_file_location('admin', r'C:\Users\ASDCF\.qclaw\workspace\admin_server.py')
mod = importlib.util.module_from_spec(spec)
# Don't load (would start server) - just syntax check
with open(r'C:\Users\ASDCF\.qclaw\workspace\admin_server.py', 'r') as f:
    code = f.read()
compile(code, 'admin_server.py', 'exec')
print('Syntax OK')
