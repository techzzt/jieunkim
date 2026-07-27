import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set minimalist font & clean aesthetic
plt.rcParams['font.sans-serif'] = 'sans-serif'
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#94a3b8'
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'

dirs = [
    '/Users/jieun/Desktop/Career/Portfolio/images',
    '/Users/jieun/Desktop/homepage/images'
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

def save_to_all(fig, filename):
    for d in dirs:
        path = os.path.join(d, filename)
        fig.savefig(path, bbox_inches='tight', dpi=220, facecolor='white', transparent=False)
    plt.close(fig)

# ----------------------------------------------------
# 1. Hyundai Excel Data Table (Simple Header: Timestamp, Cycle_ID, Vehicle_ID, X1 ~ X4)
# ----------------------------------------------------
np.random.seed(42)

dates_c1 = pd.date_range('2021-07-01 08:30:00', periods=4, freq='1min')
dates_c2 = pd.date_range('2021-07-01 14:15:00', periods=3, freq='1min')

dates_all = list(dates_c1.strftime('%Y-%m-%d %H:%M:%S')) + list(dates_c2.strftime('%Y-%m-%d %H:%M:%S'))
cycles = ['Cycle_01 (Start)', 'Cycle_01', 'Cycle_01', 'Cycle_01 (End)',
          'Cycle_02 (Start)', 'Cycle_02 (Abnormal)', 'Cycle_02']
vehicles = ['FCEV_001'] * 7
x1 = [25.0, 72.4, 75.1, 40.2, 24.8, 88.6, 76.2]
x2 = [1.2, 2.1, 2.3, 1.2, 1.2, 3.4, 2.2]
x3 = [320.5, 335.2, 338.0, 320.1, 320.0, 355.8, 330.4]
x4 = [0.021, 0.034, 0.038, 0.020, 0.022, 0.089, 0.035]
labels = ['Normal', 'Normal', 'Normal', 'Normal', 'Normal', 'Abnormal', 'Normal']

df_excel = pd.DataFrame({
    'Timestamp': dates_all,
    'Driving_Cycle_ID': cycles,
    'Vehicle_ID': vehicles,
    'X1': x1,
    'X2': x2,
    'X3': x3,
    'X4': x4,
    'Status': labels
})

fig, ax = plt.subplots(figsize=(9.8, 3.4), dpi=220)
ax.axis('tight')
ax.axis('off')

table = ax.table(cellText=df_excel.values,
                 colLabels=df_excel.columns,
                 cellLoc='center',
                 loc='center')

table.auto_set_font_size(False)
table.set_fontsize(8.8)
table.scale(1.12, 1.6)

# Minimal border & text styling
for (row, col), cell in table.get_celld().items():
    cell.set_facecolor('white')
    cell.set_edgecolor('#cbd5e1')
    cell.set_linewidth(0.6)
    
    if row == 0:
        cell.set_text_props(color='#0f172a', weight='bold')
    else:
        if col == 7 and cell.get_text().get_text() == 'Abnormal':
            cell.set_text_props(color='#dc2626', weight='bold')
        elif col == 7:
            cell.set_text_props(color='#166534', weight='bold')
        elif col == 1:
            cell.set_text_props(color='#0f172a', weight='bold')
        else:
            cell.set_text_props(color='#334155')

plt.title("Hyundai Telemetry Dataset Sample (Driving Cycle Sequence)", 
          fontsize=10.5, pad=12, weight='bold', color='#0f172a')
plt.tight_layout()
save_to_all(fig, 'hyundai_excel_data.png')

# ----------------------------------------------------
# 2. Hyundai Driving Cycle Profile & Autoencoder Error Plot
# ----------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.2), dpi=220, gridspec_kw={'width_ratios': [2.2, 1]})

cycle_time = np.linspace(0, 100, 200)

speed_profile = 80 * np.sin(np.pi * cycle_time / 100)**0.8
normal_cycle_err = 0.05 + 0.04 * (speed_profile / 80) + np.random.normal(0, 0.015, 200)
abnormal_cycle_err = normal_cycle_err.copy()
abnormal_cycle_err[90:130] += 0.45 + 0.1 * np.sin(np.linspace(0, 6*np.pi, 40))

ax1.plot(cycle_time, normal_cycle_err, color='#0f172a', lw=1.3, label='Normal Driving Cycle Error')
ax1.plot(cycle_time, abnormal_cycle_err, color='#dc2626', lw=1.3, label='Abnormal Driving Cycle Error')
ax1.axhline(y=0.22, color='#d97706', linestyle='--', linewidth=1.4, label='Anomaly Threshold (0.22)')

ax1.axvline(x=0, color='#94a3b8', linestyle=':', lw=1)
ax1.axvline(x=100, color='#94a3b8', linestyle=':', lw=1)
ax1.text(0, -0.07, 'Trip Start', ha='center', fontsize=7.5, color='#475569')
ax1.text(100, -0.07, 'Trip End', ha='center', fontsize=7.5, color='#475569')
ax1.text(50, 0.7, 'Abnormal Anomaly Spike', ha='center', fontsize=8.5, color='#dc2626', weight='bold')

ax1.set_title('Driving Cycle Reconstruction Error Profile', fontsize=10.5, weight='bold', color='#0f172a')
ax1.set_xlabel('Driving Cycle Progress (%)', fontsize=8.5)
ax1.set_ylabel('Reconstruction Loss (MSE)', fontsize=8.5)
ax1.set_ylim(-0.02, 0.85)
ax1.grid(False)
ax1.legend(loc='upper left', fontsize=7.5, frameon=False)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)

