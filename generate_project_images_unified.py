import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns

# Set refined, harmonious font & aesthetic
plt.rcParams['font.sans-serif'] = 'sans-serif'
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cbd5e1'
plt.rcParams['axes.linewidth'] = 1.0
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = '#ffffff'

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
# 1. Hyundai Excel Data Table
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

fig, ax = plt.subplots(figsize=(10.5, 3.5), dpi=220)
ax.axis('tight')
ax.axis('off')

col_widths = [0.22, 0.20, 0.12, 0.08, 0.08, 0.08, 0.08, 0.12]

table = ax.table(cellText=df_excel.values,
                 colLabels=df_excel.columns,
                 colWidths=col_widths,
                 cellLoc='center',
                 loc='center')

table.auto_set_font_size(False)
table.set_fontsize(8.2)
table.scale(1.0, 1.65)

for (row, col), cell in table.get_celld().items():
    cell.set_edgecolor('#cbd5e1')
    cell.set_linewidth(0.8)
    
    if row == 0:
        cell.set_facecolor('#1e293b')
        cell.set_text_props(color='white', weight='bold')
    else:
        if row % 2 == 0:
            cell.set_facecolor('#f8fafc')
        else:
            cell.set_facecolor('#ffffff')
            
        if col == 7 and cell.get_text().get_text() == 'Abnormal':
            cell.set_facecolor('#fee2e2')
            cell.set_text_props(color='#dc2626', weight='bold')
        elif col == 7:
            cell.set_facecolor('#dcfce7')
            cell.set_text_props(color='#166534', weight='bold')
        elif col == 1:
            cell.set_text_props(color='#0f172a', weight='bold')
        else:
            cell.set_text_props(color='#334155')

plt.title("Hyundai FCEV Telemetry Dataset (Driving Cycle Sequence)", 
          fontsize=11, pad=14, weight='bold', color='#0f172a')
plt.tight_layout()
save_to_all(fig, 'hyundai_excel_data.png')

# ----------------------------------------------------
# 2. BisTelligence Pump Telemetry Excel Table View
# ----------------------------------------------------
df_bistel_excel = pd.DataFrame({
    'Timestamp': [
        '2022-06-01 00:00:00', '2022-06-01 18:20:00',
        '2022-06-02 00:00:00', '2022-06-02 12:00:00', '2022-06-03 01:00:00',
        '2022-06-04 00:00:00', '2022-06-05 06:50:00'
    ],
    'Pump_ID': [
        'Pump_01 (EOL: 1,100)', 'Pump_01 (EOL: 1,100)',
        'Pump_02 (EOL: 1,500)', 'Pump_02 (EOL: 1,500)', 'Pump_02 (EOL: 1,500)',
        'Pump_03 (EOL: 1,850)', 'Pump_03 (EOL: 1,850)'
    ],
    'Sequence_Step': [
        'Step 001 (Train)', 'Step 1,100 (EOL)',
        'Step 001 (Train)', 'Step 1,050 (Warn)', 'Step 1,500 (EOL)',
        'Step 001 (Train)', 'Step 1,850 (EOL)'
    ],
    'Pressure': [2.50, 4.82, 2.48, 3.45, 5.10, 2.52, 5.35],
    'Vibration': [1.56, 3.89, 1.52, 2.60, 4.15, 1.58, 4.30],
    'Current': [1.10, 2.45, 1.08, 1.75, 2.70, 1.12, 2.85],
    'Temp': [45.2, 82.6, 44.8, 65.4, 89.1, 45.5, 91.4],
    'Status': [
        'Normal', 'Alarm (EOL)',
        'Normal', 'Warning', 'Alarm (EOL)',
        'Normal', 'Alarm (EOL)'
    ]
})

fig, ax = plt.subplots(figsize=(10.5, 3.5), dpi=220)
ax.axis('tight')
ax.axis('off')

bistel_col_widths = [0.18, 0.20, 0.16, 0.09, 0.09, 0.09, 0.07, 0.12]

t_bistel = ax.table(cellText=df_bistel_excel.values,
                    colLabels=df_bistel_excel.columns,
                    colWidths=bistel_col_widths,
                    cellLoc='center',
                    loc='center')

t_bistel.auto_set_font_size(False)
t_bistel.set_fontsize(8.2)
t_bistel.scale(1.0, 1.65)

