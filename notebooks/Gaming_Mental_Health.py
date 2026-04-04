import os
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\Users\bhavy\Downloads\Gaming and Mental Health.csv")
def ensure_directories() -> None:
    """Create output directories if they do not already exist."""
    Path("images").mkdir(parents=True, exist_ok=True)
    Path("outputs").mkdir(parents=True, exist_ok=True)


def load_data(file_path: str) -> pd.DataFrame:
    """Load dataset from CSV."""
    df = pd.read_csv(file_path)
    return df


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Clean column names for consistency."""
    df.columns = [col.strip().lower() for col in df.columns]
    return df


def basic_data_check(df: pd.DataFrame) -> None:
    """Print high-level dataset information."""
    print("\n--- SHAPE ---")
    print(df.shape)

    print("\n--- COLUMNS ---")
    print(df.columns.tolist())

    print("\n--- INFO ---")
    print(df.info())

    print("\n--- MISSING VALUES ---")
    print(df.isnull().sum())

    print("\n--- FIRST 5 ROWS ---")
    print(df.head())

    print("\n--- NUMERIC SUMMARY ---")
    print(df.describe(include="number"))

    print("\n--- CATEGORICAL SUMMARY ---")
    print(df.describe(include="object"))


def save_csv_outputs(df: pd.DataFrame) -> None:
    """Generate summary CSV files for GitHub portfolio visibility."""
    risk_dist = (
        df["gaming_addiction_risk_level"]
        .value_counts(dropna=False)
        .rename_axis("gaming_addiction_risk_level")
        .reset_index(name="count")
    )
    risk_dist.to_csv("outputs/risk_distribution.csv", index=False)

    avg_hours = (
        df.groupby("gaming_addiction_risk_level", dropna=False)["daily_gaming_hours"]
        .mean()
        .reset_index(name="avg_daily_gaming_hours")
        .sort_values(by="avg_daily_gaming_hours", ascending=False)
    )
    avg_hours.to_csv("outputs/avg_gaming_hours_by_risk.csv", index=False)

    avg_spending = (
        df.groupby("gaming_addiction_risk_level", dropna=False)["monthly_game_spending_usd"]
        .mean()
        .reset_index(name="avg_monthly_spending_usd")
        .sort_values(by="avg_monthly_spending_usd", ascending=False)
    )
    avg_spending.to_csv("outputs/avg_spending_by_risk.csv", index=False)

    avg_isolation = (
        df.groupby("gaming_addiction_risk_level", dropna=False)["social_isolation_score"]
        .mean()
        .reset_index(name="avg_social_isolation_score")
        .sort_values(by="avg_social_isolation_score", ascending=False)
    )
    avg_isolation.to_csv("outputs/avg_social_isolation_by_risk.csv", index=False)

    if "game_genre" in df.columns:
        genre_risk = (
            df.groupby(["game_genre", "gaming_addiction_risk_level"], dropna=False)
            .size()
            .reset_index(name="count")
            .sort_values(by="count", ascending=False)
        )
        genre_risk.to_csv("outputs/genre_by_risk_counts.csv", index=False)

    print("\nSummary CSV files saved in /outputs")


def plot_risk_distribution(df: pd.DataFrame) -> None:
    risk_counts = (
        df["gaming_addiction_risk_level"]
        .value_counts()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    risk_counts.plot(kind="bar")
    plt.title("Gaming Addiction Risk Distribution")
    plt.xlabel("Risk Level")
    plt.ylabel("Number of Users")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("images/risk_distribution.png")
    plt.close()


def plot_avg_gaming_hours_by_risk(df: pd.DataFrame) -> None:
    avg_hours = (
        df.groupby("gaming_addiction_risk_level")["daily_gaming_hours"]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    avg_hours.plot(kind="bar")
    plt.title("Average Daily Gaming Hours by Risk Level")
    plt.xlabel("Risk Level")
    plt.ylabel("Average Daily Gaming Hours")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("images/gaming_hours_by_risk.png")
    plt.close()


def plot_avg_spending_by_risk(df: pd.DataFrame) -> None:
    avg_spending = (
        df.groupby("gaming_addiction_risk_level")["monthly_game_spending_usd"]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    avg_spending.plot(kind="bar")
    plt.title("Average Monthly Spending by Risk Level")
    plt.xlabel("Risk Level")
    plt.ylabel("Average Monthly Spending (USD)")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("images/spending_by_risk.png")
    plt.close()


def plot_avg_isolation_by_risk(df: pd.DataFrame) -> None:
    avg_isolation = (
        df.groupby("gaming_addiction_risk_level")["social_isolation_score"]
        .mean()
        .sort_values(ascending=False)
    )

    plt.figure(figsize=(8, 5))
    avg_isolation.plot(kind="bar")
    plt.title("Average Social Isolation Score by Risk Level")
    plt.xlabel("Risk Level")
    plt.ylabel("Average Social Isolation Score")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("images/social_isolation_by_risk.png")
    plt.close()


def plot_top_genres(df: pd.DataFrame) -> None:
    if "game_genre" not in df.columns:
        print("\nColumn 'game_genre' not found. Skipping genre chart.")
        return

    top_genres = df["game_genre"].value_counts().head(10)

    plt.figure(figsize=(10, 6))
    top_genres.plot(kind="bar")
    plt.title("Top 10 Game Genres by User Count")
    plt.xlabel("Game Genre")
    plt.ylabel("Number of Users")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("images/top_game_genres.png")
    plt.close()


def generate_key_insights(df: pd.DataFrame) -> None:
    print("\n--- KEY INSIGHTS ---")

    avg_hours = (
        df.groupby("gaming_addiction_risk_level")["daily_gaming_hours"]
        .mean()
        .sort_values(ascending=False)
    )
    print("\nAverage daily gaming hours by risk level:")
    print(avg_hours)

    avg_spending = (
        df.groupby("gaming_addiction_risk_level")["monthly_game_spending_usd"]
        .mean()
        .sort_values(ascending=False)
    )
    print("\nAverage monthly spending by risk level:")
    print(avg_spending)

    avg_isolation = (
        df.groupby("gaming_addiction_risk_level")["social_isolation_score"]
        .mean()
        .sort_values(ascending=False)
    )
    print("\nAverage social isolation score by risk level:")
    print(avg_isolation)

    if "game_genre" in df.columns:
        genre_counts = df["game_genre"].value_counts().head(10)
        print("\nTop game genres:")
        print(genre_counts)


def main() -> None:
    ensure_directories()

    file_path = "data/gaming_mental_health.csv"  # change this if your file name is different

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        print("Put your CSV file inside the data folder and update file_path if needed.")
        return

    df = load_data(file_path)
    df = standardize_columns(df)

    required_columns = [
        "daily_gaming_hours",
        "monthly_game_spending_usd",
        "social_isolation_score",
        "gaming_addiction_risk_level",
    ]

    missing_required = [col for col in required_columns if col not in df.columns]
    if missing_required:
        print(f"Missing required columns: {missing_required}")
        return

    basic_data_check(df)
    save_csv_outputs(df)

    plot_risk_distribution(df)
    plot_avg_gaming_hours_by_risk(df)
    plot_avg_spending_by_risk(df)
    plot_avg_isolation_by_risk(df)
    plot_top_genres(df)

    generate_key_insights(df)

    print("\nAnalysis complete.")
    print("Charts saved in /images")
    print("Summary tables saved in /outputs")


if __name__ == "__main__":
    main()
