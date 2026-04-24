import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# ================= PAGE =================
st.set_page_config(page_title="Induction Motor Drive", layout="centered")

st.title("⚡ Induction Motor Drive (V/f Control Simulator)")

st.markdown("""
### 🔹 Realistic VFD-Based Control

✔ Frequency is controlled  
✔ Voltage automatically adjusted (constant V/f)  
✔ Slip is NOT input → it varies with load  
""")

# ================= SIDEBAR =================
st.sidebar.header("🔧 Motor Parameters")

P = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)

# Base values
V_base = st.sidebar.number_input("Base Voltage (V)", value=230.0)
f_base = st.sidebar.number_input("Base Frequency (Hz)", value=50.0)

# Control variable
f = st.sidebar.slider("Operating Frequency (Hz)", 1.0, 100.0, 50.0)

# Load torque (NEW)
Tl = st.sidebar.slider("Load Torque (Nm)", 1.0, 50.0, 10.0)

# ================= V/f CONTROL =================
if f <= f_base:
    V = (V_base / f_base) * f
else:
    V = V_base  # field weakening region

vf_ratio = V / f

# ================= SLIP CALCULATION =================
# simple proportional model
k = 0.02  # tuning factor

slip = k * (Tl * f) / (V**2 + 1e-6)
slip = min(max(slip, 0.001), 0.1)  # limit realistic range

# ================= MOTOR SPEED =================
Ns = 120 * f / P
Nr = Ns * (1 - slip)

# torque display (equal to load torque in steady state)
T = Tl

# ================= DISPLAY =================
st.subheader("📊 Motor Performance")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Synchronous Speed (RPM)", f"{Ns:.1f}")

with col2:
    st.metric("Rotor Speed (RPM)", f"{Nr:.1f}")

with col3:
    st.metric("Slip (auto)", f"{slip:.4f}")

st.metric("Load Torque (Nm)", f"{Tl:.2f}")
st.metric("Adjusted Voltage (V)", f"{V:.2f}")
st.metric("V/f Ratio", f"{vf_ratio:.2f}")

# ================= SPEED GRAPH =================
st.subheader("📈 Speed vs Frequency")

f_range = np.linspace(1, 100, 100)
speed_curve = (120 * f_range / P) * (1 - slip)

fig1 = plt.figure()
plt.plot(f_range, speed_curve)
plt.axvline(f_base, linestyle="--", label="Base Frequency")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Speed (RPM)")
plt.legend()
plt.grid()

st.pyplot(fig1)

# ================= V/f GRAPH =================
st.subheader("📉 V/f Control Characteristic")

f_range2 = np.linspace(1, 100, 100)
V_curve = []

for freq in f_range2:
    if freq <= f_base:
        V_curve.append((V_base / f_base) * freq)
    else:
        V_curve.append(V_base)

fig2 = plt.figure()
plt.plot(f_range2, V_curve)
plt.axvline(f_base, linestyle="--", label="Base Frequency")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Voltage (V)")
plt.legend()
plt.grid()

st.pyplot(fig2)

# ================= CIRCUIT DIAGRAM =================
def induction_motor_drive_circuit():
    d = schemdraw.Drawing()

    d += elm.SourceSin().label("3ϕ AC")
    d += elm.Line().right()

    d += elm.Box(w=2, h=1).label("Rectifier")
    d += elm.Line().right()

    d.push()
    d += elm.Capacitor().down().label("DC Link")
    d += elm.Ground()
    d.pop()

    d += elm.Line().right()

    d += elm.Box(w=2, h=1).label("Inverter")
    d += elm.Line().right()

    d += elm.Circle().label("IM")

    return d

st.markdown("---")
st.subheader("⚙️ Induction Motor Drive Circuit")

st.pyplot(induction_motor_drive_circuit().draw().fig)

# ================= INTERPRETATION =================
st.markdown("---")
st.subheader("📘 Observations")

st.write("""
✔ Load ↑ → Slip ↑ → Speed ↓  
✔ Frequency ↑ → Speed ↑  
✔ Constant V/f → constant flux  

✔ Below base frequency → constant torque region  
✔ Above base frequency → field weakening region  
""")

# ================= INSIGHT =================
st.info("""
💡 Key Concept:

Slip is NOT controlled manually.

Motor automatically adjusts slip to match load torque.
""")

st.success("Simulation Complete ✅")