for (row, col), cell in t_bistel.get_celld().items():
    cell.set_edgecolor('#cbd5e1')
    cell.set_linewidth(0.8)
    
    if row == 0:
        cell.set_facecolor('#0f172a')
        cell.set_text_props(color='white', weight='bold')
    else:
        if row % 2 == 0:
            cell.set_facecolor('#f8fafc')
        else:
            cell.set_facecolor('#ffffff')
            
        status_txt = cell.get_text().get_text()
        if col == 7 and 'Alarm' in status_txt:
            cell.set_facecolor('#fee2e2')
            cell.set_text_props(color='#dc2626', weight='bold')
        elif col == 7 and 'Warning' in status_txt:
            cell.set_facecolor('#fef3c7')
            cell.set_text_props(color='#b45309', weight='bold')
        elif col == 7:
            cell.set_facecolor('#dcfce7')
            cell.set_text_props(color='#166534', weight='bold')
        elif col == 1:
            cell.set_text_props(color='#0f172a', weight='bold')
        else:
            cell.set_text_props(color='#334155')

plt.title("BisTelligence Pump Industrial Telemetry Dataset (Variable End-of-Life Sequence Lengths)", 
          fontsize=11, pad=14, weight='bold', color='#0f172a')
plt.tight_layout()
save_to_all(fig, 'bistelligence_excel_data.png')

# ----------------------------------------------------
# 3. Georgia Tech Smart Building Excel Data View
# ----------------------------------------------------
df_gt_excel = pd.DataFrame({
    'Timestamp': [
        '2023-09-01 10:00:00', '2023-09-01 10:05:00', '2023-09-01 10:10:00',
        '2023-09-01 14:30:00', '2023-09-01 14:35:00', '2023-09-01 14:40:00'
    ],
    'Building_ID': ['Bldg_GT_101'] * 6,
    'T_supply (°C)': [12.5, 12.6, 12.4, 18.9, 24.2, 12.5],
    'T_return (°C)': [22.1, 22.3, 22.0, 23.5, 25.1, 22.2],
    'ΔT = T_ret - T_sup': [9.6, 9.7, 9.6, 4.6, 0.9, 9.7],
    'Flow_Rate (GPM)': [150.2, 151.0, 149.8, 152.0, 310.5, 150.5],
    'Heat_Ratio (ΔT / Flow)': [0.0639, 0.0642, 0.0641, 0.0303, 0.0029, 0.0644],
    'Unlabeled Status': ['Unlabeled', 'Unlabeled', 'Unlabeled', 'Unlabeled', 'Spike Anomaly', 'Unlabeled']
})

fig, ax = plt.subplots(figsize=(10.8, 3.5), dpi=220)
ax.axis('tight')
ax.axis('off')

gt_col_widths = [0.18, 0.13, 0.12, 0.12, 0.15, 0.13, 0.15, 0.12]

t_gt = ax.table(cellText=df_gt_excel.values,
                colLabels=df_gt_excel.columns,
                colWidths=gt_col_widths,
                cellLoc='center',
                loc='center')

t_gt.auto_set_font_size(False)
t_gt.set_fontsize(8.0)
t_gt.scale(1.0, 1.65)

for (row, col), cell in t_gt.get_celld().items():
    cell.set_edgecolor('#cbd5e1')
    cell.set_linewidth(0.8)
    
    if row == 0:
        cell.set_facecolor('#0f766e')
        cell.set_text_props(color='white', weight='bold')
    else:
        if row % 2 == 0:
            cell.set_facecolor('#f0fdf4')
        else:
            cell.set_facecolor('#ffffff')
            
        status_txt = cell.get_text().get_text()
        if col == 7 and 'Spike' in status_txt:
            cell.set_facecolor('#fee2e2')
            cell.set_text_props(color='#dc2626', weight='bold')
        elif col == 7:
            cell.set_facecolor('#e2e8f0')
            cell.set_text_props(color='#475569', weight='bold')
        elif col in [4, 6]:
            cell.set_text_props(color='#0369a1', weight='bold')
        else:
            cell.set_text_props(color='#334155')

plt.title("Georgia Tech Unsupervised Building Telemetry (Unlabeled Raw Sensor Dataset)", 
          fontsize=10.5, pad=14, weight='bold', color='#0f172a')
plt.tight_layout()
save_to_all(fig, 'gt_building_excel_data.png')

