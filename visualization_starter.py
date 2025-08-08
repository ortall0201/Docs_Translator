import matplotlib.pyplot as plt
import numpy as np

# Sample data
x = np.linspace(0, 10, 100)
y1 = np.sin(x)
y2 = np.cos(x)

# Create subplots
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))

# 1. Line plot
ax1.plot(x, y1, label='sin(x)', color='blue')
ax1.plot(x, y2, label='cos(x)', color='red')
ax1.set_title('Line Plot: Sin and Cos')
ax1.legend()
ax1.grid(True)

# 2. Bar chart
categories = ['A', 'B', 'C', 'D', 'E']
values = [23, 45, 56, 78, 32]
ax2.bar(categories, values, color=['red', 'green', 'blue', 'orange', 'purple'])
ax2.set_title('Bar Chart')
ax2.set_ylabel('Values')

# 3. Scatter plot
np.random.seed(42)
x_scatter = np.random.randn(50)
y_scatter = np.random.randn(50)
colors = np.random.randn(50)
ax3.scatter(x_scatter, y_scatter, c=colors, alpha=0.6, cmap='viridis')
ax3.set_title('Scatter Plot')
ax3.set_xlabel('X values')
ax3.set_ylabel('Y values')

# 4. Pie chart
sizes = [30, 25, 20, 15, 10]
labels = ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5']
ax4.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
ax4.set_title('Pie Chart')

plt.tight_layout()
plt.show()