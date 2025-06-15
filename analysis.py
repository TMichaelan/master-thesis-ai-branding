# ====================== 1.  IMPORTS & SETTINGS ======================
import os, re, pandas as pd, numpy as np, seaborn as sns, matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
from pingouin import cronbach_alpha
from contextlib import redirect_stdout

sns.set_theme(style="whitegrid")

DATA_PATH = "data/data.csv"
OUT_DIR   = "results"
os.makedirs(OUT_DIR, exist_ok=True)

AI_BRANDS    = ['Ecotiva','Visioniq','Fidelicon','Seraphic','Etiera','Verdura']
HUMAN_BRANDS = ['Grove Collaborative','Plaid','Northvolt','Klevu',
                'Norse Projects','Seedlip']

LIKERT = {'Very bad':1,'Bad':2,'Neutral':3,'Good':4,'Very good':5}

REC_KEYWORDS = ['recommend', 'logo']
SUMMARY_FILE = f"{OUT_DIR}/stat_tests_summary.txt"

# ====================== 2.  HELPER FUNCTIONS =======================
def find_col(df, keywords):
    patt = re.compile('.*'.join(map(re.escape, keywords)), flags=re.I)
    cols = [c for c in df.columns if patt.search(c)]
    if not cols:
        raise KeyError(f"No column matches keywords: {keywords}")
    return cols[0]

def col_for(df, phrase, brand):
    return find_col(df, [phrase, brand])

# ====================== 3.  LOAD & LONG FORMAT =====================
def load_long(path=DATA_PATH):
    raw = pd.read_csv(path)
    rec_col = find_col(raw, REC_KEYWORDS)
    raw[rec_col] = pd.to_numeric(raw[rec_col], errors="coerce")

    records = []
    for ridx, row in raw.iterrows():
        rec = row[rec_col]
        for br in AI_BRANDS + HUMAN_BRANDS:
            try:
                mem  = pd.to_numeric(row[col_for(raw, "memorable",  br)], errors="coerce")
                attr = pd.to_numeric(row[col_for(raw, "attractive", br)], errors="coerce")
                clar_raw = row[col_for(raw, "rate the name", br)]
                clar = pd.to_numeric(clar_raw, errors="coerce")
                if pd.isna(clar):
                    clar = LIKERT.get(str(clar_raw).strip(), np.nan)
            except KeyError:
                continue
            records.append([ridx, br,
                            'AI' if br in AI_BRANDS else 'Human',
                            mem, attr, clar, rec])
    return pd.DataFrame(records, columns=[
        "resp_id","brand","origin",
        "memorability","attractiveness","clarity","recommendation"
    ])

df_long = load_long()

# ====================== 4.  ANALYSIS (captured to file) =============
with open(SUMMARY_FILE, "w", encoding="utf-8") as fh, redirect_stdout(fh):

    print(df_long.head(), "\n")

    # 4.1  Cronbach’s alpha
    def alpha_for(var):
        wide = df_long.pivot_table(index="resp_id", columns="brand", values=var)
        return round(cronbach_alpha(wide.dropna(axis=1, how='all'))[0], 3)

    print("Cronbach’s α:")
    for v in ["memorability","attractiveness","clarity"]:
        print(f"• {v.title():13s}: {alpha_for(v)}")

    # 4.2  Welch t-tests
    print("\nWelch t-tests (AI vs Human):")
    ai  = df_long[df_long.origin=="AI"   ].groupby("resp_id").mean(numeric_only=True)
    hum = df_long[df_long.origin=="Human"].groupby("resp_id").mean(numeric_only=True)
    for col in ["memorability","attractiveness","clarity"]:
        t, p = stats.ttest_ind(ai[col], hum[col], equal_var=False, nan_policy="omit")
        print(f"• {col.title():13s}: t = {t:6.3f}   p = {p:7.4f}")

    # 4.3  OLS regression
    agg = df_long.groupby("resp_id").mean(numeric_only=True).dropna()
    X = sm.add_constant(agg[["memorability","attractiveness","clarity"]])
    model = sm.OLS(agg["recommendation"], X).fit()
    print("\nOLS regression (respondent level):")
    print(model.summary())

