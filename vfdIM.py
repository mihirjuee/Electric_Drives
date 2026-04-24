import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import schemdraw
import schemdraw.elements as elm
from schemdraw import flow


# ================= PAGE =================
st.set_page_config(page_title="Induction Motor Drive", page_icon="logo.png", layout="centered")

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
def draw_full_vfd():
    # 1. Setup figure
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # 2. Setup Drawing with axes canvas for Streamlit compatibility
    d = schemdraw.Drawing(canvas=ax)
    d.config(unit=1.5)
    
    # === Main Power Bus (Top and Bottom) ===
    # Use Ic elements for the legs, which are excellent for 3-phase circuits
    # The 'Ic' element acts like a leg/phase module.

    # --- RECTIFIER LEG ---
    # Create the Rectifier phase-leg using an Ic element with two diodes
    leg_diode = elm.Ic(pins=[elm.IcPin(name='top', side='T'),
                              elm.IcPin(name='bot', side='B'),
                              elm.IcPin(name='ac', side='L')],
                        w=0.8, h=2, leadlen=0.2)
    # The element needs to be modified internally to contain the diodes.
    # This is a bit advanced, but cleaner. A simpler approach is to loop
    # standard diodes and connecting wires. Let's do that for clarity.

    # --- Simpler, Correct Looping Approach ---
    # Draw the top bus bar
    d += elm.Line().at((0, 3)).to((8, 3)).label('+', loc='top').label('Fixed DC Voltage', loc='top', ofst=0.5)
    d += elm.Line().at((0, 0)).to((8, 0)).label('-', loc='top') # Use a simple line for ground

    # Loop to draw the 3 rectifier phases
    for i in range(3):
        x = i * 1.5 + 0.5
        d.push()
        d += elm.Line().at((x, 3)).down().length(0.1)
        d += elm.Diode().label(f'D{i+1}', loc='bottom').down().reverse()
        d.push()
        d += elm.Line().left().length(1.0).label(f'L{i+1}', loc='left') if i < 3 else elm.Line().left().length(2.0)
        d.pop()
        d += elm.Diode().label(f'D{i+4}', loc='top').down().reverse()
        d += elm.Line().down().length(0.2)
        d.pop()

    # Capacitor
    d += elm.Capacitor().at((5.5, 3)).to((5.5, 0)).label('DC Link')

    # Loop to draw the 3 inverter phases
    # Using Ic module for standard inverter look
    leg_igbt = elm.Ic(pins=[elm.IcPin(name='t', side='T'),
                            elm.IcPin(name='b', side='B'),
                            elm.IcPin(name='ac', side='R')],
                        w=1.2, h=2)

    for i in range(3):
        x = i * 1.5 + 4.5
        d += leg_igbt.at((x, 3)).label(f'Leg {i+1}') # Place it.

    # Final output lines to motor
    d += elm.Line().at((9.0, 1.5)).right().length(1.5).label('U', loc='top')
    d += elm.Line().at((9.0, 1.0)).right().length(1.5).label('V', loc='top')
    d += elm.Line().at((9.0, 0.5)).right().length(1.5).label('W', loc='top')
    
    # Motor
    d += elm.Motor().at((11, 1)).label('Motor')

    # Draw and hide axes
    d.draw()
    ax.axis('off')
    return fig

# --- Streamlit Display ---
st.title("⚡ VFD Circuit Schematic Recreator")
st.markdown("### Power Circuit Diagram")
st.pyplot(draw_full_vfd())
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
