import pandas as pd


def validtion_of_file(df: pd.DataFrame):
    df['risk_level'] = pd.cut(
        df['range_km'],
        bins=[-float("inf"), 20, 100, 300, float("inf")],
        labels=['low', 'medium', 'high', 'extreme']
    ).astype(str)
    df = df.fillna("Unknown")

    return df.to_dict(orient="records")
