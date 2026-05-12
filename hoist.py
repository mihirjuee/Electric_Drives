import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Four Quadrant Hoist Simulation",
    layout="wide"
)

st.title("⚙️ Four Quadrant Operation of Hoist")

st.markdown("""
### Features
- Common Torque-Speed axis
- Four quadrant hoist operation
- Moving loaded/empty cage
- Moving counterweight
- Rotation direction
- Motor torque direction
- Load torque direction
""")

# =========================================================
# SESSION STATE
# =========================================================

if "run_animation" not in st.session_state:
    st.session_state.run_animation = False

# =========================================================
# BUTTONS
# =========================================================

col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Play Animation"):
        st.session_state.run_animation = True

with col2:
    if st.button("⏹ Stop Animation"):
        st.session_state.run_animation = False

placeholder = st.empty()

# =========================================================
# QUADRANT DATA
# =========================================================

quadrants = [

    # TOP LEFT
    {
        "title": "Quadrant II",
        "mode": "Forward Braking",
        "loaded": False,
        "direction": "down",
        "rotation": "CW",
        "motor_torque": "←",
        "load_torque": "→"
    },

    # TOP RIGHT
    {
        "title": "Quadrant I",
        "mode": "Forward Motoring",
        "loaded": True,
        "direction": "up",
        "rotation": "CW",
        "motor_torque": "→",
        "load_torque": "←"
    },

    # BOTTOM LEFT
    {
        "title": "Quadrant III",
        "mode": "Reverse Motoring",
        "loaded": False,
        "direction": "up",
        "rotation": "CCW",
        "motor_torque": "←",
        "load_torque": "→"
    },

    # BOTTOM RIGHT
    {
        "title": "Quadrant IV",
        "mode": "Reverse Braking",
        "loaded": True,
        "direction": "down",
        "rotation": "CCW",
        "motor_torque": "→",
        "load_torque": "←"
    }
]

# =========================================================
# DRAW HOIST
# =========================================================

def draw_hoist(
    ax,
    title,
    mode,
    loaded,
    direction,
    cage_y,
    rotation,
    motor_torque,
    load_torque
):

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # -----------------------------------------------------
    # BORDER
    # -----------------------------------------------------

    border = patches.Rectangle(
        (0, 0),
        10,
        10,
        fill=False,
        linewidth=2
    )

    ax.add_patch(border)

    # -----------------------------------------------------
    # PULLEY
    # -----------------------------------------------------

    pulley = patches.Circle(
        (5, 8),
        1,
        fill=False,
        linewidth=3
    )

    ax.add_patch(pulley)

    # -----------------------------------------------------
    # ROTATION DIRECTION
    # -----------------------------------------------------

    if rotation == "CW":

        arc = patches.Arc(
            (5, 8),
            1.6,
            1.6,
            theta1=30,
            theta2=300,
            linewidth=2,
            color='green'
        )

        ax.add_patch(arc)

        ax.arrow(
            5.7,
            7.2,
            -0.01,
            0.01,
            head_width=0.15,
            color='green'
        )

    else:

        arc = patches.Arc(
            (5, 8),
            1.6,
            1.6,
            theta1=120,
            theta2=390,
            linewidth=2,
            color='purple'
        )

        ax.add_patch(arc)

        ax.arrow(
            4.3,
            7.2,
            0.01,
            0.01,
            head_width=0.15,
            color='purple'
        )

    # -----------------------------------------------------
    # COUNTERWEIGHT POSITION
    # -----------------------------------------------------

    counter_y = 10 - cage_y

    # -----------------------------------------------------
    # ROPE
    # -----------------------------------------------------

    ax.plot(
        [4, 4],
        [8, counter_y + 1.3],
        linewidth=3,
        color='black'
    )

    ax.plot(
        [6, 6],
        [8, cage_y],
        linewidth=3,
        color='black'
    )

    # -----------------------------------------------------
    # COUNTERWEIGHT
    # -----------------------------------------------------

    counter = patches.Rectangle(
        (3.2, counter_y),
        1.5,
        1.3,
        facecolor='gray'
    )

    ax.add_patch(counter)

    ax.text(
        1.5,
        counter_y + 0.2,
        "Counter\nWeight",
        fontsize=8
    )

    # -----------------------------------------------------
    # CAGE
    # -----------------------------------------------------

    if loaded:
        cage_color = "orange"
        cage_label = "Loaded Cage"
    else:
        cage_color = "lightblue"
        cage_label = "Empty Cage"

    cage = patches.Rectangle(
        (5.2, cage_y - 1),
        1.5,
        1.3,
        facecolor=cage_color
    )

    ax.add_patch(cage)

    ax.text(
        6.9,
        cage_y - 0.2,
        cage_label,
        fontsize=8
    )

    # -----------------------------------------------------
    # MOTION ARROW
    # -----------------------------------------------------

    if direction == "up":

        ax.arrow(
            8,
            cage_y - 0.5,
            0,
            1,
            width=0.08,
            head_width=0.35,
            color='green'
        )

    else:

        ax.arrow(
            8,
            cage_y + 0.5,
            0,
            -1,
            width=0.08,
            head_width=0.35,
            color='red'
        )

    # -----------------------------------------------------
    # TORQUE DIRECTION
    # -----------------------------------------------------

    ax.text(
        0.5,
        2,
        f"Motor Torque: {motor_torque}",
        fontsize=9,
        color='blue'
    )

    ax.text(
        0.5,
        1.3,
        f"Load Torque: {load_torque}",
        fontsize=9,
        color='brown'
    )

    # -----------------------------------------------------
    # TITLES
    # -----------------------------------------------------

    ax.text(
        0.5,
        9.5,
        title,
        fontsize=12,
        weight='bold'
    )

    ax.text(
        0.5,
        8.9,
        mode,
        fontsize=10
    )

    ax.axis('off')

