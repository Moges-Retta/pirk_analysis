# PIRK Analysis Package

## Overview
**PIRK Analysis** is a Python package designed to process, fit, and visualize experimental PIRK/ECS (Pulse-Amplitude Modulation) data from photosynthesis experiments. The package supports:

- Parsing and cleaning experimental datasets  
- Fitting Dirk-PIRK models to ECS traces  
- Calculating derived parameters like amplitudes and lifetimes  
- Visualizing traces, fitted curves, and Pirk responses  
- Exporting fit tables and results for further analysis  

This package is aimed at researchers working with plant light-response experiments who need a structured and reproducible workflow.

---

## Features

- **Data parsing**: Load, clean, and correct genotype labels.
- **Model fitting**: Construct and fit Dirk-PIRK models with variable amplitude and lifetime components.
- **Calculations**: Derive metrics such as steady-state Pirk amplitudes and RMSE of fits.
- **Plotting**: Publication-ready figures of traces, Pirk points, and fitted curves.
- **Reporting**: Generate tables of fitted parameters, standard errors, and confidence intervals.

---

## Installation

```bash
# Clone the repository
git clone https://github.com/Moges-Retta/pirk_analysis.git
cd pirk_analysis

# Install requirements
pip install -r requirements.txt
```

---

## Usage

### Import the package
```python
import pandas as pd
from pirk import prep_traces_for_fitting, fit_pirk_dirk_selected_expt, plot_PAM
```

### Prepare data
```python
trace_x, trace_y, pirk_points, dirk_point_indexes = prep_traces_for_fitting(combined_df, index=0)
```

### Fit Dirk-PIRK model
```python
guess_dict = {
    'amplitude': 0.5,
    'lifetime': 0.1,
    'y_offset': 0,
    'pirk_begin_amplitude': 0.05,
    'pirk_end_amplitude': 0.3,
    'pirk_amplitude_recovery_lifetime': 0.2,
    'offset_amplitude': 0.1,
    'offset_lifetime': 0.5
}
fit_results = fit_pirk_dirk(combined_df, index=0, guess_dict=guess_dict)
```

### Plot traces
```python
plot_PAM(trace_y, i_inc=50, genotype="Col-0", replicate=1)
```

### Plot Pirk points with shaded Dirk period
```python
from pirk.plotting.traces import plot_traces_genotype_replicate

plot_traces_genotype_replicate(trace_y, trace_x, pirk_points, dirk_begin=0.35,
                               genotype="Col-0", replicate=1)
```

---

## Package Structure

```
pirk_analysis/
├── pirk/
│   ├── parsing/         # Data loading and cleaning
│   ├── fitting/         # Model construction and fitting
│   ├── calculations/    # Derived parameters
│   ├── plotting/        # Visualization routines
│   ├── reporting/       # Export fit tables
│   └── utils/           # Helper functions
├── scripts/             # CLI scripts for processing
├── tests/               # Unit tests
├── notebooks/           # Example analyses
└── README.md
```

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for bug fixes, new features, or improvements.  

---

## License

[MIT License](LICENSE)