print(f"✔  Analysis summary saved to {SUMMARY_FILE}")

# ====================== 5.  VISUALISATIONS ==========================
def save_histograms():
    for attr in ["memorability","attractiveness","clarity"]:
        plt.figure(figsize=(6,4))
        sns.histplot(data=df_long, x=attr, hue="origin",
                     kde=True, bins=5, palette="Set2", edgecolor="w")
        plt.xlim(1,5); plt.ylim(0)
        plt.title(f"{attr.title()} Distribution by Brand Origin")
        plt.tight_layout()
        plt.savefig(f"{OUT_DIR}/{attr}_hist.png", dpi=300)
        plt.close()

def save_bar_means():
    mean_df = (df_long.groupby("origin")
              [["memorability","attractiveness","clarity"]].mean()
              .reset_index().melt(id_vars="origin", var_name="Attribute", value_name="Mean"))
    plt.figure(figsize=(7,4))
    sns.barplot(data=mean_df, x="Attribute", y="Mean",
                hue="origin", palette="Set2", errorbar="se")
    plt.ylim(0,5)
    plt.ylabel("Mean score")
    plt.title("Mean Attribute Ratings by Origin")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/mean_attribute_ratings.png", dpi=300)
    plt.close()

def save_corr_heatmap():
    corr = df_long[["memorability","attractiveness","clarity"]].corr(method="spearman")
    plt.figure(figsize=(4,3.5))
    sns.heatmap(corr, annot=True, vmin=-1, vmax=1, cmap="coolwarm", fmt=".2f")
    plt.title("Spearman correlation")
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/spearman_corr.png", dpi=300)
    plt.close()

save_histograms()
save_bar_means()
save_corr_heatmap()

print("✔  Plots saved in", OUT_DIR)


# ===============================================================
# 1. SETTINGS & HELPERS
# ===============================================================
import os, re, numpy as np, pandas as pd, matplotlib.pyplot as plt
from scipy.stats import binomtest

OUT_DIR = "results"
DATA_PATH = "data/data.csv"
os.makedirs(OUT_DIR, exist_ok=True)

PAIR_COLS = [
    'Which logo do you prefer? (Norse Projects or Etiera)',
    'Which brand name do you prefer? (Norse Projects or Etiera)',
    'Which logo do you prefer? (Verdura or Seedlip)',
    'Which brand name do you prefer? (Verdura or Seedlip)',
    'Which logo do you prefer? (Ecotiva or Groove Collaborative)',
    'Which brand name do you prefer? (Ecotiva or Groove Collaborative)',
    'Which logo do you prefer? (Seraphic or Plaid)',
    'Which brand name do you prefer? (Seraphic or Plaid)',
]
AI_SET = {'Etiera','Verdura','Ecotiva','Seraphic'}

df = pd.read_csv(DATA_PATH)

def parse_pair(txt: str):
    m = re.search(r'\((.*?)\s+or\s+(.*?)\)', txt)
    return m.group(1).strip(), m.group(2).strip()

# ===============================================================
# 2. PAIRWISE COMPUTATION
# ===============================================================
rows = []
for col in PAIR_COLS:
    if col not in df.columns:
        print(f"⚠ Column not found: {col}"); continue

    first, second = parse_pair(col)
    ai_brand  = first if first in AI_SET else second
    human_br  = second if ai_brand == first else first
    ai_pos    = 1 if ai_brand == first else 2
    human_pos = 2 if ai_pos == 1 else 1

    ai_votes = human_votes = 0
    for v in df[col]:
        if pd.isna(v): continue
        if str(v).strip().isdigit():
            ai_votes    += (int(v) == ai_pos)
            human_votes += (int(v) == human_pos)
        else:
            val = str(v).strip().lower()
            ai_votes    += (val == ai_brand.lower())
            human_votes += (val == human_br.lower())

    total = ai_votes + human_votes
    p_val   = binomtest(ai_votes, total, 0.5).pvalue if total else np.nan
    ai_share = round(ai_votes/total, 3) if total else np.nan

    rows.append([
        'Logo' if 'logo' in col.lower() else 'Name',
        f'{ai_brand} vs {human_br}',
        ai_votes, human_votes, total, ai_share,
        round(p_val, 4) if total else 'NA'
    ])

