
import random
import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="Smart Energy Monitor",
    page_icon="⚡",
    layout="wide"
)

# ---------------- CUSTOM DASHBOARD DESIGN ----------------

st.markdown("""
<style>
/* Main background */
.stApp {
    background: linear-gradient(135deg, #08111f 0%, #101d31 55%, #0c1728 100%);
    color: #edf4ff;
}

/* Main content spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

/* Headings */
h1 {
    color: #f4f8ff !important;
    font-size: 2.3rem !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #e6efff !important;
}

/* Reading metric cards */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #172941, #112035);
    border: 1px solid #2b4563;
    padding: 20px 18px;
    border-radius: 16px;
    box-shadow: 0 6px 18px rgba(0, 0, 0, 0.18);
}

/* Metric labels and values */
div[data-testid="stMetricLabel"] {
    color: #a9bfd9 !important;
}

div[data-testid="stMetricValue"] {
    color: #50e3a4 !important;
    font-weight: 750;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #10b981, #34d399);
    color: #071521 !important;
    border: none;
    border-radius: 10px;
    padding: 0.65rem 1.1rem;
    font-weight: 700;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background: #6ee7b7;
    border: none;
    transform: translateY(-1px);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #0d192a;
    border-right: 1px solid #223750;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 12px;
}

/* Reading table */
div[data-testid="stDataFrame"] {
    border: 1px solid #2b4563;
    border-radius: 12px;
    overflow: hidden;
}

/* Download button */
.stDownloadButton > button {
    border-radius: 10px;
    font-weight: 650;
}

/* Small-screen support */
@media (max-width: 768px) {
    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }

    h1 {
        font-size: 1.7rem !important;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------------- DASHBOARD TITLE ----------------
st.title("⚡ Smart Energy Monitor")
st.caption("IoT-Based Smart Energy Consumption Monitoring System")
st.info(
    "Demo mode: readings are simulated, "
    "not collected from physical sensors."
)

# ---------------- SIDEBAR SETTINGS ----------------
st.sidebar.header("⚙️ Settings")

tariff = st.sidebar.number_input(
    "Electricity rate (₹ per kWh)",
    min_value=0.0,
    value=8.0,
    step=0.5
)

threshold = st.sidebar.slider(
    "Power alert threshold (W)",
    min_value=100,
    max_value=2500,
    value=1500
)

# ---------------- STORE READINGS ----------------
if "readings" not in st.session_state:
    st.session_state.readings = []

# ---------------- GENERATE NEW READING ----------------
if st.button("⚡ Generate New Reading"):
    voltage = round(random.uniform(215, 240), 2)
    current = round(random.uniform(0.5, 10), 2)
    power = round(voltage * current, 2)

    # Each reading represents one simulated minute
    energy = power / 60000

    if st.session_state.readings:
        previous_energy = st.session_state.readings[-1]["Energy (kWh)"]
    else:
        previous_energy = 0

    total_energy = previous_energy + energy

    new_reading = {
        "Time": pd.Timestamp.now().strftime("%H:%M:%S"),
        "Voltage (V)": voltage,
        "Current (A)": current,
        "Power (W)": power,
        "Energy (kWh)": round(total_energy, 6)
    }

    st.session_state.readings.append(new_reading)

# ---------------- DISPLAY DASHBOARD ----------------
if st.session_state.readings:

    df = pd.DataFrame(st.session_state.readings)
    latest = df.iloc[-1]

    # Reading cards
    st.markdown("## 📊 Live Energy Overview")
    st.caption("Monitor electrical readings and estimated consumption.")

    col1, col2, col3, col4 = st.columns(4, gap="medium")

    with col1:
        st.metric(
            "🔌 Voltage",
            f'{latest["Voltage (V)"]} V'
        )

    with col2:
        st.metric(
            "⚡ Current",
            f'{latest["Current (A)"]} A'
        )

    with col3:
        st.metric(
            "📈 Power",
            f'{latest["Power (W)"]} W'
        )

    with col4:
        st.metric(
            "🔋 Energy Used",
            f'{latest["Energy (kWh)"]:.5f} kWh'
        )

    # Estimated electricity cost
    cost = latest["Energy (kWh)"] * tariff

    st.markdown("## 💰 Estimated Electricity Cost")
    st.metric("Estimated Cost", f"₹{cost:.4f}")

    # Power consumption alert
    if latest["Power (W)"] > threshold:
        st.error("⚠️ High power consumption detected!")
    else:
        st.success(
            "✅ Power consumption is within the configured limit."
        )

    # ---------------- GRAPHS ----------------
    
    # ---------------- GRAPHS ----------------
    st.markdown("## 📉 Consumption Analytics")

    if len(df) < 2:
        st.info("Generate at least 2 readings to display the graphs.")
    else:
        chart1, chart2 = st.columns(2, gap="large")

        with chart1:
            st.markdown("### ⚡ Power Consumption")

            fig = px.line(
                df,
                x="Time",
                y="Power (W)",
                markers=True,
                title="Power Usage Over Time",
                template="plotly_dark"
            )

            fig.update_traces(
                line=dict(width=3),
                marker=dict(size=8)
            )

            fig.update_layout(
                height=380,
                xaxis_title="Time",
                yaxis_title="Power (Watts)",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(23,36,56,0.7)",
                margin=dict(l=20, r=20, t=60, b=40)
            )

            st.plotly_chart(fig, use_container_width=True)

        with chart2:
            st.markdown("### 🔋 Energy Consumption")

            fig2 = px.line(
                df,
                x="Time",
                y="Energy (kWh)",
                markers=True,
                title="Cumulative Energy Usage",
                template="plotly_dark"
            )

            fig2.update_traces(
                line=dict(width=3),
                marker=dict(size=8)
            )

            fig2.update_layout(
                height=380,
                xaxis_title="Time",
                yaxis_title="Energy (kWh)",
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(23,36,56,0.7)",
                margin=dict(l=20, r=20, t=60, b=40)
            )

            st.plotly_chart(fig2, use_container_width=True)


    # ---------------- READING HISTORY ----------------
    st.markdown("## 📋 Reading History")

    st.dataframe(
        df,
        use_container_width=True
    )

    # ---------------- DOWNLOAD CSV ----------------
    st.download_button(
        label="📥 Download Readings as CSV",
        data=df.to_csv(index=False),
        file_name="energy_readings.csv",
        mime="text/csv"
    )

else:
    st.info(
        "Click 'Generate New Reading' to start monitoring."
    )
