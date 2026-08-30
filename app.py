import urllib.parse
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Group Directory & Medical SOS", page_icon="📇", layout="wide"
)


@st.cache_data(ttl=600)
def load_data():
  sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRdR30A6c3cRpzS_yBSPP_LHWaRNE0YinscZfVf6xWeJfqjdvpPG_2JcVnTKp7dfUkl5NjR170Q1-lo/pub?output=csv"
  df = pd.read_csv(sheet_url)
  df.columns = df.columns.str.strip().str.lstrip("\ufeff")
  return df


df = load_data()

st.title("📇 Group Directory & Interactive SOS")
st.markdown(
    "Cross-platform directory with quick navigation, communication, and medical"
    " emergency details."
)

st.sidebar.header("Navigation & Filters")
app_mode = st.sidebar.radio(
    "Select Mode", ["Directory", "Submit Update / Feedback"]
)

if app_mode == "Directory":
  search_query = st.sidebar.text_input("Search by Name or Notes")
  favorite_filter = st.sidebar.checkbox("Show Favorites Only", value=False)

  filtered_df = df.copy()

  if search_query:
    filtered_df = filtered_df[
        filtered_df["Full Name"].str.contains(search_query, case=False, na=False)
        | filtered_df["Notes"].str.contains(search_query, case=False, na=False)
    ]

  if favorite_filter and "Is Favorite" in filtered_df.columns:
    filtered_df = filtered_df[
        filtered_df["Is Favorite"]
        .astype(str)
        .str.upper()
        .isin(["TRUE", "1", "YES"])
    ]

  if filtered_df.empty:
    st.warning("No entries found matching your criteria.")
  else:
    for index, row in filtered_df.iterrows():
      name = row["Full Name"]
      blood = row.get("Blood Group", "N/A")
      with st.expander(f"👤 {name}  |  🩸 Blood Group: {blood}"):
        col1, col2 = st.columns(2)

        with col1:
          st.subheader("📞 Communication & Web")

          address = row.get("Address", "")
          maps_url = (
              f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(str(address))}"
              if address
              else "#"
          )
          st.markdown(f"**Address:** [{address}]({maps_url})")

          phone = row.get("Phone Number", "")
          st.markdown(f"**Phone:** [{phone}](tel:{phone})")
          st.markdown(
              f"**WhatsApp Chat:** [Open Chat]({row.get('WhatsApp Chat', '#')})"
          )
          st.markdown(
              f"**WhatsApp Call:** [Voice Call](tel:{row.get('WhatsApp Call', '')})"
          )

          ig_handle = str(row.get("Instagram", "")).strip()
          ig_url = (
              ig_handle
              if ig_handle.startswith("http")
              else f"https://instagram.com/{ig_handle.replace('@', '')}"
          )

          fb_val = str(row.get("Facebook", "")).strip()
          fb_url = fb_val if fb_val.startswith("http") else f"https://{fb_val}"

          st.markdown(f"**Instagram:** [{ig_handle}]({ig_url})")
          st.markdown(f"**Facebook:** [Open Profile]({fb_url})")
          st.markdown(
              f"**Website:** [{row.get('Website', '')}]({row.get('Website', '#')})"
          )
          st.markdown(
              f"**Email:** [{row.get('Email', '')}](mailto:{row.get('Email', '')})"
          )

        with col2:
          st.subheader("🚨 Medical Emergency & SOS")
          st.error(f"""
                - **Blood Group:** {row.get('Blood Group', 'N/A')}
                - **Allergies:** {row.get('Allergies', 'None')}
                - **Medical Conditions:** {row.get('Medical Conditions', 'None')}
                - **Medications:** {row.get('Medications', 'None')}
                """)

          emerg_phone = row.get("Emergency Contact Phone", "")
          st.info(f"""
                **Emergency Contact:**
                - **Name:** {row.get('Emergency Contact Name', 'N/A')} ({row.get('Emergency Contact Relationship', '')})
                - **Phone:** [{emerg_phone}](tel:{emerg_phone})
                """)

        st.markdown("---")
        st.markdown(
            f"*Additional Notes:* {row.get('Notes', '')} | *Timezone:*"
            f" {row.get('Timezone', '')}"
        )

elif app_mode == "Submit Update / Feedback":
  st.header("📝 Request an Entry Update or Addition")
  st.markdown(
      "Use the form below to submit modifications or add new members. Please"
      " sign in with your verified email address when prompted."
  )
  google_form_embed_url = (
      "https://docs.google.com/forms/d/e/YOUR_FORM_EMBED_ID/viewform?embedded=true"
  )
  st.components.v1.iframe(google_form_embed_url, height=800, scrolling=True)