# Right: SHAP Value with clean X1, X2, X3, X4, X5
features = ['X1', 'X2', 'X4', 'X3', 'X5']
shap_values = [0.44, 0.29, 0.16, 0.08, 0.04]

bars = ax2.barh(features[::-1], shap_values[::-1], color='#475569', height=0.55)
bars[-1].set_color('#dc2626')
ax2.set_title('SHAP Feature Importance', fontsize=10.5, weight='bold', color='#0f172a')
ax2.set_xlabel('Mean |SHAP Value|', fontsize=8.5)
ax2.grid(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
save_to_all(fig, 'hyundai_reconstruction_error.png')

# ----------------------------------------------------
# 3. BisTelligence Health Index (No Grid)
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(9.5, 3.8), dpi=220)

n_steps = 1500
t_steps = np.arange(n_steps)
train_len = int(n_steps * 0.3)

base_loss = np.abs(np.random.normal(0.05, 0.02, train_len))
degradation_steps = n_steps - train_len
degrad_loss = np.abs(np.random.normal(0.05, 0.03, degradation_steps)) + \
              0.02 * np.exp(np.linspace(0, 3.8, degradation_steps)) + \
              np.sin(np.linspace(0, 30, degradation_steps)) * 0.04

full_loss = np.concatenate([base_loss, degrad_loss])

ax.plot(t_steps, full_loss, color='#0f172a', lw=1.3, label='LSTM-AE Loss (Health Index)')

ax.axvline(x=train_len, color='#16a34a', linestyle='--', lw=1.4, label='Initial 30% Baseline')
ax.axhline(y=0.35, color='#d97706', linestyle=':', lw=1.4, label='Warning (0.35)')
ax.axhline(y=0.65, color='#dc2626', linestyle='--', lw=1.4, label='Alarm (0.65)')

ax.text(train_len/2, 0.85, 'Train (30%)', ha='center', fontsize=8.5, color='#16a34a', weight='bold')
ax.text(train_len + 300, 0.85, 'Normal Zone', ha='center', fontsize=8.5, color='#475569')
ax.text(1200, 0.85, 'Warning', ha='center', fontsize=8.5, color='#d97706', weight='bold')
ax.text(1435, 0.85, 'Alarm', ha='center', fontsize=8.5, color='#dc2626', weight='bold')

ax.set_title('BisTelligence Pump End-of-Life Health Index Curve', fontsize=11, weight='bold', color='#0f172a')
ax.set_xlabel('Operating Time Steps', fontsize=9)
ax.set_ylabel('Health Index', fontsize=9)
ax.set_ylim(0, 0.95)
ax.grid(False)
ax.legend(loc='upper left', fontsize=8, frameon=False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

plt.tight_layout()
save_to_all(fig, 'bistelligence_health_index.png')

# ----------------------------------------------------
# 4. BisTelligence Multi-Sensor Signals (Clean Lines, No Grid)
# ----------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 3.8), dpi=220, gridspec_kw={'width_ratios': [1, 1.3]})

corr_data = np.array([
    [1.00, 0.88, 0.74, -0.42, 0.12],
    [0.88, 1.00, 0.81, -0.51, 0.08],
    [0.74, 0.81, 1.00, -0.38, 0.15],
    [-0.42, -0.51, -0.38, 1.00, -0.22],
    [0.12, 0.08, 0.15, -0.22, 1.00]
])
sensor_names = ['Sensor 1', 'Sensor 2', 'Sensor 3', 'Sensor 4', 'Sensor 5']

sns.heatmap(corr_data, annot=True, fmt='.2f', cmap='Greys', vmin=-1, vmax=1,
            xticklabels=sensor_names, yticklabels=sensor_names, ax=ax1, cbar=False, annot_kws={"size": 7.5})
ax1.set_title('Sensor Correlation', fontsize=10, weight='bold', color='#0f172a')
ax1.tick_params(axis='x', rotation=45, labelsize=7.5)
ax1.tick_params(axis='y', rotation=0, labelsize=7.5)

t_sample = np.linspace(0, 50, 200)
s1 = np.sin(t_sample) + np.random.normal(0, 0.1, 200) + 2
s2 = np.sin(t_sample + 0.3) * 0.8 + np.random.normal(0, 0.1, 200) + 1.2
s3 = np.cos(t_sample) * 0.5 + np.random.normal(0, 0.08, 200)

ax2.plot(t_sample, s1, label='Sensor 1', color='#0f172a', lw=1.1)
ax2.plot(t_sample, s2, label='Sensor 2', color='#475569', lw=1.1, linestyle='--')
ax2.plot(t_sample, s3, label='Sensor 3', color='#94a3b8', lw=1.1, linestyle=':')
ax2.set_title('Multi-Sensor Signals', fontsize=10, weight='bold', color='#0f172a')
ax2.set_xlabel('Time (s)', fontsize=8)
ax2.grid(False)
ax2.legend(fontsize=7.5, loc='upper right', frameon=False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

plt.tight_layout()
save_to_all(fig, 'bistelligence_sensor_correlation.png')

print("All driving cycle & clean headers updated successfully!")
