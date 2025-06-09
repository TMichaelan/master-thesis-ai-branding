import numpy as np
from scipy.stats import ttest_ind
from pingouin import cronbach_alpha
import statsmodels.formula.api as smf

def run_analysis(df_long):
    print("Cronbach’s alpha:")
    for var in ['memorability', 'attractiveness', 'clarity']:
        wide = df_long.pivot(columns='brand', values=var)
        try:
            alpha = cronbach_alpha(wide)[0]
            print(f"- {var.title()}: {round(alpha, 3)}")
        except Exception as e:
            print(f"- {var.title()}: error → {e}")

    print("\nGroup means (AI vs Human):")
    print(df_long.groupby("origin")[['memorability', 'attractiveness', 'clarity']].mean().round(2))

    print("\nWelch’s t-tests by attribute:")
    for attr in ["memorability", "attractiveness", "clarity"]:
        t_result = ttest_ind(
            df_long[df_long["origin"] == "AI"][attr],
            df_long[df_long["origin"] == "Human"][attr],
            equal_var=False
        )
        print(f"- {attr.title()}: t = {t_result.statistic:.3f}, p = {t_result.pvalue:.4f}")

    print("\nSpearman Correlation Matrix:")
    corr = df_long[['memorability', 'attractiveness', 'clarity']].corr(method='spearman').round(2)
    print(corr)

    # Regression example
    df_long["recommendation"] = (0.3 * df_long["memorability"] +
                                 0.5 * df_long["attractiveness"] +
                                 0.4 * df_long["clarity"] +
                                 np.random.normal(0, 0.5, size=len(df_long)))
    model = smf.ols("recommendation ~ memorability + attractiveness + clarity", data=df_long).fit()
    print("\nOLS Regression Summary:")
    print(model.summary())
    