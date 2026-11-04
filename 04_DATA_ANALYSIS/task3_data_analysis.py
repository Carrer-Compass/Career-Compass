
import pandas as pd
import re
from pathlib import Path

# -----------------------------------------
# TASK 3: DATA ANALYSIS
# -----------------------------------------

# Locate project and cleaned datasets
PROJECT_DIR = Path(__file__).resolve().parent.parent

possible_paths = [
    PROJECT_DIR / "OUTPUTS",
    PROJECT_DIR.parent / "DAV_PROJECT" / "OUTPUTS"
]

DATA_DIR = next(
    (path for path in possible_paths if path.exists()),
    None
)

if DATA_DIR is None:
    raise FileNotFoundError("Cleaned dataset folder not found!")

OUTPUT_DIR = PROJECT_DIR / "04_DATA_ANALYSIS" / "analysis_outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load datasets
students = pd.read_csv(DATA_DIR / "cleaned_student_placement.csv")
jobs = pd.read_csv(DATA_DIR / "cleaned_it_job_roles.csv")

print("\n========== DATASET INFORMATION ==========")
print("Student dataset:", students.shape)
print("Job roles dataset:", jobs.shape)

# -----------------------------------------
# 1. STUDENT PLACEMENT ANALYSIS
# -----------------------------------------

print("\n========== STUDENT PLACEMENT ANALYSIS ==========")

total_students = len(students)
placed_students = students["placed"].sum()

placement_rate = (
    placed_students / total_students * 100
    if total_students > 0 else 0
)

print("Total students:", total_students)
print("Placed students:", placed_students)
print("Placement rate:", round(placement_rate, 2), "%")

# Placement status distribution
placement_distribution = (
    students["placed"]
    .value_counts()
    .reset_index()
)
placement_distribution.columns = ["Placement_Status", "Students"]

# CGPA analysis
cgpa_analysis = students.groupby("placed")["cgpa"].agg(
    ["count", "mean", "min", "max"]
).reset_index()

# Internship analysis
internship_analysis = students.groupby("internships")["placed"].agg(
    ["count", "mean"]
).reset_index()

internship_analysis["placement_percentage"] = (
    internship_analysis["mean"] * 100
)

# Certification analysis
certification_analysis = students.groupby("certifications")["placed"].agg(
    ["count", "mean"]
).reset_index()

certification_analysis["placement_percentage"] = (
    certification_analysis["mean"] * 100
)

# Coding score analysis
coding_analysis = students.groupby("coding_skills")["placed"].agg(
    ["count", "mean"]
).reset_index()

coding_analysis["placement_percentage"] = (
    coding_analysis["mean"] * 100
)

# Communication score analysis
communication_analysis = students.groupby(
    "communication_skills"
)["placed"].agg(["count", "mean"]).reset_index()

communication_analysis["placement_percentage"] = (
    communication_analysis["mean"] * 100
)

# Aptitude score analysis
aptitude_analysis = students.groupby("placed")["aptitude_score"].mean(
).reset_index()

# Project analysis
project_analysis = students.groupby("projects")["placed"].agg(
    ["count", "mean"]
).reset_index()

project_analysis["placement_percentage"] = (
    project_analysis["mean"] * 100
)

# Company type analysis
company_analysis = (
    students[students["placed"] == 1]
    .groupby("company_type")
    .size()
    .reset_index(name="students")
)

# Package analysis (placed students only)
package_analysis = students[
    (students["placed"] == 1) &
    (students["package_lpa"].notna())
]

average_package = (
    package_analysis["package_lpa"].mean()
    if not package_analysis.empty else 0
)

print("Average package:", round(average_package, 2), "LPA")

# -----------------------------------------
# 2. INDUSTRY JOB ROLE ANALYSIS
# -----------------------------------------

print("\n========== INDUSTRY JOB ROLE ANALYSIS ==========")

job_title_analysis = (
    jobs["job title"]
    .value_counts()
    .reset_index()
)

job_title_analysis.columns = ["Job_Title", "Count"]

# Extract skills from job descriptions
def extract_terms(series):
    terms = []

    for value in series.dropna():
        parts = re.split(r"[,;|\n]+", str(value))

        for part in parts:
            term = part.strip().lower()

            if term and term not in ["not available", "unknown"]:
                terms.append(term)

    return pd.Series(terms).value_counts().reset_index()

skill_demand = extract_terms(jobs["skills"])
skill_demand.columns = ["Skill", "Demand_Count"]

certification_demand = extract_terms(jobs["certification"])
certification_demand.columns = ["Certification", "Demand_Count"]

# -----------------------------------------
# 3. CORRELATION ANALYSIS
# -----------------------------------------

numeric_columns = [
    "age", "cgpa", "backlogs", "internships",
    "certifications", "coding_skills",
    "communication_skills", "aptitude_score",
    "projects", "placed", "package_lpa"
]

correlation_data = students[numeric_columns].corr()

# -----------------------------------------
# 4. EXPORT ANALYSIS RESULTS
# -----------------------------------------

results = {
    "placement_distribution": placement_distribution,
    "cgpa_analysis": cgpa_analysis,
    "internship_analysis": internship_analysis,
    "certification_analysis": certification_analysis,
    "coding_analysis": coding_analysis,
    "communication_analysis": communication_analysis,
    "aptitude_analysis": aptitude_analysis,
    "project_analysis": project_analysis,
    "company_analysis": company_analysis,
    "job_title_analysis": job_title_analysis,
    "skill_demand": skill_demand,
    "certification_demand": certification_demand,
    "correlation_analysis": correlation_data.reset_index()
}

for name, dataframe in results.items():
    dataframe.to_csv(
        OUTPUT_DIR / f"{name}.csv",
        index=False
    )

# Summary report
with open(OUTPUT_DIR / "analysis_summary.txt", "w") as file:
    file.write("STUDENT PLACEMENT AND INDUSTRY SKILL ANALYSIS\n")
    file.write("=" * 50 + "\n")
    file.write(f"Total Students: {total_students}\n")
    file.write(f"Placed Students: {placed_students}\n")
    file.write(f"Placement Rate: {placement_rate:.2f}%\n")
    file.write(f"Average Package: {average_package:.2f} LPA\n")
    file.write(f"Total Job Role Records: {len(jobs)}\n\n")

    file.write("TOP 10 INDUSTRY SKILLS\n")
    file.write(skill_demand.head(10).to_string(index=False))

    file.write("\n\nTOP 10 JOB TITLES\n")
    file.write(job_title_analysis.head(10).to_string(index=False))

print("\n========== ANALYSIS COMPLETED ==========")
print("All analysis files saved in:")
print(OUTPUT_DIR)

print("\nTop 10 demanded industry skills:")
print(skill_demand.head(10).to_string(index=False))

print("\nTop 10 job titles:")
print(job_title_analysis.head(10).to_string(index=False))
