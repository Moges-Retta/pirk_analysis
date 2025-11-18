"""
PIRK Analysis Package

Provides tools for:
- Parsing and cleaning experimental PIRK/ECS data
- Fitting Dirk-PIRK models
- Calculating derived parameters
- Plotting traces and fit results
- Exporting fit tables and metrics
"""

# Expose common functions and submodules
from .parsing import *
from .fitting import *
from .calculations import *
from .plotting import *
from .reporting import *
from .utils import *

__version__ = "0.1.0"