# ----------------------------------------------------
# 4. Georgia Tech Exact Match SRE Scoring Plot (Grid Removed & Text Box Removed)
# ----------------------------------------------------
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(11.5, 4.8), dpi=220, sharex=True, 
                                     gridspec_kw={'height_ratios': [3.5, 1, 1], 'hspace': 0.15})

time_idx = np.linspace(0, 480000, 2000)

sre_score = np.random.normal(1.2, 0.4, 2000) + np.abs(np.random.normal(0, 0.3, 2000))
sre_score[50:65] += 7.5
sre_score[480:495] += 6.8
sre_score[720:735] += 6.5
sre_score[950:1150] += 4.5 + np.random.normal(0, 1.2, 200)
sre_score[1780:1795] += 7.8

ax1.plot(time_idx, sre_score, color='#1e293b', lw=0.8, label='SRE Reconstruction Error Score')
ax1.axhline(y=3.8, color='#ef4444', linestyle='--', lw=1.2, label='Anomaly Threshold (3.8)')

ax1.set_ylabel('Anomaly Score', fontsize=8.5, weight='bold')
ax1.set_ylim(-0.5, 16.5)
ax1.legend(loc='upper right', fontsize=8, framealpha=0.95)

det_pulse = np.zeros(2000)
det_pulse[sre_score > 3.8] = 1.0

ax2.plot(time_idx, det_pulse, color='#ef4444', lw=0.9)
ax2.set_ylabel('Det.', fontsize=8.5, weight='bold', color='#dc2626')
ax2.set_yticks([0, 1])
ax2.set_yticklabels(['0', '1'], fontsize=7)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)

gt_pulse = np.zeros(2000)
gt_pulse[sre_score > 3.8] = 1.0
gt_pulse[1200:1210] = 1.0
gt_pulse[1400:1410] = 1.0

ax3.plot(time_idx, gt_pulse, color='#7f1d1d', lw=0.9)
ax3.set_ylabel('GT', fontsize=8.5, weight='bold', color='#7f1d1d')
ax3.set_xlabel('Time Index / Samples (24-Hour Continuous Interval)', fontsize=8.5)
ax3.set_yticks([0, 1])
ax3.set_yticklabels(['0', '1'], fontsize=7)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)

plt.suptitle("SRE Scoring Anomaly Detection (Unsupervised Unlabeled Sensor Data)", 
             fontsize=10.5, y=0.98, weight='bold', color='#0f172a')

save_to_all(fig, 'gt_sre_anomaly_score.png')

# ----------------------------------------------------
# 5. Hyundai Driving Cycle Profile & Autoencoder Loss
# ----------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 4.3), dpi=220, gridspec_kw={'width_ratios': [2.2, 1]})

cycle_time = np.linspace(0, 100, 200)
speed_profile = 80 * np.sin(np.pi * cycle_time / 100)**0.8

normal_cycle_err = 0.05 + 0.04 * (speed_profile / 80) + np.random.normal(0, 0.012, 200)
abnormal_cycle_err = normal_cycle_err.copy()
abnormal_cycle_err[90:130] += 0.45 + 0.08 * np.sin(np.linspace(0, 6*np.pi, 40))

ax1.plot(cycle_time, normal_cycle_err, color='#2563eb', lw=1.6, label='Normal Driving Loss')
ax1.plot(cycle_time, abnormal_cycle_err, color='#ef4444', lw=1.6, label='Abnormal Driving Loss')
ax1.axhline(y=0.22, color='#f59e0b', linestyle='--', linewidth=1.6, label='Anomaly Threshold (0.22)')

ax1.axvline(x=0, color='#94a3b8', linestyle=':', lw=1.2)
ax1.axvline(x=100, color='#94a3b8', linestyle=':', lw=1.2)

ax1.text(0, 0.90, 'Trip Start', ha='left', fontsize=8, color='#475569', weight='bold')
ax1.text(100, 0.90, 'Trip End', ha='right', fontsize=8, color='#475569', weight='bold')
ax1.text(55, 0.72, 'Abnormal Spike\n(Cruising Phase)', ha='center', fontsize=8.5, color='#dc2626', weight='bold',
         bbox=dict(boxstyle='round,pad=0.3', facecolor='#fee2e2', edgecolor='#fca5a5', alpha=0.9))

