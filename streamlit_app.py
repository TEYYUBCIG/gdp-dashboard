import streamlit as st
import pandas as pd

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("Duplicates.csv")
    df.columns = ["duplicate_name", "main_name"]
    return df

df = load_data()

st.title("🧹 Producer Name Deduplication Tool")
st.markdown("Select which duplicate names should be **mapped** to the main name.")

# Group by main_name
grouped = df.groupby("main_name")

confirmed_mappings = []

for main_name, group in grouped:
    st.subheader(f"Main Name: **{main_name}**")
    selected = st.multiselect(
        label=f"Select confirmed duplicates for: {main_name}",
        options=group["duplicate_name"].tolist(),
        key=main_name
    )
    for dup in selected:
        confirmed_mappings.append({
            "duplicate_name": dup,
            "main_name": main_name
        })

# Save confirmed mappings
if confirmed_mappings:
    if st.button("💾 Export Confirmed Mappings"):
        out_df = pd.DataFrame(confirmed_mappings)
        out_df.to_csv("confirmed_mappings.csv", index=False)
        st.success("✅ Confirmed mappings saved to `confirmed_mappings.csv`.")
