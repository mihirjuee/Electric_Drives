import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

st.set_page_config(page_title="Hoist Motion Simulation", layout="centered")

st.title("⚙️ Four Quadrant Hoist Motion Simulation")

# Session state
if "running" not in st.session_state:
    st.session_state.running = False

quadrants = [
    {
        "title": "Quadrant I",
        "mode": "Forward Motoring",
        "motion": "Loaded Cage Moving UP"
    },
    {
        "title": "Quadrant II",
        "mode": "Forward Braking",
        "motion": "Empty Cage Moving DOWN"
    },
    {
        "title": "Quadrant III",
        "mode": "Reverse Motoring",
        "motion": "Empty Cage Moving UP"
    },
    {
        "title": "Quadrant IV",
        "mode": "Reverse Braking",
        "motion": "Loaded Cage Moving DOWN"
    }
]

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Play Simulation"):
        st.session_state.running = True

with col2:
    if st.button("⏹ Stop"):
        st.session_state.running = False

placeholder = st.empty()

def draw_hoist(position, title, mode, motion):

    fig, ax = plt.subplots(figsize=(5, 7))

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Pulley
    pulley = patches.Circle((5, 8), 1, fill=False, linewidth=3)
    ax.add_patch(pulley)

    # Rope left side
    ax.plot([4, 4], [8, 3], linewidth=3)

    # Rope right side
    ax.plot([6, 6], [8, position], linewidth=3)

    # Counter weight
    counter = patches.Rectangle((3.4, 2), 1.2, 1)
    ax.add_patch(counter)

    # Cage
    cage = patches.Rectangle((5.4, position - 1), 1.2, 1)
    ax.add_patch(cage)

    # Motion Arrow
    if "UP" in motion:
        ax.arrow(
            8,
            position - 0.5,
            0,
            1,
            width=0.08,
            head_width=0.4,
            color='green'
        )
    else:
        ax.arrow(
            8,
            position + 0.5,
            0,
            -1,
            width=0.08,
            head_width=0.4,
            color='red'
        )

    # Text
    ax.text(0.5, 9.5, title, fontsize=14, weight='bold')
    ax.text(0.5, 9, mode, fontsize=12)
    ax.text(0.5, 8.5, motion, fontsize=12)

    ax.axis('off')

    return fig

# Animation
if st.session_state.running:

    for q in quadrants:

        # UP movement
        if "UP" in q["motion"]:
            positions = [2, 3, 4, 5, 6]

        # DOWN movement
        else:
            positions = [6, 5, 4, 3, 2]

        for pos in positions:

            if not st.session_state.running:
                break

            with placeholder.container():

                fig = draw_hoist(
                    pos,
                    q["title"],
                    q["mode"],
                    q["motion"]
                )

                st.pyplot(fig)

            time.sleep(0.4)

else:
    st.info("Press ▶ Play Simulation")