pref_df = pd.DataFrame(rows, columns=[
    'Type','Pair','AI_votes','Human_votes','N_total','AI_share','p_value'
])
pref_df.to_csv(f"{OUT_DIR}/pairwise_preference.csv", index=False)

# ===============================================================
# 3. WRITE TEXT SUMMARY
# ===============================================================
with open(f"{OUT_DIR}/pairwise_preference_summary.txt", "w") as f:
    f.write(pref_df.to_string(index=False))
print("✔  Results saved to results/pairwise_preference.csv and …summary.txt")

# ===============================================================
# 4. PLOTS
# ===============================================================
pref_df['Human_share'] = 1 - pref_df['AI_share']

def plot_pref(sub, fname, title):
    pairs, ai_s, hum_s = sub['Pair'], sub['AI_share'], sub['Human_share']
    y = range(len(pairs))

    plt.figure(figsize=(8, 3.5))
    plt.barh(y, hum_s, color='#d95f02', label='Human')
    plt.barh(y, ai_s,  color='#1b9e77', left=hum_s, label='AI')

    plt.yticks(y, pairs)
    plt.axvline(0.5, ls='--', c='gray')
    plt.xlim(0, 1)
    plt.xlabel('Share of votes')
    plt.title(title)

    for j, (ai, hum) in enumerate(zip(ai_s, hum_s)):
        plt.text(hum + ai + 0.02, j, f'{ai*100:.1f} %', va='center')
        plt.text(hum/2, j, f'{hum*100:.1f} %', va='center',
                 color='white', ha='center', fontsize=8)

    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/{fname}", dpi=300)
    plt.close()

plot_pref(pref_df[pref_df.Type == 'Logo'],
          'ai_logo_preference.png',
          'Preference split – Logos (AI vs Human)')

plot_pref(pref_df[pref_df.Type == 'Name'],
          'ai_name_preference.png',
          'Preference split – Names (AI vs Human)')

print("✔  Figures saved in results/")


# ===============================================================
# 1. SETTINGS & HELPER
# ===============================================================
import os, re, pandas as pd, matplotlib.pyplot as plt, seaborn as sns
from scipy.stats import ttest_ind

OUT_DIR = "results"
os.makedirs(OUT_DIR, exist_ok=True)

BRAND_INDUSTRY = {
    # --- HUMAN --------------------------------------------------
    'grove collaborative': {'health'},
    'plaid'              : {'finance', 'tech'},
    'northvolt'          : {'industry'},
    'klevu'              : {'tech'},
    'norse projects'     : {'fashion'},
    'seedlip'            : {'food'},
    # --- AI -----------------------------------------------------
    'ecotiva'            : {'health'},
    'visioniq'           : {'tech'},
    'fidelicon'          : {'tech'},
    'seraphic'           : {'health'},
    'etiera'             : {'fashion'},
    'verdura'            : {'health'},
}

def extract_brand(text: str) -> str | None:
    """Returns brand name from 'What industry does "Brand" belong to?'."""
    for pattern in [r'"([^"]+)"', r'"([^"?]+)\??', r'does\s+"?([^"?]+?)\??"?\s+belong']:
        m = re.search(pattern, text, flags=re.I)
        if m: return m.group(1).strip()
    return None

