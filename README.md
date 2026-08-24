# Fluid Flow Engineering Calculator

A Streamlit-based petroleum engineering calculator for analysing steady pipe flow. The app accepts pipe and fluid properties, calculates velocity, Reynolds number, flow regime, Darcy friction factor, Darcy-Weisbach pressure drop, and head loss, then presents the results in a Pandas table and visualises pressure drop against flow rate with an interactive Plotly chart. It was developed as an AI-assisted/vibe-coding engineering project and includes input validation so invalid physical values produce warnings rather than crashes.

## Live App

**Live Streamlit URL:** `https://fluid-flow-engineering-calculator-2-cxj4q5hkesgg5yrdvybwmg.streamlit.app/

Replace the placeholder above with the actual public URL after deployment.

## GitHub Repository

https://github.com/delakofitd/fluid-flow-engineering-calculator-2

## Requirements covered

- Sidebar with more than 3 interactive input controls
- Dynamic Plotly chart
- Pandas results table
- Warning-based error handling
- Title, subtitle, and user instructions
- `requirements.txt`
- AI documentation block at the top of `app.py`
- Public GitHub repository
- At least 3 meaningful commits

## Engineering equations

The calculator uses SI units internally.

- Reynolds number: `Re = rho * V * D / mu`
- Laminar Darcy friction factor: `f = 64 / Re`
- Turbulent Darcy friction factor: Swamee-Jain explicit approximation
- Darcy-Weisbach pressure drop: `Delta P = f * (L/D) * rho * V^2 / 2`
- Head loss: `h_f = Delta P / (rho * g)`

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Suggested commit history

1. `Build core fluid flow calculator with engineering calculations and validation`
2. `Add Streamlit and plotting dependencies`
3. `Add project documentation and deployment instructions`
4. Add live Streamlit deployment URL

## Deployment

Use Streamlit Community Cloud to deploy the public GitHub repository. Select:

- Repository: `delakofitd/fluid-flow-engineering-calculator-2`
- Branch: `main`
- Main file path: `app.py`

After deployment, paste the generated `https://...streamlit.app` URL into the Live App section above and commit that README update.
