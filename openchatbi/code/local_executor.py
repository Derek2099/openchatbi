import sys
from io import StringIO

from openchatbi.code.executor_base import ExecutorBase


class LocalExecutor(ExecutorBase):

    def run_code(self, code: str) -> str:
        safe_globals = {"__builtins__": __builtins__}
        
        # Pre-import commonly used libraries as mentioned in agent_prompt.md
        # These are the libraries available for run_python_code tool
        try:
            import pandas as pd
            import numpy as np
            import matplotlib
            import matplotlib.pyplot as plt
            import seaborn as sns
            import requests
            import json
            
            # Make libraries available in the execution environment
            safe_globals['pd'] = pd
            safe_globals['pandas'] = pd
            safe_globals['np'] = np
            safe_globals['numpy'] = np
            safe_globals['plt'] = plt
            safe_globals['matplotlib'] = matplotlib
            safe_globals['sns'] = sns
            safe_globals['seaborn'] = sns
            safe_globals['requests'] = requests
            safe_globals['json'] = json
        except ImportError as e:
            # If any library is not available, continue without it
            # This allows the code to work even if some libraries are missing
            pass
        
        # Load local datasets if available
        try:
            from openchatbi.config_loader import ConfigLoader
            config_loader = ConfigLoader()
            config = config_loader.get()
            if config.local_dataset_manager:
                # Pre-load datasets as pandas DataFrames
                datasets = config.local_dataset_manager.load_all_datasets()
                safe_globals.update(datasets)
        except Exception:
            # If config not available or datasets can't be loaded, continue without them
            pass
        
        original_stdout = sys.stdout
        output_buffer = StringIO()
        sys.stdout = output_buffer
        try:
            exec(code, safe_globals, safe_globals)
            output = output_buffer.getvalue()
            return True, output
        except Exception as e:
            return False, str(e)
        finally:
            sys.stdout = original_stdout