# ===============================================================
# 2. COMPUTE ACCURACY PER BRAND
# ===============================================================
industry_cols = [c for c in df.columns if c.lower().startswith('what industry')]

rows, flags = [], pd.Series(0, index=df.index, dtype=int)

for col in industry_cols:
    brand = extract_brand(col)
    if brand is None:
        print(f"⚠ Could not parse column: {col}");  continue
    key = brand.lower()
    if key not in BRAND_INDUSTRY:
        print(f"⚠ No ground-truth industry for {brand}");  continue

    valid_set = {x.lower() for x in BRAND_INDUSTRY[key]}
    answers   = df[col].astype(str).str.strip().str.lower()
    correct   = answers.isin(valid_set)

    flags |= correct.astype(int)
    total, hits = answers.notna().sum(), correct.sum()
    accuracy = round(hits/total, 3) if total else None
    rows.append([brand, ', '.join(valid_set), hits, total, accuracy])

acc_df = pd.DataFrame(rows,
    columns=['Brand','TrueIndustry','Correct','Total','Accuracy'])
acc_df['Origin'] = acc_df['Brand'].str.lower().isin(
    ['ecotiva','visioniq','fidelicon','seraphic','etiera','verdura']
).map({True:'AI', False:'Human'})

acc_df.to_csv(f"{OUT_DIR}/industry_accuracy.csv", index=False)
df['correct_industry_answers'] = flags   # attention flag

# ===============================================================
# 3. TEXT SUMMARY
# ===============================================================
ai_acc  = acc_df.loc[acc_df.Origin=='AI',   'Accuracy']
hum_acc = acc_df.loc[acc_df.Origin=='Human','Accuracy']
t, p    = ttest_ind(ai_acc, hum_acc, equal_var=False)

with open(f"{OUT_DIR}/industry_accuracy_summary.txt", "w") as fh:
    fh.write("Industry-identification accuracy per brand\n")
    fh.write(acc_df.to_string(index=False))
    fh.write("\n\nGroup means & Welch t-test\n")
    fh.write(f"Mean AI    = {ai_acc.mean():.3f}\n")
    fh.write(f"Mean Human = {hum_acc.mean():.3f}\n")
    fh.write(f"Welch t = {t:.2f}  (p = {p:.4f})\n")

print("✔  Files saved: industry_accuracy.csv, industry_accuracy_summary.txt")

# ===============================================================
# 4. PLOT
# ===============================================================
sns.set_theme(style="whitegrid")
plt.figure(figsize=(7,4.5))
sns.barplot(data=acc_df.sort_values('Accuracy'),
            x='Accuracy', y='Brand', hue='Origin',
            palette={'AI':'#1b9e77','Human':'#d95f02'})
plt.xlim(0,1)
plt.xlabel('Accuracy of industry identification')
plt.ylabel('')
plt.axvline(acc_df['Accuracy'].mean(), color='gray', ls='--', label='Overall mean')
plt.title('Frequency of correct industry guesses per brand')
plt.legend(loc='lower right')
plt.tight_layout()
plt.savefig(f"{OUT_DIR}/industry_accuracy_plot.png", dpi=300)
plt.close()
print("✔  Plot saved as industry_accuracy_plot.png in results/")


# ===============================================================
# 6.1  DESCRIPTIVE STATISTICS (means by origin)
# ===============================================================
import pandas as pd, os
OUT_DIR = "results"
os.makedirs(OUT_DIR, exist_ok=True)

mean_df = (df_long
           .groupby("origin")[["memorability","attractiveness","clarity"]]
           .mean()
           .round(2)                    
           .rename_axis(None))

# Save to CSV & text
mean_df.to_csv(f"{OUT_DIR}/descriptive_means.csv")
with open(f"{OUT_DIR}/descriptive_means.txt", "w") as fh:
    fh.write("Mean attribute scores by brand origin\n")
    fh.write(mean_df.to_string())

print(mean_df)
print("\n✔  Files saved: descriptive_means.csv / .txt in results/")