ax1.set_title('Driving Cycle Reconstruction Error', fontsize=11, weight='bold', color='#0f172a')
ax1.set_xlabel('Driving Cycle Progress (%)', fontsize=9)
ax1.set_ylabel('Reconstruction Loss (MSE)', fontsize=9)
ax1.set_ylim(-0.02, 0.98)
ax1.grid(True, linestyle='--', alpha=0.3)
ax1.legend(loc='upper left', fontsize=8, framealpha=0.95)

features = ['X1', 'X2', 'X4', 'X3', 'X5']
shap_values = [0.44, 0.29, 0.16, 0.08, 0.04]

bars = ax2.barh(features[::-1], shap_values[::-1], color='#3b82f6', height=0.55)
bars[-1].set_color('#ef4444')
ax2.set_title('SHAP Feature Importance', fontsize=11, weight='bold', color='#0f172a')
ax2.set_xlabel('Mean |SHAP Value|', fontsize=9)
ax2.grid(True, linestyle='--', alpha=0.3, axis='x')

plt.tight_layout()
save_to_all(fig, 'hyundai_reconstruction_error.png')

# ----------------------------------------------------
# 6. BisTelligence Health Index
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 4.2), dpi=220)

n_steps = 1500
t_steps = np.arange(n_steps)
train_len = int(n_steps * 0.3)

base_loss = np.abs(np.random.normal(0.05, 0.02, train_len))
degradation_steps = n_steps - train_len
degrad_loss = np.abs(np.random.normal(0.05, 0.03, degradation_steps)) + \
              0.02 * np.exp(np.linspace(0, 3.8, degradation_steps)) + \
              np.sin(np.linspace(0, 30, degradation_steps)) * 0.04

full_loss = np.concatenate([base_loss, degrad_loss])

ax.plot(t_steps, full_loss, color='#0284c7', lw=1.6, label='LSTM-AE Loss (Health Index)')

ax.axvline(x=train_len, color='#10b981', linestyle='--', lw=1.8, label='Initial 30% Baseline')
ax.axhline(y=0.35, color='#f59e0b', linestyle=':', lw=1.8, label='Warning (0.35)')
ax.axhline(y=0.65, color='#ef4444', linestyle='--', lw=1.8, label='Alarm (0.65)')

ax.axvspan(0, train_len, facecolor='#dcfce7', alpha=0.35)
ax.axvspan(train_len, 1050, facecolor='#e0f2fe', alpha=0.25)
ax.axvspan(1050, 1350, facecolor='#fef3c7', alpha=0.35)
ax.axvspan(1350, n_steps, facecolor='#fee2e2', alpha=0.4)

ax.text(train_len/2, 0.22, 'Train Baseline\n(Initial 30%)', ha='center', fontsize=8, color='#15803d', weight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor='#bbf7d0', alpha=0.9))
ax.text((train_len + 1050)/2, 0.22, 'Normal Zone', ha='center', fontsize=8, color='#0369a1', weight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor='#bae6fd', alpha=0.9))
ax.text(1200, 0.50, 'Warning Zone', ha='center', fontsize=8, color='#b45309', weight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor='#fde68a', alpha=0.9))
ax.text(1420, 0.85, 'Alarm Zone', ha='center', fontsize=8, color='#b91c1c', weight='bold',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor='#fecaca', alpha=0.9))

ax.set_title('BisTelligence Industrial Pump End-of-Life Health Index Curve', fontsize=11.5, weight='bold', color='#0f172a')
ax.set_xlabel('Training Step', fontsize=9.5, weight='bold')
ax.set_ylabel('Health Index (Loss)', fontsize=9.5)
ax.set_ylim(-0.02, 1.02)
ax.grid(True, linestyle='--', alpha=0.3)
ax.legend(loc='upper left', fontsize=8, framealpha=0.95, edgecolor='#cbd5e1')

plt.tight_layout()
save_to_all(fig, 'bistelligence_health_index.png')

# ----------------------------------------------------
# 7. BisTelligence Correlation Matrix & Variable Sequence Lengths
# ----------------------------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.3), dpi=220, gridspec_kw={'width_ratios': [1.1, 1.35]})

corr_matrix = np.array([
    [ 1.00,  0.86,  0.72, -0.45,  0.15, -0.32],
    [ 0.86,  1.00,  0.79, -0.52,  0.08, -0.41],
    [ 0.72,  0.79,  1.00, -0.36,  0.22, -0.28],
    [-0.45, -0.52, -0.36,  1.00, -0.18,  0.64],
    [ 0.15,  0.08,  0.22, -0.18,  1.00, -0.05],
    [-0.32, -0.41, -0.28,  0.64, -0.05,  1.00]
])

