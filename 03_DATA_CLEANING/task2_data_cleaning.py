import pandas as pd
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "datasets"
OUTPUT_DIR = BASE_DIR / "outputs"

OUTPUT_DIR.mkdir(exist_ok=True)

# Input files
student_file = DATA_DIR / "student_placement_raw.xlsx"
job_file = DATA_DIR / "it_job_roles_raw.xlsx"


def clean_text(value):
    """Remove unnecessary spaces from text."""
    if isinstance(value, str):
        return " ".join(value.strip().split())
    return value


# ==========================================
# 1. STUDENT PLACEMENT DATA CLEANING
# ==========================================

print("\nCleaning Student Placement Dataset...")

students = pd.read_excel(
    student_file,
    sheet_name="Sheet1"
)

# Remove empty and unnamed columns
students = students.loc[
    :, ~students.columns.astype(str).str.startswith("Unnamed")
]

# Standardize column names
students.columns = (
    students.columns.astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Clean text columns
for col in students.select_dtypes(include="object").columns:
    students[col] = students[col].apply(clean_text)

# Convert numeric columns
numeric_columns = [
    "student_id", "age", "cgpa", "backlogs",
    "internships", "certifications",
    "coding_skills", "communication_skills",
    "aptitude_test", "projects", "placed",
    "package_lpa"
]

for col in numeric_columns:
    if col in students.columns:
        students[col] = pd.to_numeric(
            students[col], errors="coerce"
        )

# Remove duplicate records
students = students.drop_duplicates()

# Remove records without student ID
students = students.dropna(subset=["student_id"])

# Fill missing numerical values with median
for col in numeric_columns:
    if col in students.columns:
        students[col] = students[col].fillna(
            students[col].median()
        )

# Fill missing categorical values
for col in students.select_dtypes(include="object").columns:
    students[col] = students[col].fillna("Unknown")

# Save cleaned dataset
students.to_csv(
    OUTPUT_DIR / "cleaned_student_placement.csv",
    index=False
)

students.to_excel(
    OUTPUT_DIR / "cleaned_student_placement.xlsx",
    index=False
)

print("Student dataset cleaned successfully!")
print("Final shape:", students.shape)


# ==========================================
# 2. IT JOB ROLES DATA CLEANING
# ==========================================

print("\nCleaning IT Job Roles Dataset...")

jobs = pd.read_excel(
    job_file,
    sheet_name="Sheet1"
)

# Remove unnamed columns
jobs = jobs.loc[
    :, ~jobs.columns.astype(str).str.startswith("Unnamed")
]

# Standardize column names
jobs.columns = (
    jobs.columns.astype(str)
    .str.strip()
    .str.lower()
)

# Remove duplicate Skills.1 column if identical
if "skills.1" in jobs.columns and "skills" in jobs.columns:
    first = jobs["skills"].fillna("").astype(str).str.strip()
    second = jobs["skills.1"].fillna("").astype(str).str.strip()

    if first.equals(second):
        jobs = jobs.drop(columns=["skills.1"])

# Clean text values
for col in jobs.select_dtypes(include="object").columns:
    jobs[col] = jobs[col].apply(clean_text)

# Remove records without job titles
jobs = jobs.dropna(subset=["job title"])

# Remove exact duplicate records
jobs = jobs.drop_duplicates()

# Fill missing descriptions, skills and certifications
for col in jobs.select_dtypes(include="object").columns:
    jobs[col] = jobs[col].fillna("Not Available")

# Save cleaned dataset
jobs.to_csv(
    OUTPUT_DIR / "cleaned_it_job_roles.csv",
    index=False
)

jobs.to_excel(
    OUTPUT_DIR / "cleaned_it_job_roles.xlsx",
    index=False
)

print("IT Job Roles dataset cleaned successfully!")
print("Final shape:", jobs.shape)


# ==========================================
# 3. FINAL DATA QUALITY REPORT
# ==========================================

print("\n========== DATA CLEANING REPORT ==========")

for name, df in [
    ("Student Placement", students),
    ("IT Job Roles", jobs)
]:
    print(f"\n{name} Dataset")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))
    print("Missing values:")
    print(df.isnull().sum())
    print("Duplicate rows:", df.duplicated().sum())

print("\nBoth datasets cleaned successfully!")
print("Cleaned files saved in the outputs folder.")