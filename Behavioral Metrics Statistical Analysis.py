import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.utils import resample

# 1. Create the Dataset (Matches your provided mock data)
data = {
    'ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'A_Stress': [2, 2, 2, 3, 3, 4, 2, 4, 3, 3],
    'B_Stress': [4, 5, 3, 5, 4, 2, 3, 5, 4, 4], # Results in Mean Delta ~ +1.1
    'A_Bore':   [3, 4, 2, 2, 5, 3, 1, 4, 2, 3],
    'B_Bore':   [2, 3, 1, 2, 4, 4, 2, 3, 1, 4]  # Results in Mean Delta ~ -0.2
}
df = pd.DataFrame(data)

# 2. Calculate Differences (Delta)
df['Delta_Stress'] = df['B_Stress'] - df['A_Stress']
df['Delta_Bore']   = df['B_Bore'] - df['A_Bore']

# 3. Bootstrap 95% Confidence Intervals
np.random.seed(42) # Fixed seed for reproducibility
n_boot = 10000

def get_bootstrap_ci(data):
    means = [resample(data).mean() for _ in range(n_boot)]
    lower = np.percentile(means, 2.5)
    upper = np.percentile(means, 97.5)
    mean = np.mean(data)
    return mean, lower, upper

mean_s, low_s, high_s = get_bootstrap_ci(df['Delta_Stress'])
mean_b, low_b, high_b = get_bootstrap_ci(df['Delta_Bore'])

# 4. Prepare Data for Plotting
labels = ['Δ Stress\n(Timer - No Timer)', 'Δ Boredom\n(Timer - No Timer)']
means = [mean_s, mean_b]
# Error bars must be relative to the mean for matplotlib
errors = [
    [mean_s - low_s, mean_b - low_b], # Lower errors
    [high_s - mean_s, high_b - mean_b]  # Upper errors
]

# 5. Generate the Forest Plot
fig, ax = plt.subplots(figsize=(8, 6))

# Plot Error Bars
# The ecolor argument can sometimes misinterpret a list of colors
# when plotting multiple points, leading to a ValueError.
# To ensure each error bar gets its intended color, plot them individually.
error_colors = ['#D95319', '#0072BD']
for i in range(len(means)):
    ax.errorbar(x=[i], y=[means[i]],
                yerr=[[errors[0][i]], [errors[1][i]]], # yerr needs to be a list of lists for a single point
                fmt='o', markersize=12, capsize=10, linewidth=3,
                color='black', ecolor=error_colors[i])

# Add Reference Line at 0 (No Effect)
ax.axhline(0, color='gray', linestyle='--', linewidth=1.5, alpha=0.7)
ax.text(1.1, 0.05, 'Zero Line (No Difference)', color='gray', fontsize=10, style='italic')

# Aesthetics
ax.set_xticks([0, 1])
ax.set_xticklabels(labels, fontsize=12, fontweight='bold')
ax.set_ylabel('Mean Change (Score 1-5)', fontsize=12)
ax.set_title('95% Confidence Intervals: Stress vs. Boredom', fontsize=14, fontweight='bold')
ax.set_ylim(-1.5, 2.0)

# Add Annotation for Interpretation
ax.annotate('Significant\n(CI does not touch 0)', xy=(0.05, low_s), xytext=(0.2, low_s - 0.5),
            arrowprops=dict(facecolor='black', shrink=0.05))

ax.annotate('Not Significant\n(CI crosses 0)', xy=(0.95, high_b), xytext=(0.5, high_b + 0.8),
            arrowprops=dict(facecolor='black', shrink=0.05))

# Show Values on Plot (Mean and Confidence Interval)
for i, mean in enumerate(means):
    # Calculate the actual lower and upper bounds from mean and errors
    low_ci = mean - errors[0][i]
    high_ci = mean + errors[1][i]
    ax.text(i + 0.1, mean,
            f"Mean: {mean:+.2f}\nCI: [{low_ci:+.2f}, {high_ci:+.2f}]",
            fontsize=10, fontweight='bold', color='black',
            verticalalignment='center')

plt.tight_layout()
plt.show()