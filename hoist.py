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
- Simultaneous 4-quadrant display
- Moving loaded cage
- Moving empty cage
- Moving counterweight
- Torque-Speed indication
- Up/Down motion arrows
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
#
# Layout:
#
#   Q2 | Q1
#   --------
#   Q3 | Q4
# =========================================================

quadrants = [

    {
        "title": "Quadrant II",
        "mode": "Forward Braking",
        "loaded": False,
        "direction": "down",
        "torque": "-T",
        "speed": "+ω"
    },

    {
        "title": "Quadrant I",
        "mode": "Forward Motoring",
        "loaded": True,
        "direction": "up",
        "torque": "+T",
        "speed": "+ω"
    },

    {
        "title": "Quadrant III",
        "mode": "Reverse Motoring",
        "loaded": False,
        "direction": "up",
        "torque": "-T",
        "speed": "-ω"
    },

    {
        "title": "Quadrant IV",
        "mode": "Reverse Braking",
        "loaded": True,
        "direction": "down",
        "torque": "+T",
        "speed": "-ω"
    }

]

# =========================================================
# DRAW FUNCTION
# =========================================================

def draw_single_hoist(
    ax,
    title,
    mode,
    loaded,
    direction,
    cage_y,
    torque,
    speed
):

    # -----------------------------------------------------
    # AXIS LIMITS
    # -----------------------------------------------------

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
    # TORQUE-SPEED AXES
    # -----------------------------------------------------

    # Torque Axis
    ax.arrow(
        1,
        1,
        2,
        0,
        head_width=0.2,
        head_length=0.2,
        linewidth=2,
        color='black'
    )

    # Speed Axis
    ax.arrow(
        1,
        1,
        0,
        2,
        head_width=0.2,
        head_length=0.2,
        linewidth=2,
        color='black'
    )

    # Axis Labels
    ax.text(3.1, 0.7, "Torque", fontsize=9)
    ax.text(0.4, 3.1, "Speed", fontsize=9)

    # Signs
    ax.text(
        2.2,
        1.4,
        torque,
        fontsize=12,
        weight='bold'
    )

    ax.text(
        1.2,
        2.3,
        speed,
        fontsize=12,
        weight='bold'
    )

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
    # COUNTERWEIGHT POSITION
    # Counterweight moves opposite to cage
    # -----------------------------------------------------

    counter_y = 10 - cage_y

    # -----------------------------------------------------
    # ROPE
    # -----------------------------------------------------

    # Left Rope
    ax.plot(
        [4, 4],
        [8, counter_y + 1.3],
        linewidth=3,
        color='black'
    )

    # Right Rope
    ax.plot(
        [6, 6],
        [8, cage_y],
        linewidth=3,
        color='black'
    )

    # -----------------------------------------------------
    # COUNTERWEIGHT
    # -----------------------------------------------------

    counter_weight = patches.Rectangle(
        (3.2, counter_y),
        1.5,
        1.3,
        facecolor='gray'
    )

    ax.add_patch(counter_weight)

    ax.text(
        1.6,
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
    # DIRECTION ARROW
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

    # Remove axes
    ax.axis('off')


# =========================================================
# STATIC VIEW
# =========================================================

def draw_static():

    fig, axs = plt.subplots(
        2,
        2,
        figsize=(12, 12)
    )

    axs = axs.flatten()

    for i, q in enumerate(quadrants):

        draw_single_hoist(
            axs[i],
            q["title"],
            q["mode"],
            q["loaded"],
            q["direction"],
            cage_y=4,
            torque=q["torque"],
            speed=q["speed"]
        )

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
            figsize=(12, 12)
        )

        axs = axs.flatten()

        for i, q in enumerate(quadrants):

            # Upward motion
            if q["direction"] == "up":

                cage_y = 2 + (step % 5)

            # Downward motion
            else:

                cage_y = 6 - (step % 5)

            draw_single_hoist(
                axs[i],
                q["title"],
                q["mode"],
                q["loaded"],
                q["direction"],
                cage_y,
                q["torque"],
                q["speed"]
            )

        plt.tight_layout()

        placeholder.pyplot(fig)

        plt.close(fig)

        time.sleep(0.4)

else:

    draw_static()
