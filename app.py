import urllib.parse
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Group Directory & Medical SOS", page_icon="📇", layout="wide"
)


@st.cache_data
def load_data():
  df = pd.read_csv("people_data.csv")
  # Clean column names to remove any hidden spaces or BOM characters
  df.columns = df.columns.str.strip().str.lstrip("\ufeff")
  return df


df = load_data()

st.title("📇 Group Directory & Interactive SOS")
st.markdown(
    "Cross-platform directory with quick navigation, communication, and medical"
    " emergency details."
)

# Sidebar Navigation and Filters
st.sidebar.header("Navigation & Filters")
app_mode = st.sidebar.radio(
    "Select Mode", ["Directory", "Submit Update / Feedback"]
)

if app_mode == "Directory":
  search_query = st.sidebar.text_input("Search by Name or Notes")
  favorite_filter = st.sidebar.checkbox("Show Favorites Only", value=False)

  filtered_df = df.copy()

  # Ensure columns exist before filtering
  name_col = (
      "Full Name" if "Full Name" in filtered_df.columns else filtered_df.columns[1]
  )
  notes_col = "Notes" if "Notes" in filtered_df.columns else None
  fav_col = "Is Favorite" if "Is Favorite" in filtered_df.columns else None

  if search_query:
    if notes_col:
      filtered_df = filtered_df[
          filtered_df[name_col].str.contains(search_query, case=False, na=False)
          | filtered_df[notes_col].str.contains(
              search_query, case=False, na=False
          )
      ]
    else:
      filtered_df = filtered_df[
          filtered_df[name_col].str.contains(search_query, case=False, na=False)
      ]

  if favorite_filter and fav_col:
    filtered_df = filtered_df[
        filtered_df[fav_col].astype(str).str.upper().isin(["TRUE", "1", "YES"])
    ]

  if filtered_df.empty:
    st.warning("No entries found matching your criteria.")
  else:
    for index, row in filtered_df.iterrows():
      name = row.get(name_col, "Member")
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
          st.markdown(f"**Website:** [{row.get('Website', '')}]({row.get('Website', '#')})")
          st.markdown(f"**Email:** [{row.get('Email', '')}](mailto:{row.get('Email', '')})")

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
            f"*Additional Notes:* {row.get('Notes', '')} | *Timezone:* {row.get('Timezone', '')}"
        )

elif app_mode == "Submit Update / Feedback":
  st.header("📝 Request an Entry Update or Addition")
  st.markdown(
      "Use the form below to submit modifications or add new members. Please sign in with your verified email address when prompted."
  )

  google_form_embed_url = "https://docs.google.com/forms/d/e/YOUR_FORM_EMBED_ID/viewform?embedded=true"
  st.components.v1.iframe(google_form_embed_url, height=800, scrolling=True)
