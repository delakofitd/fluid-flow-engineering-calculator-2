# ============================================================
# AI DOCUMENTATION
# AI tools used: ChatGPT (GPT-5.6 Luna) for code generation,
# debugging, engineering-formula verification, and documentation.
#
# Key prompts used:
# 1. "Build a Streamlit fluid-flow engineering calculator for a
#    petroleum engineering student with sidebar inputs, a chart,
#    Pandas results table, and input validation."
# 2. "Implement Reynolds number, flow regime, Darcy friction
#    factor, velocity, pressure drop and head loss using clear
#    engineering equations and no unnecessary dependencies."
# 3. "Add a dynamic Plotly chart of pressure drop against flow rate,
#    robust warnings for invalid inputs, and explanatory instructions."
#
# Most important manual verification/fix:
# I manually verified the units and Darcy-Weisbach calculation,
# especially the conversion of flow rate from L/s to m^3/s and the
# use of dynamic viscosity in Pa.s when calculating Reynolds number.
# I also checked the laminar/turbulent friction-factor branches.
# ============================================================

import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="Fluid Flow Engineering Calculator",
    page_icon="💧",
    layout="wide",
)


def calculate_flow(
    flow_lps, diameter_mm, length_m, density, viscosity_mpas, roughness_mm
):
    """Calculate pipe-flow parameters using SI units internally."""
    flow_m3s = flow_lps / 1000.0
    diameter_m = diameter_mm / 1000.0
    viscosity_pas = viscosity_mpas / 1000.0
    roughness_m = roughness_mm / 1000.0

    area = math.pi * diameter_m**2 / 4.0
    velocity = flow_m3s / area
    reynolds = density * velocity * diameter_m / viscosity_pas
    relative_roughness = roughness_m / diameter_m

    if reynolds < 2300:
        regime = "Laminar"
        friction_factor = 64.0 / reynolds
    elif reynolds < 4000:
        regime = "Transitional"
        friction_factor = 0.25 / (
            math.log10(relative_roughness / 3.7 + 5.74 / reynolds**0.9) ** 2
        )
    else:
        regime = "Turbulent"
        friction_factor = 0.25 / (
            math.log10(relative_roughness / 3.7 + 5.74 / reynolds**0.9) ** 2
        )

    pressure_drop_pa = (
        friction_factor * (length_m / diameter_m) * density * velocity**2 / 2.0
    )
    pressure_drop_kpa = pressure_drop_pa / 1000.0
    head_loss_m = pressure_drop_pa / (density * 9.81)

    return {
        "Flow rate (L/s)": flow_lps,
        "Velocity (m/s)": velocity,
        "Reynolds number": reynolds,
        "Flow regime": regime,
        "Darcy friction factor": friction_factor,
        "Pressure drop (kPa)": pressure_drop_kpa,
        "Head loss (m)": head_loss_m,
    }


st.title("💧 Fluid Flow Engineering Calculator")
st.subheader("A practical pipe-flow analysis tool for petroleum engineering")
st.write(
    "Use the sidebar to enter pipe and fluid properties. The calculator "
    "updates velocity, Reynolds number, flow regime, Darcy friction "
    "factor, pressure drop, and head loss automatically."
)
st.info(
    "**Instructions:** Enter positive physical values in the sidebar. "
    "The chart shows how pressure drop changes as flow rate changes while "
    "the other pipe/fluid properties remain fixed."
)

st.sidebar.header("Pipe & Fluid Inputs")
flow_lps = st.sidebar.number_input(
    "Flow rate (L/s)", min_value=0.0, value=10.0, step=0.5
)
diameter_mm = st.sidebar.number_input(
    "Pipe diameter (mm)", min_value=0.0, value=100.0, step=5.0
)
length_m = st.sidebar.number_input(
    "Pipe length (m)", min_value=0.0, value=100.0, step=10.0
)
density = st.sidebar.number_input(
    "Fluid density (kg/m³)", min_value=0.0, value=850.0, step=10.0
)
viscosity_mpas = st.sidebar.number_input(
    "Dynamic viscosity (mPa·s)", min_value=0.0, value=2.0, step=0.1
)
roughness_mm = st.sidebar.number_input(
    "Pipe roughness (mm)",
    min_value=0.0,
    value=0.045,
    step=0.005,
    format="%.4f",
)
chart_max_lps = st.sidebar.slider(
    "Chart maximum flow rate (L/s)",
    min_value=5.0,
    max_value=100.0,
    value=50.0,
    step=5.0,
)