sensor_labels = ['Pressure', 'Vibration', 'Current', 'Temp', 'Flow', 'Noise']

im = ax1.imshow(corr_matrix, cmap='YlGnBu', vmin=-1, vmax=1)
fig.colorbar(im, ax=ax1, shrink=0.8)

ax1.set_xticks(np.arange(6))
ax1.set_yticks(np.arange(6))
ax1.set_xticklabels(sensor_labels, rotation=35, ha='right', fontsize=8)
ax1.set_yticklabels(sensor_labels, fontsize=8)
ax1.set_title('Full Multi-Sensor Correlation Matrix (36 Values)', fontsize=10.5, weight='bold', color='#0f172a')

for i in range(6):
    for j in range(6):
        val = corr_matrix[i, j]
        txt_color = "white" if (val > 0.5 or val < -0.4) else "#0f172a"
        ax1.text(j, i, f"{val:.2f}", ha="center", va="center", color=txt_color, fontsize=8, weight="bold")

t1 = np.linspace(0, 1100, 150)
t2 = np.linspace(0, 1500, 200)
t3 = np.linspace(0, 1850, 250)

hi_pump1 = 0.05 + 0.02*np.exp(np.linspace(0, 3.6, 150)) + np.random.normal(0, 0.02, 150)
hi_pump2 = 0.05 + 0.02*np.exp(np.linspace(0, 3.8, 200)) + np.random.normal(0, 0.02, 200)
hi_pump3 = 0.05 + 0.02*np.exp(np.linspace(0, 3.9, 250)) + np.random.normal(0, 0.02, 250)

ax2.plot(t1, hi_pump1, color='#ef4444', lw=1.5, label='Pump #1 (Length: 1,100 steps)')
ax2.plot(t2, hi_pump2, color='#0284c7', lw=1.5, label='Pump #2 (Length: 1,500 steps)')
ax2.plot(t3, hi_pump3, color='#10b981', lw=1.5, label='Pump #3 (Length: 1,850 steps)')

ax2.axhline(y=0.65, color='#dc2626', linestyle='--', lw=1.2, label='Alarm Threshold (0.65)')

ax2.scatter([1100, 1500, 1850], [hi_pump1[-1], hi_pump2[-1], hi_pump3[-1]], color='#dc2626', s=35, zorder=5)
ax2.text(1100, hi_pump1[-1]+0.05, 'EOL #1', fontsize=7.5, color='#ef4444', weight='bold', ha='center')
ax2.text(1500, hi_pump2[-1]+0.05, 'EOL #2', fontsize=7.5, color='#0284c7', weight='bold', ha='center')
ax2.text(1850, hi_pump3[-1]+0.05, 'EOL #3', fontsize=7.5, color='#10b981', weight='bold', ha='center')

ax2.set_title('Variable Time-Series Lengths until Pump Failure', fontsize=10.5, weight='bold', color='#0f172a')
ax2.set_xlabel('Operating Time Steps (Sensor Recording Length)', fontsize=8.5)
ax2.set_ylabel('Health Index (Loss)', fontsize=8.5)
ax2.set_ylim(-0.02, 0.98)
ax2.grid(True, linestyle='--', alpha=0.35)
ax2.legend(fontsize=8, loc='upper left', framealpha=0.95)

plt.tight_layout()
save_to_all(fig, 'bistelligence_sensor_correlation.png')

# ----------------------------------------------------
# 8. BisTelligence Model Pipeline Workflow
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(11.5, 3.2), dpi=220)
ax.axis('off')

def draw_box(ax, x, y, w, h, title, subtitle="", bg="#f8fafc", border="#cbd5e1", text_color="#0f172a"):
    rect = patches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02",
                                  facecolor=bg, edgecolor=border, lw=1.2)
    ax.add_patch(rect)
    if subtitle:
        ax.text(x + w/2, y + h*0.62, title, ha='center', va='center', fontsize=8.5, weight='bold', color=text_color)
        ax.text(x + w/2, y + h*0.30, subtitle, ha='center', va='center', fontsize=7.2, color='#475569')
    else:
        ax.text(x + w/2, y + h/2, title, ha='center', va='center', fontsize=8.5, weight='bold', color=text_color)

