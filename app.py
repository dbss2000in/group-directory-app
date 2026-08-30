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
  df = df.fillna("None")
  return df


df = load_data()

st.title("📇 Group Directory & Interactive SOS (India)")
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
              if address != "None" and address
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
            f" {row.get('Timezone', 'Asia/Kolkata')}"
        )

elif app_mode == "Submit Update / Feedback":
  st.header("📝 Request an Entry Update or Addition")
  st.markdown(
      "Fill out the form below to submit modifications or add new member"
      " details. Submissions will be sent directly to the group"
      " administrator."
  )

  with st.expander(
      "📋 View Database Fields & Example Format (Click to Expand)"
  ):
    st.markdown("""
        When requesting an update or addition, please include as many of the following fields as applicable:
        - **Full Name:** Aarav Sharma
        - **Address:** Flat 402, Lotus Apartments, MG Road, Bangalore 560001
        - **Phone Number:** +91-98765-43210
        - **WhatsApp Call / Chat:** +91-98765-43210 or https://wa.me/919876543210
        - **Instagram / Facebook:** @aarav_sharma / fb.com/aaravsharma
        - **Email / Website:** aarav.sharma@example.com / https://aaravsharma.dev
        - **Blood Group:** O+
        - **Allergies:** None
        - **Medical Conditions:** None
        - **Medications:** None
        - **Emergency Contact Name & Relationship:** Priya Sharma (Spouse)
        - **Emergency Contact Phone:** +91-98765-43211
        - **Birthday & Timezone:** 15-06-1988 / West Bengal/Kolkata
        - **Notes:** Prefers WhatsApp messages over calls.
        """)

  formspree_url = "https://formspree.io/f/xwlkpdwb"

  form_html = f"""
    <form action="{formspree_url}" method="POST" style="max-width: 600px; font-family: sans-serif;">
        <div style="margin-bottom: 15px;">
            <label style="display: block; font-weight: bold; margin-bottom: 5px;">Your Email Address:</label>
            <input type="email" name="email" required style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;" placeholder="name@example.com">
        </div>
        <div style="margin-bottom: 15px;">
            <label style="display: block; font-weight: bold; margin-bottom: 5px;">Full Name (Member):</label>
            <input type="text" name="full_name" required style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;" placeholder="Aarav Sharma">
        </div>
        <div style="margin-bottom: 15px;">
            <label style="display: block; font-weight: bold; margin-bottom: 5px;">Update Details / New Information:</label>
            <textarea name="update_details" rows="6" required style="width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px;" placeholder="Type your update details here..."></textarea>
        </div>
        <button type="submit" style="background-color: #ff4b4b; color: white; padding: 10px 20px; border: none; border-radius: 4px; font-weight: bold; cursor: pointer;">Submit Request</button>
    </form>
    """
  st.components.v1.html(form_html, height=500)