inputs = {
    "Flow rate": flow_lps,
    "Pipe diameter": diameter_mm,
    "Pipe length": length_m,
    "Fluid density": density,
    "Dynamic viscosity": viscosity_mpas,
}
invalid = [name for name, value in inputs.items() if value <= 0]

if invalid:
    st.warning(
        "Please enter values greater than zero for: " + ", ".join(invalid) + "."
    )
    st.stop()

if roughness_mm < 0:
    st.warning("Pipe roughness cannot be negative.")
    st.stop()

try:
    result = calculate_flow(
        flow_lps,
        diameter_mm,
        length_m,
        density,
        viscosity_mpas,
        roughness_mm,
    )
except (ValueError, ZeroDivisionError, OverflowError) as exc:
    st.warning(f"The calculation could not be completed with these inputs: {exc}")
    st.stop()

metric_cols = st.columns(4)
metric_cols[0].metric("Velocity", f"{result['Velocity (m/s)']:.3f} m/s")
metric_cols[1].metric("Reynolds Number", f"{result['Reynolds number']:,.0f}")
metric_cols[2].metric("Pressure Drop", f"{result['Pressure drop (kPa)']:.3f} kPa")
metric_cols[3].metric("Flow Regime", result["Flow regime"])

st.subheader("Calculation Results")
results_df = pd.DataFrame(
    [
        ["Velocity", f"{result['Velocity (m/s)']:.4f}", "m/s"],
        ["Reynolds number", f"{result['Reynolds number']:.0f}", "dimensionless"],
        ["Flow regime", result["Flow regime"], "-"],
        [
            "Darcy friction factor",
            f"{result['Darcy friction factor']:.5f}",
            "dimensionless",
        ],
        ["Pressure drop", f"{result['Pressure drop (kPa)']:.4f}", "kPa"],
        ["Head loss", f"{result['Head loss (m)']:.4f}", "m"],
    ],
    columns=["Parameter", "Value", "Unit"],
)
st.dataframe(results_df, use_container_width=True, hide_index=True)

st.subheader("Pressure Drop vs Flow Rate")
flow_values = [max(0.1, chart_max_lps * i / 50.0) for i in range(1, 51)]
pressure_values = []

for q in flow_values:
    q_result = calculate_flow(
        q, diameter_mm, length_m, density, viscosity_mpas, roughness_mm
    )
    pressure_values.append(q_result["Pressure drop (kPa)"])

fig = go.Figure()
fig.add_trace(
    go.Scatter(
        x=flow_values,
        y=pressure_values,
        mode="lines+markers",
        name="Pressure drop",
    )
)
fig.add_vline(
    x=flow_lps,
    line_dash="dash",
    annotation_text="Selected flow",
    annotation_position="top right",
)
fig.update_layout(
    xaxis_title="Flow rate (L/s)",
    yaxis_title="Pressure drop (kPa)",
    title="Pipe Pressure-Drop Characteristic",
    hovermode="x unified",
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Engineering Notes")
st.markdown(
    "- **Reynolds number:** $Re = \\rho VD/\\mu$\n"
    "- **Darcy-Weisbach pressure drop:** $\\Delta P = f(L/D)(\\rho V^2/2)$\n"
    "- **Head loss:** $h_f = \\Delta P/(\\rho g)$\n"
    "- Laminar flow uses $f=64/Re$; turbulent flow uses the explicit "
    "Swamee–Jain approximation."
)

st.caption(
    "Educational calculator — verify design calculations against applicable "
    "engineering standards before use in the field."
)
