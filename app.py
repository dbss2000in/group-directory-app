import urllib.parse
import pandas as pd
import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Group Directory & Medical SOS", page_icon="📇", layout="wide"
)


@st.cache_data
def load_data():
  return pd.read_csv("people_data.csv")


df = load_data()

st.title("📇 Group Directory & Interactive SOS")
st.markdown("Cross-platform directory with quick navigation, communication, and medical emergency details.")

# Sidebar Navigation and Filters
st.sidebar.header("Navigation & Filters")
app_mode = st.sidebar.radio("Select Mode", ["Directory", "Submit Update / Feedback"])

if app_mode == "Directory":
  search_query = st.sidebar.text_input("Search by Name or Notes")
  favorite_filter = st.sidebar.checkbox("Show Favorites Only", value=False)

  filtered_df = df.copy()
  if search_query:
    filtered_df = filtered_df[
        filtered_df["Full Name"]
        .str.contains(search_query, case=False, na=False)
        | filtered_df["Notes"].str.contains(search_query, case=False, na=False)
    ]

  if favorite_filter:
    filtered_df = filtered_df[
        filtered_df["Is Favorite"].astype(str).str.upper() == "TRUE"
    ]

  if filtered_df.empty:
    st.warning("No entries found matching your criteria.")
  else:
    for index, row in filtered_df.iterrows():
      with st.expander(
          f"👤 {row['Full Name']}  |  🩸 Blood Group: {row['Blood Group']}"
      ):
        col1, col2 = st.columns(2)

        with col1:
          st.subheader("📞 Communication & Web")

          # Address with Google Maps Link
          address = row["Address"]
          maps_url = (
              f"https://www.google.com/maps/search/?api=1&query={urllib.parse.quote(str(address))}"
          )
          st.markdown(f"**Address:** [{address}]({maps_url})")

          # Phone & WhatsApp
          phone = row["Phone Number"]
          st.markdown(f"**Phone:** [{phone}](tel:{phone})")
          st.markdown(f"**WhatsApp Chat:** [Open Chat]({row['WhatsApp Chat']})")
          st.markdown(f"**WhatsApp Call:** [Voice Call](tel:{row['WhatsApp Call']})")

          # Socials & Web
          ig_handle = str(row["Instagram"]).strip()
          ig_url = (
              ig_handle
              if ig_handle.startswith("http")
              else f"https://instagram.com/{ig_handle.replace('@', '')}"
          )

          fb_val = str(row["Facebook"]).strip()
          fb_url = fb_val if fb_val.startswith("http") else f"https://{fb_val}"

          st.markdown(f"**Instagram:** [{ig_handle}]({ig_url})")
          st.markdown(f"**Facebook:** [Open Profile]({fb_url})")
          st.markdown(f"**Website:** [{row['Website']}]({row['Website']})")
          st.markdown(f"**Email:** [{row['Email']}](mailto:{row['Email']})")

        with col2:
          st.subheader("🚨 Medical Emergency & SOS")
          st.error(f"""
                - **Blood Group:** {row['Blood Group']}
                - **Allergies:** {row.get('Allergies', 'None')}
                - **Medical Conditions:** {row.get('Medical Conditions', 'None')}
                - **Medications:** {row.get('Medications', 'None')}
                """)

          emerg_phone = row["Emergency Contact Phone"]
          st.info(f"""
                **Emergency Contact:**
                - **Name:** {row['Emergency Contact Name']} ({row['Emergency Contact Relationship']})
                - **Phone:** [{emerg_phone}](tel:{emerg_phone})
                """)

        st.markdown("---")
        st.markdown(
            f"*Additional Notes:* {row['Notes']} | *Timezone:* {row['Timezone']}"
        )

elif app_mode == "Submit Update / Feedback":
  st.header("📝 Request an Entry Update or Addition")
  st.markdown(
      "Use the form below to submit modifications or add new members. Please sign in with your verified email address when prompted."
  )

  # Replace with your actual Google Form embed URL
  google_form_embed_url = "https://docs.google.com/forms/d/e/YOUR_FORM_EMBED_ID/viewform?embedded=true"
  st.components.v1.iframe(google_form_embed_url, height=800, scrolling=True)