# =========================================================
# DRAW COMMON AXIS
# =========================================================

def draw_common_axis(fig):

    ax = fig.add_axes([0.38, 0.38, 0.24, 0.24])

    ax.axhline(0, color='black', linewidth=2)
    ax.axvline(0, color='black', linewidth=2)

    ax.set_xlim(-1, 1)
    ax.set_ylim(-1, 1)

    ax.text(0.8, 0.05, "+T", fontsize=12)
    ax.text(-0.95, 0.05, "-T", fontsize=12)

    ax.text(0.05, 0.8, "+ω", fontsize=12)
    ax.text(0.05, -0.9, "-ω", fontsize=12)

    ax.text(0.45, 0.45, "Q1")
    ax.text(-0.65, 0.45, "Q2")
    ax.text(-0.65, -0.55, "Q3")
    ax.text(0.45, -0.55, "Q4")

    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_title("Torque-Speed Plane", fontsize=10)

# =========================================================
# STATIC DRAW
# =========================================================

def draw_static():

    fig, axs = plt.subplots(
        2,
        2,
        figsize=(14, 14)
    )

    axs = axs.flatten()

    for i, q in enumerate(quadrants):

        draw_hoist(
            axs[i],
            q["title"],
            q["mode"],
            q["loaded"],
            q["direction"],
            cage_y=4,
            rotation=q["rotation"],
            motor_torque=q["motor_torque"],
            load_torque=q["load_torque"]
        )

    draw_common_axis(fig)

    plt.tight_layout()

    placeholder.pyplot(fig)

    plt.close(fig)

# =========================================================
# ANIMATION
# =========================================================

if st.session_state.run_animation:

    for step in range(100):

        if not st.session_state.run_animation:
            break

        fig, axs = plt.subplots(
            2,
            2,
            figsize=(14, 14)
        )

        axs = axs.flatten()

        for i, q in enumerate(quadrants):

            if q["direction"] == "up":
                cage_y = 2 + (step % 5)
            else:
                cage_y = 6 - (step % 5)

            draw_hoist(
                axs[i],
                q["title"],
                q["mode"],
                q["loaded"],
                q["direction"],
                cage_y,
                rotation=q["rotation"],
                motor_torque=q["motor_torque"],
                load_torque=q["load_torque"]
            )

        draw_common_axis(fig)

        plt.tight_layout()

        placeholder.pyplot(fig)

        plt.close(fig)

        time.sleep(0.4)

else:

    draw_static()
