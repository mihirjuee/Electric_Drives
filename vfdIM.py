import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

# ================= PAGE =================
st.set_page_config(page_title="Induction Motor Drive", layout="centered")

st.title("⚡ Induction Motor Drive (V/f Control)")

st.markdown("""
### 🔹 Realistic VFD Operation

✔ Frequency is the control input  
✔ Voltage is automatically adjusted (constant V/f)  
✔ Slip depends on load torque  
""")

# ================= SIDEBAR =================
st.sidebar.header("🔧 Motor Parameters")

P = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)

# Rated values (fixed)
V_base = st.sidebar.number_input(
    "Rated Voltage (V)",
    min_value=50.0,
    max_value=1000.0,
    value=230.0,
    step=10.0
)

f_base = st.sidebar.number_input(
    "Base Frequency (Hz)",
    min_value=10.0,
    max_value=100.0,
    value=50.0,
    step=1.0
)

# Control variable
f = st.sidebar.slider(
    "Operating Frequency (Hz)",
    min_value=1.0,
    max_value=100.0,
    value=50.0,
    step=1.0
)

# Load torque
Tl = st.sidebar.slider("Load Torque (Nm)", 1.0, 50.0, 10.0)

# ================= V/f CONTROL =================
if f <= f_base:
    V = (V_base / f_base) * f
else:
    V = V_base  # field weakening

vf_ratio = V / f

# ================= SPEED =================
Ns = 120 * f / P

# ================= SLIP FROM LOAD =================
T_rated = 20  # tuning parameter

slip = 0.02 + 0.08 * (Tl / T_rated)
slip = min(max(slip, 0.005), 0.1)

Nr = Ns * (1 - slip)

# ================= DISPLAY =================
st.subheader("📊 Motor Performance")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Synchronous Speed (RPM)", f"{Ns:.1f}")

with col2:
    st.metric("Rotor Speed (RPM)", f"{Nr:.1f}")

with col3:
    st.metric("Slip", f"{slip:.4f}")

st.metric("Load Torque (Nm)", f"{Tl:.2f}")
st.metric("Operating Voltage", f"{V:.2f}")
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
✔ Frequency ↑ → Speed ↑  
✔ Load ↑ → Slip ↑ → Speed ↓  

✔ Below base frequency → constant torque region  
✔ Above base frequency → field weakening region  

✔ Voltage is NOT controlled manually → derived from V/f
""")

# ================= INSIGHT =================
st.info("""
💡 Key Concept:

Ns = 120f / P

Slip is not an input — it adjusts automatically with load torque.
""")

st.success("Simulation Complete ✅")
