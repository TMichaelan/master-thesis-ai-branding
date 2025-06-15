# AI vs Human Brand Name Survey Analysis

This project analyzes survey data comparing AI-generated and human-created brand names. It calculates reliability, performs statistical tests, and visualizes results. All plots and result files are saved in the `results/` directory.

## Project Structure

```
.
├── data/
│   └── data.csv                # Your survey data file
├── results/                    # Output directory for plots and result tables
│   ├── *.png                   # Plots (histograms, barplots, etc.)
│   ├── *.csv                   # Summary tables
│   └── *.txt                   # Statistical test summaries
├── analysis.py                 # Main analysis script
├── requirements.txt            # Python dependencies
├── AI_Brand_Analysis.ipynb     # Jupyter notebook (optional)
└── README.md                   # Project description (this file)
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
   You can run the main script:
   ```
   python analysis.py
   ```
   or use the Jupyter notebook `AI_Brand_Analysis.ipynb` for step-by-step exploration.

   This will:
   - Prepare and clean the data
   - Calculate Cronbach’s alpha for reliability
   - Compare AI and human brand ratings (means, t-tests)
   - Run regression analysis
   - Save all plots and result tables to the `results/` directory

## Main Components

- **analysis.py**  
  Loads the CSV, processes the data, runs all statistical analyses, and saves plots and tables to `results/`.

- **AI_Brand_Analysis.ipynb**  
  Jupyter notebook for interactive analysis and visualization (optional).

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

All generated plots and result files will be saved in the `results/` directory.

---

**Note:**  
Make sure your data columns match the expected format (see code in `analysis.py` for details).