import os
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def make_all_plots(df_long, img_dir="img"):
    os.makedirs(img_dir, exist_ok=True)
    attributes = ['memorability', 'attractiveness', 'clarity']

    # Barplot of means
    plt.figure(figsize=(6, 4))
    sns.barplot(data=df_long, x="origin", y="memorability", errorbar="sd")
    plt.title("Memorability by Brand Origin")
    plt.ylabel("Mean Score")
    plt.tight_layout()
    plt.savefig(f"{img_dir}/memorability_by_origin.png")
    plt.close()

    # Histograms for each attribute
    for attr in attributes:
        plt.figure(figsize=(6, 4))
        sns.histplot(data=df_long, x=attr, hue="origin", kde=True, bins=5)
        plt.title(f"{attr.title()} Distribution by Brand Origin")
        plt.xlabel("Rating")
        plt.ylabel("Frequency")
        plt.tight_layout()
        plt.savefig(f"{img_dir}/{attr}_distribution.png")
        plt.close()

    # Correlation heatmap
    corr = df_long[attributes].corr(method='spearman').round(2)
    plt.figure(figsize=(5, 4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Spearman Correlation Matrix")
    plt.tight_layout()
    plt.savefig(f"{img_dir}/spearman_corr_matrix.png")
    plt.close()

    # Grouped barplot for all attributes
    group_means = df_long.groupby("origin")[attributes].mean().T
    group_means.reset_index(inplace=True)
    group_means = pd.melt(group_means, id_vars='index', var_name='Origin', value_name='Mean Score')
    group_means.rename(columns={'index': 'Attribute'}, inplace=True)
    plt.figure(figsize=(8, 5))
    sns.barplot(data=group_means, x='Attribute', y='Mean Score', hue='Origin', palette='muted')
    plt.ylabel("Mean Score")
    plt.ylim(0, 5)
    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"{img_dir}/mean_attribute_ratings.png")
    plt.close()
    