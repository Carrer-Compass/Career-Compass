
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
ANALYSIS_DIR = BASE_DIR / "04_DATA_ANALYSIS" / "analysis_outputs"
OUTPUT_DIR = Path(__file__).resolve().parent / "visualization_outputs"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")


def save_chart(filename):
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / filename, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"Saved: {filename}")


# 1. Placement Status Distribution
df = pd.read_csv(ANALYSIS_DIR / "placement_distribution.csv")

plt.figure(figsize=(7, 5))
plt.pie(
    df["Students"],
    labels=["Not Placed", "Placed"],
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Student Placement Status Distribution")
save_chart("01_placement_distribution.png")


# 2. Average CGPA vs Placement Status
df = pd.read_csv(ANALYSIS_DIR / "cgpa_analysis.csv")

plt.figure(figsize=(7, 5))
sns.barplot(
    data=df,
    x="placed",
    y="mean"
)
plt.xticks([0, 1], ["Not Placed", "Placed"])
plt.xlabel("Placement Status")
plt.ylabel("Average CGPA")
plt.title("Average CGPA vs Placement Status")
save_chart("02_cgpa_vs_placement.png")


# 3. Internship Experience vs Placement Percentage
df = pd.read_csv(ANALYSIS_DIR / "internship_analysis.csv")

plt.figure(figsize=(8, 5))
sns.barplot(
    data=df,
    x="internships",
    y="placement_percentage"
)
plt.xlabel("Number of Internships")
plt.ylabel("Placement Percentage")
plt.title("Internship Experience vs Placement Percentage")
save_chart("03_internship_analysis.png")


# 4. Coding Skill Score vs Placement Percentage
df = pd.read_csv(ANALYSIS_DIR / "coding_analysis.csv")

plt.figure(figsize=(8, 5))
sns.barplot(
    data=df,
    x="coding_skills",
    y="placement_percentage"
)
plt.xlabel("Coding Skill Score")
plt.ylabel("Placement Percentage")
plt.title("Coding Skill Score vs Placement Percentage")
save_chart("04_coding_analysis.png")


# 5. Top 10 Industry-Demanded Skills
df = pd.read_csv(ANALYSIS_DIR / "skill_demand.csv")
df = df.sort_values("Demand_Count", ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=df,
    x="Demand_Count",
    y="Skill"
)
plt.xlabel("Demand Count")
plt.ylabel("Industry Skills")
plt.title("Top 10 Industry-Demanded Skills")
save_chart("05_top_industry_skills.png")


# 6. Top 10 Industry-Demanded Certifications
df = pd.read_csv(ANALYSIS_DIR / "certification_demand.csv")
df = df.sort_values("Demand_Count", ascending=False).head(10)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=df,
    x="Demand_Count",
    y="Certification"
)
plt.xlabel("Demand Count")
plt.ylabel("Certifications")
plt.title("Top 10 Industry-Demanded Certifications")
save_chart("06_top_certifications.png")


# 7. Correlation Heatmap
df = pd.read_csv(ANALYSIS_DIR / "correlation_analysis.csv")
df = df.set_index("index")

plt.figure(figsize=(12, 9))
sns.heatmap(
    df,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)
plt.title("Student Placement Dataset - Correlation Heatmap")
save_chart("07_correlation_heatmap.png")


print("\nAll visualizations generated successfully!")
print("Output folder:", OUTPUT_DIR)
