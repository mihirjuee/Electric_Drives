import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# ================= PAGE =================
st.set_page_config(page_title="DC Motor Control", layout="wide")
st.title("⚡ DC Motor Control using Full Bridge Converter")

st.latex(r"V_{dc} = \frac{2V_m}{\pi} \cos(\alpha)")

# ================= SIDEBAR =================
st.sidebar.header("🔧 Converter Inputs")

Vm = st.sidebar.number_input("AC Peak Voltage (Vm)", value=325.0)
alpha_deg = st.sidebar.slider("Firing Angle α (deg)", 0, 180, 30)

st.sidebar.header("⚙️ Motor Parameters")

Ra = st.sidebar.number_input("Armature Resistance (Ω)", value=2.0)
K = st.sidebar.number_input("Motor Constant (K)", value=0.5)

# ================= CALCULATIONS =================
alpha = np.deg2rad(alpha_deg)

Vdc = (2 * Vm / np.pi) * np.cos(alpha)
Ia = Vdc / Ra if Ra != 0 else 0
omega = Vdc / K if K != 0 else 0

# ================= CIRCUIT DIAGRAM =================
st.subheader("🔌 Full Bridge Converter with DC Motor")

with schemdraw.Drawing() as d:

    # AC source
    d += elm.SourceSin().label("AC")
    d += elm.Line().right()
    d += elm.Dot()
    d.push()
    # Bridge left leg
    d.push()
    d += elm.Diode().up().label("T1")
    d += elm.Line().right()
    d.push()
    d += elm.Diode().down().label("T2").reverse()
    d.pop()
    d += elm.Line().right()
    d += elm.Resistor().down().label("Ra")
    d += elm.SourceV().down().label("Eb").reverse()
    d += elm.Line().down(2)
    d += elm.Line().left()
    d.pop()
    d += elm.Line().down(2)

    # Bridge right leg

    d += elm.Diode().down().label("T4").reverse()
    d += elm.Line().right()
    d += elm.Diode().up().label("T3")
    d.push()
    d += elm.Dot()
    d += elm.Line().left(3.5)
    d += elm.Line().down(1)
    d += elm.Line().left(2.5)
    d.pop()
    d += elm.Line().up()
    fig_circuit = d.draw().fig

st.pyplot(fig_circuit)

# ================= WAVEFORMS =================
theta_deg = np.degrees(t)
alpha_deg = np.degrees(alpha)

fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

# ================= INPUT =================
ax[0].plot(theta_deg, vs)

ax[0].set_title("Input AC Voltage")
ax[0].set_ylabel("Voltage (V)")
ax[0].grid(True)

# Dynamic limits
ymax = np.max(vs)

# Mark firing angles
ax[0].axvline(alpha_deg, linestyle='--', linewidth=1)
ax[0].axvline(180 + alpha_deg, linestyle='--', linewidth=1)

# Labels (position-safe)
ax[0].text(alpha_deg + 2, ymax*0.8, f'α = {alpha_deg:.0f}°')
ax[0].text(180 + alpha_deg + 2, ymax*0.8, 'π + α')

# ================= OUTPUT =================
ax[1].plot(theta_deg, vout)

ax[1].set_title("Converter Output Voltage")
ax[1].set_xlabel("Electrical Angle (°)")
ax[1].set_ylabel("Voltage (V)")
ax[1].grid(True)

# Mark firing angles
ax[1].axvline(alpha_deg, linestyle='--', linewidth=1)
ax[1].axvline(180 + alpha_deg, linestyle='--', linewidth=1)

# Conduction region shading (VERY IMPORTANT)
ax[1].axvspan(alpha_deg, 180, alpha=0.2)
ax[1].axvspan(180 + alpha_deg, 360, alpha=0.2)

# Label positions based on output waveform
yout_max = np.max(vout)

ax[1].text(alpha_deg + 5, yout_max*0.6, 'T1,T2 ON')
ax[1].text(180 + alpha_deg + 5, yout_max*0.6, 'T3,T4 ON')

# Clean degree ticks
ax[1].set_xticks([0, 90, 180, 270, 360])

plt.tight_layout(h_pad=2)
st.pyplot(fig)

# ================= RESULTS =================
st.subheader("📊 Motor Performance")

c1, c2, c3 = st.columns(3)

c1.metric("DC Output Voltage", f"{Vdc:.2f} V")
c2.metric("Armature Current", f"{Ia:.2f} A")
c3.metric("Motor Speed", f"{omega:.2f} rad/s")

# ================= INSIGHT =================
st.info(
    "Increasing firing angle α reduces average output voltage, "
    "which reduces motor speed. At α = 90°, output voltage ≈ 0. "
    "Above 90°, the converter enters inversion mode."
)
