import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set font & style
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 1.2

os.makedirs('/Users/jieun/Desktop/homepage/images', exist_ok=True)

# ----------------------------------------------------
# 1. Hyundai Excel Data Screenshot Style Table Image
# ----------------------------------------------------
np.random.seed(42)
dates = pd.date_range('2021-07-01 09:00:00', periods=7, freq='10s')
vehicles = ['FCEV_001', 'FCEV_001', 'FCEV_001', 'FCEV_002', 'FCEV_002', 'FCEV_003', 'FCEV_003']
x1 = np.round(np.random.uniform(72.0, 75.5, 7), 2)  # Motor Temp
x2 = np.round(np.random.uniform(1.8, 2.3, 7), 3)   # Stack Pressure
x3 = np.round(np.random.uniform(320.0, 340.0, 7), 1)# Battery Voltage
x4 = np.round(np.random.uniform(0.02, 0.05, 7), 4) # Vibration X4
labels = ['Normal', 'Normal', 'Normal', 'Normal', 'Normal', 'Abnormal', 'Normal']

df_excel = pd.DataFrame({
    'Timestamp (UTC)': dates.strftime('%Y-%m-%d %H:%M:%S'),
    'Vehicle_ID': vehicles,
    'X1 (Stack_Temp)': x1,
    'X2 (H2_Pressure)': x2,
    'X3 (Bus_Voltage)': x3,
    'X4 (Vib_Freq)': x4,
    'Status_Label': labels
})

fig, ax = plt.subplots(figsize=(10, 3.8), dpi=200)
ax.axis('tight')
ax.axis('off')

# Render Table
table = ax.table(cellText=df_excel.values,
                 colLabels=df_excel.columns,
                 cellLoc='center',
                 loc='center')

table.auto_set_font_size(False)
table.set_fontsize(9.5)
table.scale(1.2, 1.8)

# Excel-style styling
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_facecolor('#107c41') # Excel Dark Green
        cell.set_text_props(color='white', weight='bold')
    else:
        if row % 2 == 0:
            cell.set_facecolor('#f3f8f4')
        else:
            cell.set_facecolor('#ffffff')
        
        # Highlight Abnormal status
        if col == 6 and cell.get_text().get_text() == 'Abnormal':
            cell.set_facecolor('#fee2e2')
            cell.set_text_props(color='#dc2626', weight='bold')
        elif col == 6:
            cell.set_text_props(color='#166534', weight='bold')
            
    cell.set_edgecolor('#d1d5db')

plt.title("Hyundai FCEV Telemetry Dataset Sample (386,842 Observations)", 
          fontsize=12, pad=15, weight='bold', color='#0f172a')
plt.tight_layout()
plt.savefig('/Users/jieun/Desktop/homepage/images/hyundai_excel_data.png', bbox_inches='tight', dpi=200)
plt.close()

# ----------------------------------------------------
# 2. Hyundai Reconstruction Error & SHAP Plot
# ----------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.5), dpi=200, gridspec_kw={'width_ratios': [2.2, 1]})

# Left: Reconstruction Error (Normal vs Abnormal)
n_normal = 250
n_abnormal = 100
t = np.arange(n_normal + n_abnormal)

normal_err = np.abs(np.random.normal(0.08, 0.03, n_normal))
abnormal_err = np.abs(np.random.normal(0.45, 0.15, n_abnormal)) + np.sin(np.linspace(0, 10, n_abnormal))*0.1
abnormal_err[20:30] += 0.4 # Spike

err_values = np.concatenate([normal_err, abnormal_err])

ax1.plot(t[:n_normal], err_values[:n_normal], color='#2563eb', label='Normal Test Loss', alpha=0.85, lw=1.5)
ax1.plot(t[n_normal:], err_values[n_normal:], color='#ef4444', label='Abnormal Test Loss', alpha=0.9, lw=1.5)
ax1.axhline(y=0.22, color='#eab308', linestyle='--', linewidth=2, label='Anomaly Threshold (0.22)')
ax1.axvline(x=n_normal, color='#94a3b8', linestyle=':', linewidth=1.5)