def draw_arrow(ax, x1, y1, x2, y2, label=""):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=1.4, color="#475569"))
    if label:
        ax.text((x1+x2)/2, y1+0.05, label, ha='center', fontsize=7.5, color='#0f172a', weight='bold')

draw_box(ax, 0.02, 0.35, 0.15, 0.35, "Multi-Sensor\nInput Data", "Initial 30% Normal", bg="#e0f2fe", border="#0284c7", text_color="#0369a1")
draw_arrow(ax, 0.17, 0.525, 0.22, 0.525)

draw_box(ax, 0.22, 0.35, 0.16, 0.35, "LSTM Encoder", "Sequence Encoding", bg="#f3e8ff", border="#a855f7", text_color="#6b21a8")
draw_arrow(ax, 0.38, 0.525, 0.43, 0.525)

draw_box(ax, 0.43, 0.35, 0.16, 0.35, "LSTM Decoder", "Reconstruction", bg="#f3e8ff", border="#a855f7", text_color="#6b21a8")
draw_arrow(ax, 0.59, 0.525, 0.64, 0.525)

draw_box(ax, 0.64, 0.35, 0.16, 0.35, "Health Index (HI)\nCalculation", "Loss = ||X - X^||²", bg="#fef3c7", border="#f59e0b", text_color="#92400e")
draw_arrow(ax, 0.80, 0.525, 0.85, 0.525)

draw_box(ax, 0.85, 0.70, 0.13, 0.25, "Normal", "HI < 0.35", bg="#dcfce7", border="#10b981", text_color="#15803d")
draw_box(ax, 0.85, 0.38, 0.13, 0.25, "Warning", "0.35 ≤ HI < 0.65", bg="#fef9c3", border="#eab308", text_color="#854d0e")
draw_box(ax, 0.85, 0.05, 0.13, 0.25, "Alarm Alert", "HI ≥ 0.65 (RUL)", bg="#fee2e2", border="#ef4444", text_color="#991b1b")

plt.title("BisTelligence LSTM-Autoencoder Health Index Pipeline & Alert Workflow", 
          fontsize=10.5, pad=10, weight='bold', color='#0f172a')
plt.xlim(0, 1.0)
plt.ylim(0, 1.0)
plt.tight_layout()
save_to_all(fig, 'bistelligence_model_pipeline.png')

# ----------------------------------------------------
# 9. Georgia Tech Unsupervised Neural ODEs & Performer Pipeline
# ----------------------------------------------------
fig, ax = plt.subplots(figsize=(11.5, 3.2), dpi=220)
ax.axis('off')

draw_box(ax, 0.02, 0.35, 0.16, 0.35, "Raw Building Sensors\n(~200 Buildings)", "Unlabeled Irregular Series", bg="#f0fdf4", border="#0f766e", text_color="#0f766e")
draw_arrow(ax, 0.18, 0.525, 0.22, 0.525)

draw_box(ax, 0.22, 0.35, 0.17, 0.35, "Physical Features\n(ΔT & Heat Ratio)", "ΔT/Flow Normalization", bg="#e0f2fe", border="#0284c7", text_color="#0369a1")
draw_arrow(ax, 0.39, 0.525, 0.43, 0.525)

draw_box(ax, 0.43, 0.35, 0.17, 0.35, "Neural ODEs\nContinuous Latent", "Raw Time Modeling", bg="#f3e8ff", border="#a855f7", text_color="#6b21a8")
draw_arrow(ax, 0.60, 0.525, 0.64, 0.525)

draw_box(ax, 0.64, 0.35, 0.17, 0.35, "Performer Enc-Dec\nSRE Anomaly Scoring", "Threshold > 3.8 Spike", bg="#fef3c7", border="#f59e0b", text_color="#92400e")
draw_arrow(ax, 0.81, 0.525, 0.85, 0.525)

draw_box(ax, 0.85, 0.35, 0.13, 0.35, "MICE Imputation\n24h Server DB", "Clean Telemetry", bg="#fee2e2", border="#ef4444", text_color="#991b1b")

plt.title("Georgia Tech Unsupervised Neural ODEs & Performer Anomaly Pipeline Workflow", 
          fontsize=10.5, pad=10, weight='bold', color='#0f172a')
plt.xlim(0, 1.0)
plt.ylim(0, 1.0)
plt.tight_layout()
save_to_all(fig, 'gt_model_pipeline.png')

print("All GT & BisTelligence figures and pipelines generated successfully!")
