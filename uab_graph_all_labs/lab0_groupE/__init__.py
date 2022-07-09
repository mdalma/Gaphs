
import os
from os.path import dirname, basename, isfile, join
import glob
import importlib
modules_ = glob.glob(join(dirname(__file__), "*.py"))
base_module_name = basename(dirname(__file__))
for f in [f for f in modules_ if isfile(f) and not f.endswith('__init__.py')]:
    submodule_name = basename(f).replace(".py", "")
    globals()[submodule_name] = importlib.import_module(f"{base_module_name}.{submodule_name}", base_module_name)

