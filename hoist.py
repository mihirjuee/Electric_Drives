import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time

st.set_page_config(page_title="4-Quadrant Hoist Simulation", layout="wide")

st.title("⚙️ Four Quadrant Operation of Hoist")

# Session state
if "run" not in st.session_state:
    st.session_state.run = False

# Buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Play Animation"):
        st.session_state.run = True

with col2:
    if st.button("⏹ Stop"):
        st.session_state.run = False

placeholder = st.empty()

quadrants = [
    {
        "title": "Quadrant I",
        "mode": "Forward Motoring",
        "loaded": True,
        "direction": "up"
    },
    {
        "title": "Quadrant II",
        "mode": "Forward Braking",
        "loaded": False,
        "direction": "down"
    },
    {
        "title": "Quadrant III",
        "mode": "Reverse Motoring",
        "loaded": False,
        "direction": "up"
    },
    {
        "title": "Quadrant IV",
        "mode": "Reverse Braking",
        "loaded": True,
        "direction": "down"
    }
]

def draw_single_hoist(ax, title, mode, loaded, direction, cage_y):

    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Pulley
    pulley = patches.Circle((5, 8), 1, fill=False, linewidth=3)
    ax.add_patch(pulley)

    # Rope
    ax.plot([4, 4], [8, 3], linewidth=3, color='black')
    ax.plot([6, 6], [8, cage_y], linewidth=3, color='black')

    # Counterweight
    counter = patches.Rectangle((3.3, 2), 1.4, 1.2,
                                facecolor='gray')
    ax.add_patch(counter)

    # Cage
    if loaded:
        cage_color = 'orange'
        label = "Loaded Cage"
    else:
        cage_color = 'lightblue'
        label = "Empty Cage"

    cage = patches.Rectangle((5.3, cage_y - 1),
                             1.4,
                             1.2,
                             facecolor=cage_color)

    ax.add_patch(cage)

    # Arrow
    if direction == "up":
        ax.arrow(8, cage_y - 0.5,
                 0, 1,
                 width=0.08,
                 head_width=0.35,
                 color='green')
    else:
        ax.arrow(8, cage_y + 0.5,
                 0, -1,
                 width=0.08,
                 head_width=0.35,
                 color='red')

    # Text
    ax.text(0.5, 9.4, title,
            fontsize=12,
            weight='bold')

    ax.text(0.5, 8.8, mode,
            fontsize=10)

    ax.text(0.5, 8.2, label,
            fontsize=10)

    ax.text(2.3, 1.5, "Counter Weight",
            fontsize=9)

    ax.axis('off')


# Animation Loop
if st.session_state.run:

    while st.session_state.run:

        # Up animation
        for step in range(5):

            fig, axs = plt.subplots(2, 2, figsize=(10, 10))

            axs = axs.flatten()

            for i, q in enumerate(quadrants):

                # UP motion
                if q["direction"] == "up":
                    cage_y = 2 + step

                # DOWN motion
                else:
                    cage_y = 6 - step

                draw_single_hoist(
                    axs[i],
                    q["title"],
                    q["mode"],
                    q["loaded"],
                    q["direction"],
                    cage_y
                )

            plt.tight_layout()

            placeholder.pyplot(fig)

            time.sleep(0.4)

else:
    fig, axs = plt.subplots(2, 2, figsize=(10, 10))

    axs = axs.flatten()

    for i, q in enumerate(quadrants):

        draw_single_hoist(
            axs[i],
            q["title"],
            q["mode"],
            q["loaded"],
            q["direction"],
            cage_y=4
        )

    plt.tight_layout()

    placeholder.pyplot(fig)

    st.info("Press ▶ Play Animation")
