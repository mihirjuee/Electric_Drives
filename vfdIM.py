import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
from schemdraw import flow


# ================= PAGE =================
st.set_page_config(page_title="Induction Motor Drive", layout="centered")

st.title("⚡ Induction Motor Drive (V/f Control Simulator)")

st.markdown("""
### 🔹 Realistic VFD-Based Induction Motor Model

✔ Frequency controlled  
✔ Voltage auto-adjusted (V/f control)  
✔ Slip depends on load  
✔ Torque-speed characteristic included  
""")

# ================= SIDEBAR =================
st.sidebar.header("🔧 Motor Parameters")

P = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)

V_base = st.sidebar.number_input("Rated Voltage (V)", value=230.0, step=10.0)
f_base = st.sidebar.number_input("Base Frequency (Hz)", value=50.0, step=1.0)

f = st.sidebar.slider("Operating Frequency (Hz)", 1.0, 100.0, 50.0, step=1.0)

Tl = st.sidebar.slider("Load Torque (Nm)", 1.0, 50.0, 10.0)

# ================= V/f CONTROL =================
if f <= f_base:
    V = (V_base / f_base) * f
else:
    V = V_base  # field weakening

vf_ratio = V / f

# ================= SPEED =================
Ns = 120 * f / P

# ================= SLIP MODEL =================
s_base = 0.03
T_rated = 20

load_factor = Tl / T_rated

if f <= f_base:
    slip = s_base * load_factor
else:
    slip = s_base * load_factor * (f / f_base)

slip = np.clip(slip, 0.005, 0.2)

Nr = Ns * (1 - slip)

# ================= TORQUE CAPABILITY =================
if f <= f_base:
    T_max = T_rated
else:
    T_max = T_rated * (f_base / f)

# ================= OVERLOAD =================
overload = Tl > T_max

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
st.metric("Operating Voltage (V)", f"{V:.2f}")
st.metric("V/f Ratio", f"{vf_ratio:.2f}")

if overload:
    st.error("⚠️ Overload! Load exceeds motor capability → Risk of stall")

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



def draw_vfd_circuit():
    # Use the Drawing object as a context manager
    with schemdraw.Drawing() as d:
        d.config(unit=1.5)
        
        # 1. AC Input
        d += elm.SourceSin().label("3φ AC")
        
        # 2. Rectifier (Flow Box)
        d += flow.Box(w=1.5, h=1).label("Rectifier")
        
        # 3. DC Link
        d.push()
        d += elm.Capacitor().down().label("DC Link")
        d += elm.Ground()
        d.pop()
        
        # 4. Inverter (Flow Box)
        d += flow.Box(w=1.5, h=1).label("Inverter")
        
        # 5. Induction Motor (Correct Element)
        d += elm.Motor().label("IM")
        
        return d

# Streamlit Display
st.subheader("VFD Power Circuit")

# Render the drawing
# Assign the drawing to a variable and pass it to st.pyplot
fig = draw_vfd_circuit()
st.pyplot(fig)
# ================= INTERPRETATION =================
st.markdown("---")
st.subheader("📘 Observations")

st.write("""
✔ Below base frequency → constant torque region  
✔ Above base frequency → field weakening (torque decreases)  

✔ Load ↑ → Slip ↑ → Speed ↓  
✔ Frequency ↑ → Speed ↑  

✔ Overload → motor may stall  

""")

st.success("Simulation Complete ✅")
