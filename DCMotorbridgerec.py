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

    # Bridge left leg
    d.push()
    d += elm.Diode().up().label("T1")
    d += elm.Line().right()
    d.push()
    d += elm.Diode().down().label("T2").reverse()
    d.pop()
    d += elm.Resistor().down().label("Ra")
    d += elm.SourceV().up().label("Eb")
    d.pop()
    d += elm.Line().down(2)

    # Bridge right leg
    d.push()
    d += elm.Diode().down().label("T4").reverse()
    d += elm.Line().right()
    d += elm.Diode().up().label("T3")
    d.pop()

    d += elm.Line().right(3)

    # Motor load
    d.push()
    d += elm.Line().right(2)
    
    
    
    
    d.pop()

    fig_circuit = d.draw().fig

st.pyplot(fig_circuit)

# ================= WAVEFORMS =================
st.subheader("📈 Waveforms")

t = np.linspace(0, 2*np.pi, 1000)
vs = Vm * np.sin(t)

vout = np.zeros_like(t)

for i in range(len(t)):
    theta = t[i] % (2*np.pi)

    if alpha <= theta <= np.pi:
        vout[i] = Vm * np.sin(theta)
    elif np.pi + alpha <= theta <= 2*np.pi:
        vout[i] = -Vm * np.sin(theta)
    else:
        vout[i] = 0

fig, ax = plt.subplots(2, 1, figsize=(10, 6), sharex=True)

# Input
ax[0].plot(t, vs)
ax[0].set_title("Input AC Voltage")
ax[0].set_ylabel("Voltage (V)")
ax[0].grid()

# Output
ax[1].plot(t, vout, color='red')
ax[1].set_title("Converter Output Voltage")
ax[1].set_xlabel("Electrical Angle (rad)")
ax[1].set_ylabel("Voltage (V)")
ax[1].grid()

plt.tight_layout()
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