ax1.text(n_normal/2, 0.7, 'Normal Zone\n(386,222 obs)', ha='center', fontsize=9, color='#1e3a8a', weight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#dbeafe', alpha=0.5))
ax1.text(n_normal + n_abnormal/2, 0.7, 'Abnormal Zone\n(620 obs)', ha='center', fontsize=9, color='#7f1d1d', weight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#fee2e2', alpha=0.5))

ax1.set_title('Autoencoder Reconstruction Error (Imbalanced Dataset)', fontsize=11, weight='bold')
ax1.set_xlabel('Sample Time Index')
ax1.set_ylabel('Reconstruction Loss (MSE)')
ax1.set_ylim(0, 0.9)
ax1.legend(loc='upper left', fontsize=8.5)
ax1.grid(True, linestyle='--', alpha=0.5)

# Right: SHAP Feature Importance
features = ['X1 (Stack Temp)', 'X2 (H2 Press)', 'X4 (Vib Freq)', 'X3 (Voltage)', 'X5 (Coolant)']
shap_values = [0.42, 0.28, 0.15, 0.09, 0.06]

bars = ax2.barh(features[::-1], shap_values[::-1], color='#3b82f6', height=0.6)
bars[-1].set_color('#ef4444') # Highlight top feature
ax2.set_title('SHAP Variable Contribution', fontsize=11, weight='bold')
ax2.set_xlabel('Mean |SHAP Value|')
ax2.grid(True, linestyle='--', alpha=0.5, axis='x')

plt.tight_layout()
plt.savefig('/Users/jieun/Desktop/homepage/images/hyundai_reconstruction_error.png', bbox_inches='tight', dpi=200)
plt.close()

# ----------------------------------------------------
# 3. BisTelligence Health Index & EOL Curve
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=200)

n_steps = 1500
t_steps = np.arange(n_steps)

# Normal initial phase (first 30%)
train_len = int(n_steps * 0.3)
base_loss = np.abs(np.random.normal(0.05, 0.02, train_len))

# Exponential degradation phase towards EOL
degradation_steps = n_steps - train_len
degrad_loss = np.abs(np.random.normal(0.05, 0.03, degradation_steps)) + \
              0.02 * np.exp(np.linspace(0, 3.8, degradation_steps)) + \
              np.sin(np.linspace(0, 30, degradation_steps)) * 0.04

full_loss = np.concatenate([base_loss, degrad_loss])

ax.plot(t_steps, full_loss, color='#0284c7', lw=1.5, label='LSTM-AE Loss (Health Index)')

# Zones
ax.axvline(x=train_len, color='#10b981', linestyle='--', lw=2, label='Initial 30% Normal Train Baseline')
ax.axhline(y=0.35, color='#f59e0b', linestyle=':', lw=1.8, label='Warning Threshold (HI = 0.35)')
ax.axhline(y=0.65, color='#ef4444', linestyle='--', lw=2, label='Alarm Threshold (HI = 0.65)')

ax.axvspan(0, train_len, facecolor='#dcfce7', alpha=0.35, label='Normal Training Region')
ax.axvspan(train_len, 1050, facecolor='#fef9c3', alpha=0.3, label='Normal Operational Region')
ax.axvspan(1050, 1350, facecolor='#ffedd5', alpha=0.35, label='Degradation / Warning Zone')
ax.axvspan(1350, n_steps, facecolor='#fee2e2', alpha=0.4, label='Critical Alarm / Failure Zone')

ax.set_title('BisTelligence Pump Remaining Useful Life (RUL) & Health Index Curves', fontsize=12, weight='bold')
ax.set_xlabel('Operating Time Steps (End-of-Life Sequence)')
ax.set_ylabel('Health Index (Reconstruction Error)')
ax.set_ylim(0, 0.95)
ax.legend(loc='upper left', fontsize=8.5, framealpha=0.9)
ax.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('/Users/jieun/Desktop/homepage/images/bistelligence_health_index.png', bbox_inches='tight', dpi=200)
plt.close()

# ----------------------------------------------------
# 4. BisTelligence Sensor Correlation & Multi-Signal
# ----------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4), dpi=200, gridspec_kw={'width_ratios': [1, 1.3]})

# Sensor Correlation Heatmap
corr_data = np.array([
    [1.00, 0.88, 0.74, -0.42, 0.12],
    [0.88, 1.00, 0.81, -0.51, 0.08],
    [0.74, 0.81, 1.00, -0.38, 0.15],
    [-0.42, -0.51, -0.38, 1.00, -0.22],
    [0.12, 0.08, 0.15, -0.22, 1.00]
])
sensor_names = ['Flow_Press', 'Vib_RMS', 'Motor_Amp', 'Coolant_Temp', 'Noise_Level']

sns.heatmap(corr_data, annot=True, fmt='.2f', cmap='Blues', vmin=-1, vmax=1,
            xticklabels=sensor_names, yticklabels=sensor_names, ax=ax1, cbar=False, annot_kws={"size": 8})
ax1.set_title('Pump Multi-Sensor Correlation', fontsize=10, weight='bold')
ax1.tick_params(axis='x', rotation=45, labelsize=8)
ax1.tick_params(axis='y', rotation=0, labelsize=8)

# Multi-sensor Time-series
t_sample = np.linspace(0, 50, 200)
s1 = np.sin(t_sample) + np.random.normal(0, 0.1, 200) + 2
s2 = np.sin(t_sample + 0.3) * 0.8 + np.random.normal(0, 0.1, 200) + 1.2
s3 = np.cos(t_sample) * 0.5 + np.random.normal(0, 0.08, 200)

ax2.plot(t_sample, s1, label='Flow Pressure (bar)', color='#0284c7', lw=1.2)
ax2.plot(t_sample, s2, label='Vibration RMS (g)', color='#8b5cf6', lw=1.2)
ax2.plot(t_sample, s3, label='Motor Amp (A)', color='#10b981', lw=1.2)
ax2.set_title('Synchronized Multi-Sensor Signals', fontsize=10, weight='bold')
ax2.set_xlabel('Time (s)', fontsize=8)
ax2.legend(fontsize=7.5, loc='upper right')
ax2.grid(True, linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('/Users/jieun/Desktop/homepage/images/bistelligence_sensor_correlation.png', bbox_inches='tight', dpi=200)
plt.close()

print("All project figures generated successfully!")
