"""Generates data.csv (100 customers, total purchase amount = 2,45,600)."""
import random
from datetime import date, timedelta
import pandas as pd

random.seed(42)

male = ["Ramesh", "Suresh", "Kiran", "Arjun", "Vikram", "Rahul", "Anil", "Sanjay", "Manoj", "Rajesh",
        "Naveen", "Prakash", "Deepak", "Mohan", "Srinivas", "Karthik", "Varun", "Harish", "Ajay", "Ravi"]
female = ["Priya", "Anjali", "Sneha", "Kavya", "Divya", "Lakshmi", "Meena", "Pooja", "Swathi", "Neha",
          "Anitha", "Sunita", "Revathi", "Sravani", "Bhavana", "Deepika", "Radha", "Geetha", "Nisha", "Madhavi"]

# First 5 rows exactly as shown in the project image
rows = [
    ("C001", "Ramesh", 28, "Male", 1500, "2023-01-10"),
    ("C002", "Priya", 32, "Female", 2300, "2023-02-15"),
    ("C003", "Suresh", 45, "Male", 1800, "2023-03-12"),
    ("C004", "Anjali", 26, "Female", 3200, "2023-04-20"),
    ("C005", "Kiran", 38, "Male", 2100, "2023-05-18"),
]

start = date(2023, 1, 1)
for i in range(6, 101):
    gender = random.choice(["Male", "Female"])
    name = random.choice(male if gender == "Male" else female)
    age = random.randint(18, 60)
    amount = random.randrange(500, 4600, 100)
    joined = start + timedelta(days=random.randint(0, 600))
    rows.append((f"C{i:03d}", name, age, gender, amount, joined.isoformat()))

df = pd.DataFrame(rows, columns=["CustomerID", "Name", "Age", "Gender", "Amount", "JoiningDate"])

# Nudge amounts so the grand total is exactly 245,600 (matches the image)
target = 245600
diff = target - int(df["Amount"].sum())
idx = 5
while diff != 0:
    step = max(min(diff, 500), -500)
    new_val = df.at[idx, "Amount"] + step
    if 500 <= new_val <= 5000:
        df.at[idx, "Amount"] = new_val
        diff -= step
    idx = idx + 1 if idx < 99 else 5

df.to_csv("data.csv", index=False)
print(df.head(), "\nRows:", len(df), "| Total:", df["Amount"].sum())
