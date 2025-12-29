import sys
from io import StringIO

from RestrictedPython import compile_restricted, safe_globals, utility_builtins
from RestrictedPython.Guards import safe_builtins, safer_getattr

from openchatbi.code.executor_base import ExecutorBase


class RestrictedLocalExecutor(ExecutorBase):

    def run_code(self, code: str) -> (bool, str):
        try:
            # compile restricted code
            byte_code = compile_restricted(code, "<string>", "exec")
            if byte_code is None:
                return False, "Failed to compile restricted code"

            restricted_locals = {}
            restricted_globals = safe_globals.copy()

            # Set up restricted environment with necessary functions
            restricted_globals.update(safe_builtins)
            restricted_globals["_getattr_"] = safer_getattr
            restricted_globals["__builtins__"] = utility_builtins

            # Pre-import commonly used libraries as mentioned in agent_prompt.md
            try:
                import pandas as pd
                import numpy as np
                import matplotlib
                import matplotlib.pyplot as plt
                import seaborn as sns
                import requests
                import json
                
                # Make libraries available in the restricted execution environment
                restricted_globals['pd'] = pd
                restricted_globals['pandas'] = pd
                restricted_globals['np'] = np
                restricted_globals['numpy'] = np
                restricted_globals['plt'] = plt
                restricted_globals['matplotlib'] = matplotlib
                restricted_globals['sns'] = sns
                restricted_globals['seaborn'] = sns
                restricted_globals['requests'] = requests
                restricted_globals['json'] = json
            except ImportError:
                # If any library is not available, continue without it
                pass

            # Load local datasets if available
            try:
                from openchatbi.config_loader import ConfigLoader
                config_loader = ConfigLoader()
                config = config_loader.get()
                if config.local_dataset_manager:
                    # Pre-load datasets as pandas DataFrames
                    datasets = config.local_dataset_manager.load_all_datasets()
                    restricted_globals.update(datasets)
            except Exception:
                # If config not available or datasets can't be loaded, continue without them
                pass

            # Add variable definitions to the restricted locals
            for key, value in self._variable.items():
                restricted_locals[key] = value

            # Capture print output
            original_stdout = sys.stdout
            output_buffer = StringIO()
            sys.stdout = output_buffer

            # Use the standard print function for RestrictedPython
            restricted_globals["_print_"] = lambda *args, **kwargs: print(*args, **kwargs)

            exec(byte_code, restricted_globals, restricted_locals)
            output = output_buffer.getvalue()

            return True, output

        except Exception as e:
            return False, str(e)
        finally:
            if "original_stdout" in locals():
                sys.stdout = original_stdout
