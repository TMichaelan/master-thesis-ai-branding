import pandas as pd

def load_and_prepare_data(filepath):
    rating_map = {
        "Very bad": 1, "Bad": 2, "Neutral": 3, "Good": 4, "Very good": 5
    }
    ai_brands = ["Ecotiva", "Visioniq", "Fidelicon", "Seraphic", "Etiera", "Verdura"]
    human_brands = ["Grove Collaborative", "Plaid", "Northvolt", "Klevu", "Norse Projects", "Seedlip"]

    df = pd.read_csv(filepath)
    for col in df.columns:
        if "How would you rate the name" in col:
            df[col] = df[col].replace(rating_map)
            df[col] = pd.to_numeric(df[col], errors='coerce')

    records = []
    for brand in ai_brands + human_brands:
        try:
            mem_col = next(col for col in df.columns if "memorable" in col and brand in col)
            vis_col = next(col for col in df.columns if "attractive" in col and brand in col)
            clr_col = next(col for col in df.columns if "rate the name" in col and brand in col)
            sub = pd.DataFrame({
                "brand": brand,
                "memorability": df[mem_col],
                "attractiveness": df[vis_col],
                "clarity": df[clr_col],
                "origin": "AI" if brand in ai_brands else "Human"
            })
            records.append(sub)
        except StopIteration:
            print(f"Skipped brand {brand}")
    df_long = pd.concat(records, ignore_index=True)
    return df_long
