# AI vs Human Brand Name Survey Analysis

This project analyzes survey data comparing AI-generated and human-created brand names. It calculates reliability, performs statistical tests, and visualizes results. All plots are saved in the `img/` directory.

## Project Structure

```
.
├── data/
│   └── data.csv              # Your survey data file
├── img/                      # Output directory for plots
├── src/
│   ├── data_processing.py    # Data loading and transformation
│   ├── analysis.py           # Statistical analysis functions
│   └── visualization.py      # Plotting functions
├── main.py                   # Main script to run the analysis
├── requirements.txt          # Python dependencies
└── README.md                 # Project description (this file)
```

## How to Use

1. **Install dependencies**  
   Run in terminal:
   ```
   pip install -r requirements.txt
   ```

2. **Add your data**  
   Place your survey CSV file as `data/data.csv`.

3. **Run the analysis**  
   ```
   python main.py
   ```
   This will:
   - Prepare and clean the data
   - Calculate Cronbach’s alpha for reliability
   - Compare AI and human brand ratings (means, t-tests)
   - Run regression analysis
   - Save all plots to the `img/` directory

## Main Components

- **src/data_processing.py**  
  Loads the CSV, maps ratings to numbers, and reshapes the data for analysis.

- **src/analysis.py**  
  Calculates reliability (Cronbach’s alpha), group means, t-tests, correlations, and runs a regression.

- **src/visualization.py**  
  Generates and saves plots: barplots, histograms, and correlation heatmaps.

- **main.py**  
  Orchestrates the workflow: loads data, runs analysis, and creates plots.

## Requirements

- Python 3.11
- pandas
- numpy
- matplotlib
- seaborn
- scipy
- statsmodels
- pingouin

Install all dependencies with:
```
pip install -r requirements.txt
```

## Output

All generated plots will be saved in the `img/` directory.

---

**Note:**  
Make sure your data columns match the expected format (see `src/data_processing.py` for details).