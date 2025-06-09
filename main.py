from src.data_processing import load_and_prepare_data
from src.analysis import run_analysis
from src.visualization import make_all_plots

def main():
    df_long = load_and_prepare_data("data/data.csv")
    run_analysis(df_long)
    make_all_plots(df_long, img_dir="img")

if __name__ == "__main__":
    main()
    