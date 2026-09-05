import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import pandas as pd

# Connect to database
conn = sqlite3.connect("mutual_funds.db")

# 1. Category-wise fund count plot
query = "SELECT category, COUNT(*) as count FROM fund_master GROUP BY category;"
df_cat = pd.read_sql(query, conn)

plt.figure(figsize=(6, 4))
sns.barplot(x="category", y="count", data=df_cat, palette="viridis")
plt.title("Number of Funds by Category")
plt.xlabel("Category")
plt.ylabel("Fund Count")
plt.savefig("category_distribution.png")
print("Saved category_distribution.png successfully!")

conn.close()