import streamlit as st
import pandas as pd


def try_parse_float(value, default):
    if value:
        try:
            return float(value)
        except:
            return default
    return default


st.set_page_config(layout="wide")

CUSTOM_CSS = """
<style>
footer {visibility: hidden;}
.main .block-container {
    padding-top: 3rem;
    padding-bottom: 0rem;
}
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

st.title("Create unit entry")
st.write("")

source = st.sidebar.selectbox(
    label="Select a source", options=["qudt.org", "Energistics"]
)
if source == "qudt.org":
    df = pd.read_csv("qudt.csv")
if source == "Energistics":
    df = pd.read_csv("energistics.csv")

quantities = list(df["quantity"].unique())

quantity = st.sidebar.selectbox(label="Select a quantity", options=["All"] + quantities)

df_quantity = df[df["quantity"] == quantity] if quantity != "All" else df
df_quantity["selector"] = df_quantity["symbol"] + " - " + df_quantity["longName"]

unit = st.sidebar.selectbox(
    label="Select a unit",
    options=df_quantity["selector"].unique(),
)

item = df_quantity[df_quantity["selector"] == unit].reset_index().iloc[0, :].squeeze()

c1, c2, c3 = st.columns((20, 1, 20))

with c1:
    externalId = st.text_input(label="External ID", value=item["externalId"])

    c11, c12 = st.columns(2)
    name = c11.text_input(
        label="Name", value=item["name"] if source == "qudt.org" else item["symbol"]
    )
    symbol = c12.text_input(label="Symbol", value=item["symbol"])
    aliasNames = st.text_input(
        label="Alias names", value=item["symbol"], help="Separate items by comma"
    )
    quantity = st.text_input(label="Quantity", value=item["quantity"])

    c13, c14 = st.columns(2)
    multiplier = c13.number_input(
        label="Multiplier", value=try_parse_float(item["multiplier"], 1.0)
    )
    offset = c14.number_input(
        label="Offset", value=try_parse_float(item["offset"], 0.0)
    )
    source = st.text_input(label="Source", value=item["source"])
    sourceReference = st.text_input(
        label="Source reference", value=item["sourceReference"]
    )

unit_json = {
    "externalId": externalId,
    "name": name,
    "longName": item["longName"],
    "symbol": symbol,
    "aliasNames": aliasNames.split(","),
    "quantity": quantity,
    "conversion": {"multiplier": multiplier, "offset": offset},
    "source": source,
    "sourceReference": sourceReference,
}

c3.write(unit_json)
