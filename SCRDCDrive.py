# ============================================================
# STREAMLIT APP
# ARMATURE VOLTAGE CONTROL OF DC MOTOR
# USING THYRISTOR DC DRIVE
# ============================================================

# Run using:
# streamlit run app.py

# ============================================================
# IMPORTS
# ============================================================

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="DC Thyristor Drive Simulator",
    layout="wide"
)

# ============================================================
# TITLE
# ============================================================

st.title("⚡ Armature Voltage Control of DC Motor")
st.subheader("Thyristor DC Drive Interactive Simulator")

st.markdown("---")

# ============================================================
# SIDEBAR CONTROLS
# ============================================================

st.sidebar.header("Drive Parameters")

Vs = st.sidebar.slider(
    "AC Supply Voltage (V)",
    100,
    400,
    230
)

alpha = st.sidebar.slider(
    "Firing Angle α (Degree)",
    0,
    180,
    45
)

Ra = st.sidebar.slider(
    "Armature Resistance Ra (Ω)",
    0.1,
    5.0,
    1.0
)

Kb = st.sidebar.slider(
    "Back EMF Constant Kb",
    0.1,
    2.0,
    1.0
)

load_torque = st.sidebar.slider(
    "Load Torque",
    0.1,
    20.0,
    5.0
)

# ============================================================
# CALCULATIONS
# ============================================================

alpha_rad = np.radians(alpha)

# Average output voltage of fully controlled rectifier
Va = (2 * np.sqrt(2) * Vs / np.pi) * np.cos(alpha_rad)

# Simplified armature current
Ia = max((Va - Kb * load_torque) / Ra, 0)

# Speed approximation
speed = max((Va - Ia * Ra) / Kb, 0)

# Power
power = Va * Ia

# ============================================================
# DISPLAY METRICS
# ============================================================

col1, col2, col3, col4 = st.columns(4)

col1.metric("Armature Voltage Va", f"{Va:.2f} V")
col2.metric("Armature Current Ia", f"{Ia:.2f} A")
col3.metric("Motor Speed", f"{speed:.2f} rpm")
col4.metric("Motor Power", f"{power:.2f} W")

st.markdown("---")

# ============================================================
# WAVEFORM GENERATION
# ============================================================

theta = np.linspace(0, 2*np.pi, 2000)

# AC input
Vin = np.sin(theta)

# Thyristor output waveform
Vout = np.zeros_like(theta)

for i in range(len(theta)):

    angle_deg = np.degrees(theta[i] % (2*np.pi))

    if angle_deg >= alpha and angle_deg <= 180:
        Vout[i] = np.sin(theta[i])

    elif angle_deg >= (180 + alpha) and angle_deg <= 360:
        Vout[i] = np.sin(theta[i])

# ============================================================
# PLOTS
# ============================================================

fig, ax = plt.subplots(figsize=(12,5))

fig.patch.set_facecolor('black')
ax.set_facecolor('black')

# AC Input
ax.plot(theta,
        Vin,
        linewidth=2.5,
        color='cyan',
        label='AC Input Voltage')

# DC Output
ax.plot(theta,
        Vout,
        linewidth=3,
        color='red',
        label='Controlled Output Voltage')

# Firing angle lines
ax.axvline(alpha_rad,
           color='yellow',
           linestyle='--',
           linewidth=2,
           label='Firing Angle α')

ax.axvline(np.pi + alpha_rad,
           color='yellow',
           linestyle='--',
           linewidth=2)

# Labels
ax.set_title(
    "Thyristor Controlled DC Output Waveform",
    fontsize=16,
    color='white',
    fontweight='bold'
)

ax.set_xlabel(
    "Electrical Angle (rad)",
    color='white',
    fontsize=12
)

ax.set_ylabel(
    "Voltage",
    color='white',
    fontsize=12
)

# Grid
ax.grid(True, alpha=0.3)

# Tick colors
ax.tick_params(colors='white')

# Legend
legend = ax.legend(facecolor='black')

for text in legend.get_texts():
    text.set_color("white")

st.pyplot(fig)

# ============================================================
# MOTOR CHARACTERISTICS
# ============================================================

st.markdown("---")
st.subheader("⚙ Motor Speed vs Firing Angle")

angles = np.linspace(0, 180, 180)

speeds = []

for a in angles:

    a_rad = np.radians(a)

    Va_temp = (2 * np.sqrt(2) * Vs / np.pi) * np.cos(a_rad)

    Ia_temp = max((Va_temp - Kb * load_torque) / Ra, 0)

    speed_temp = max((Va_temp - Ia_temp * Ra) / Kb, 0)

    speeds.append(speed_temp)

fig2, ax2 = plt.subplots(figsize=(10,5))

fig2.patch.set_facecolor('black')
ax2.set_facecolor('black')

ax2.plot(
    angles,
    speeds,
    linewidth=3,
    color='lime'
)

# Current operating point
ax2.plot(
    alpha,
    speed,
    'ro',
    markersize=10
)

ax2.set_title(
    "Speed Control using Armature Voltage",
    fontsize=16,
    color='white',
    fontweight='bold'
)

ax2.set_xlabel(
    "Firing Angle α (Degree)",
    color='white'
)

ax2.set_ylabel(
    "Motor Speed",
    color='white'
)

ax2.grid(True, alpha=0.3)

ax2.tick_params(colors='white')

st.pyplot(fig2)

# ============================================================
# MOTOR ROTATION VISUALIZATION
# ============================================================

st.markdown("---")
st.subheader("🔄 Motor Rotation Visualization")

rotation_speed = int(speed / 10)

motor_html = f"""
<div style="
display:flex;
justify-content:center;
align-items:center;
height:250px;
background-color:black;
border-radius:15px;
">

<div style="
width:120px;
height:120px;
border:10px solid cyan;
border-top:10px solid red;
border-radius:50%;
animation:spin {max(0.2, 5/max(rotation_speed,1))}s linear infinite;
">
</div>

</div>

<style>

@keyframes spin {{

from {{
transform: rotate(0deg);
}}

to {{
transform: rotate(360deg);
}}

}}

</style>
"""

st.markdown(motor_html, unsafe_allow_html=True)

# ============================================================
# THEORY SECTION
# ============================================================

st.markdown("---")

st.subheader("📘 Theory")

st.write("""
### Armature Voltage Control Method

In a thyristor DC drive, motor speed is controlled by varying the armature voltage.

The thyristor firing angle controls the average output voltage of the rectifier.

- Smaller firing angle → Higher DC voltage → Higher speed
- Larger firing angle → Lower DC voltage → Lower speed

Average output voltage:

Va = (2√2 Vs / π) cos(α)

where:

- Vs = AC supply voltage
- α = firing angle
""")

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")
st.markdown(
    "<center><h4 style='color:cyan;'>Learn EE Interactive</h4></center>",
    unsafe_allow_html=True
)
