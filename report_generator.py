import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch


# ---------------------------
# CLI ARGUMENT
# ---------------------------

parser = argparse.ArgumentParser(description="Advanced AI Report Generator")
parser.add_argument("--input", default="data/advanced_employee_performance.csv",
                    help="Input CSV file")

args = parser.parse_args()

data_path = args.input

# ---------------------------
# CREATE FOLDERS
# ---------------------------

os.makedirs("charts", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# ---------------------------
# LOAD DATA
# ---------------------------

data = pd.read_csv(data_path)
data["Date"] = pd.to_datetime(data["Date"])

# ---------------------------
# AUTOMATIC ANALYSIS
# ---------------------------

total_records = len(data)
avg_score = data["Performance_Score"].mean()

top_employee = data.loc[data["Performance_Score"].idxmax()]["Employee"]
best_department = data.groupby("Department")["Performance_Score"].mean().idxmax()

total_tasks = data["Tasks_Completed"].sum()

# ---------------------------
# CHART 1
# Tasks by Department
# ---------------------------

dept_tasks = data.groupby("Department")["Tasks_Completed"].sum()

plt.figure()
dept_tasks.plot(kind="bar")
plt.title("Tasks Completed by Department")
plt.xlabel("Department")
plt.ylabel("Tasks")

chart1 = "charts/tasks_department.png"
plt.tight_layout()
plt.savefig(chart1)
plt.close()

# ---------------------------
# CHART 2
# Score Distribution
# ---------------------------

plt.figure()
data["Performance_Score"].plot(kind="hist", bins=10)
plt.title("Performance Score Distribution")

chart2 = "charts/score_distribution.png"
plt.tight_layout()
plt.savefig(chart2)
plt.close()

# ---------------------------
# CHART 3
# Avg Score by Department
# ---------------------------

avg_dept = data.groupby("Department")["Performance_Score"].mean()

plt.figure()
avg_dept.plot(kind="bar")
plt.title("Average Score by Department")

chart3 = "charts/avg_score_department.png"
plt.tight_layout()
plt.savefig(chart3)
plt.close()

# ---------------------------
# CHART 4
# Daily Productivity
# ---------------------------

daily = data.groupby("Date")["Tasks_Completed"].sum()

plt.figure()
daily.plot()
plt.title("Daily Productivity Trend")

chart4 = "charts/daily_productivity.png"
plt.tight_layout()
plt.savefig(chart4)
plt.close()

# ---------------------------
# AUTO INSIGHTS
# ---------------------------

insights = f"""
Total Records: {total_records}

Total Tasks Completed: {total_tasks}

Average Performance Score: {avg_score:.2f}

Top Performing Employee: {top_employee}

Best Performing Department: {best_department}
"""

# ---------------------------
# TABLE DATA
# ---------------------------

table_data = [["Employee", "Department", "Tasks", "Score"]]

for _, row in data.iterrows():
    table_data.append([
        row["Employee"],
        row["Department"],
        row["Tasks_Completed"],
        row["Performance_Score"]
    ])

# ---------------------------
# PDF REPORT
# ---------------------------

styles = getSampleStyleSheet()

elements = []

elements.append(Paragraph("AI Performance Analytics Dashboard", styles["Title"]))
elements.append(Spacer(1, 20))

elements.append(Paragraph("Automated Insights", styles["Heading2"]))
elements.append(Paragraph(insights.replace("\n", "<br/>"), styles["BodyText"]))

elements.append(Spacer(1, 20))

elements.append(Paragraph("Employee Performance Data", styles["Heading2"]))
elements.append(Spacer(1, 10))

table = Table(table_data[:15])  # show first rows
elements.append(table)

elements.append(Spacer(1, 30))

elements.append(Paragraph("Visual Analytics", styles["Heading2"]))
elements.append(Spacer(1, 20))

elements.append(Image(chart1, width=5*inch, height=3*inch))
elements.append(Spacer(1, 15))

elements.append(Image(chart2, width=5*inch, height=3*inch))
elements.append(Spacer(1, 15))

elements.append(Image(chart3, width=5*inch, height=3*inch))
elements.append(Spacer(1, 15))

elements.append(Image(chart4, width=5*inch, height=3*inch))

report_file = "reports/performance_dashboard.pdf"

pdf = SimpleDocTemplate(report_file, pagesize=letter)
pdf.build(elements)

print("✅ Advanced AI Report Generated Successfully!")
print("📄 Report saved at:", report_file)