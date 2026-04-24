import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm

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
def induction_motor_drive_circuit():
    d = schemdraw.Drawing()

    # ================= 3-PHASE SOURCE =================
    d += elm.SourceSin().label("3ϕ AC Supply\n(Vs)")
    d += elm.Line().right(1)

    # ================= RECTIFIER =================
    d += elm.Resistor().label("Rectifier\n(AC → DC)")
    d += elm.Line().right(1)

    # ================= DC LINK =================
    # Top bus
    d += elm.Dot()
    
    # Capacitor branch
    d.push()
    d += elm.Capacitor().down(1.5).label("DC Link Capacitor", loc='right')
    d += elm.Ground()
    d.pop()

    # Label DC bus
    d += elm.Label().label("DC Bus").at((d.here[0], d.here[1] + 0.8))

    d += elm.Line().right(1)

    # ================= INVERTER =================
    d += elm.Resistor().label("Inverter\n(DC → AC)")
    d += elm.Line().right(1)

    # ================= MOTOR =================
    # Draw circle manually (version-safe)
    d += elm.Dot()
    
    d.push()
    d += elm.Line().up(0.6)
    d += elm.Line().right(0.6)
    d += elm.Line().down(1.2)
    d += elm.Line().left(1.2)
    d += elm.Line().up(1.2)
    d += elm.Line().right(0.6)
    d.pop()

    # Motor label
    d += elm.Label().label("IM").at((d.here[0]+0.3, d.here[1]))
    d += elm.Label().label("3ϕ Induction Motor").at((d.here[0]-1, d.here[1]+1))

    # Shaft
    d += elm.Line().right(0.8)
    d += elm.Arrow().right(0.5)

    # ================= RETURN PATH =================
    d += elm.Line().down(1.5)
    d += elm.Line().left(10)
    d += elm.Line().up(1.5)

    # ================= TITLE =================
    d += elm.Label().at((4, -2)).label("VFD-Fed Induction Motor Drive (Textbook Model)")

    return d



d = induction_motor_drive_circuit()

fig, ax = plt.subplots()
d.draw(ax=ax)

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
