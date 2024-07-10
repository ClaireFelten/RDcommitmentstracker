import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd


# data
data = pd.read_csv('RDcomtrack_v4.csv')

# Convert data to DataFrame
df = pd.DataFrame(data)

st.set_page_config(layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
    .streamlit-expanderHeader {
        background-color: #2c3e50 !important;  /* dark blue-gray color */
        color: white !important;  /* white writing */
        border: none !important;
        border-radius: 5px !important;
        padding: 10px !important;
        margin-bottom: 15px !important;
        font-size: 18px !important;
        display: flex;
        justify-content: space-between;
        align-items: center;
        <iframe
            src="https://30days.streamlit.app?embed=true"
            style="height: 450px; width: 100%;"
        ></iframe>
        }
    .streamlit-expanderHeader::after {
        content: '▼';  /* clear down arrow */
        font-size: 18px;
        color: white;
        margin-left: auto;
        }
        
.streamlit-expanderContent {
    background-color: #FAF9F6 !important;  /* off white color */
    color: #2c3e50 !important;  /* dark blue-gray text */
    border-radius: 5px !important;
    padding: 15px !important;
    margin-bottom: 10px !important;
}
    .commitment-details {
        display: flex;
        flex-direction: column;
        gap: 10px;
        margin-top: 10px;
        font-size: 16px;
    }
    .commitment-details strong {
        color: #ec7063;
    }
    .commitment-title {
        font-size: 22px !important;
        font-weight: bold !important;
        color: #ec7063 !important;  /* soft red title */
        margin-bottom: 5px !important;
    }
    .commitment-entity {
        font-size: 18px !important;
        color: #34495e !important;
        margin-bottom: 10px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app
st.title("R&D Commitments Tracker")

typelist = ['Financial', 'Political', 'In-kind']
themelist = ['Manufacturing','Regulatory', 'Clinical trials']
stlist = pd.concat([df['st1'], df['st2'], df['st3']]).unique().tolist()

# Sidebar for filters
st.sidebar.title("Filter Commitments")
selected_type = st.sidebar.selectbox("Type of Commitment", ["All"] + typelist)
selected_theme = st.sidebar.selectbox("Theme", ["All"] + themelist)
selected_subtheme = st.sidebar.selectbox("Subtheme Area", ["All"] + stlist)
selected_entity = st.sidebar.selectbox("Committing entity", ["All"] + df['entity'].unique().tolist())
search_query = st.sidebar.text_input("Search", "")

# Filter data based on sidebar inputs
filtered_df = df.copy()

if search_query:
    filtered_df = filtered_df[
        filtered_df['commName'].str.contains(search_query, case=False, na=False) |
        filtered_df['details'].str.contains(search_query, case=False, na=False)
    ]

if selected_type != "All":
    filtered_df = filtered_df[filtered_df['type'].str.contains(selected_type)]

if selected_theme != "All":
    filtered_df = filtered_df[filtered_df['themes'].str.contains(selected_theme)]

if selected_subtheme != "All":
    filtered_df = filtered_df[filtered_df['subthemes'].str.contains(selected_subtheme)]

if selected_entity != "All":
    filtered_df = filtered_df[filtered_df['entity'].str.contains(selected_entity)]

# Display overall count of filtered commitments
st.sidebar.divider()
st.sidebar.header(f"Number of commitments: {len(filtered_df)}")

# Pie charts for commitments

# Count the occurrences of each type and theme in the filtered dataframe
type_counts = [filtered_df['type'].str.contains(t, case=False, na=False).sum() for t in typelist]
theme_counts = [filtered_df['themes'].str.contains(t, case=False, na=False).sum() for t in themelist]

# Create DataFrames for plotting
type_counts_df = pd.DataFrame({'Type': typelist, 'Number of commitments': type_counts})
theme_counts_df = pd.DataFrame({'Theme': themelist, 'Number of commitments': theme_counts})

url = "https://github.com/datasets/geo-boundaries-world-110m/raw/master/countries.geojson"
world = gpd.read_file(url)

africa = world[world['continent'] == 'Africa']

# Mapping 'Africa Region' to all African countries
african_countries = [
    'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cameroon', 'Central African Republic',
    'Chad', 'Comoros', 'Congo', 'Democratic Republic of the Congo', 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea',
    'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Ivory Coast', 'Kenya', 'Lesotho', 'Liberia',
    'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria',
    'Rwanda', 'Sao Tome and Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 
    'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe'
]

# Create a count of commitments by country
country_counts = [filtered_df['geography'].str.contains(c, case=False, na=False).sum() for c in african_countries]
country_counts_df = pd.DataFrame({'country': african_countries, 'Number of commitments relevant': country_counts})

africa = africa.merge(country_counts_df, left_on='name', right_on='country', how='left').infer_objects(copy=False)

col1, col2 = st.columns([1.5, 1])
with col1:
    # Display commitments
    st.subheader("List of commitments:")
    for index, row in filtered_df.iterrows():
            expander_html = f"""
            <details>
                <summary class="streamlit-expanderHeader">{row['commName']} - {row['entity']}</summary>
                <div class="streamlit-expanderContent">
                    <div class="commitment-container">
                        <div class="commitment-title">{row['commName']}</div>
                        <div class="commitment-entity">{row['entity']}</div>
                        <div class="commitment-details">
                            <strong>Type:</strong> {row['type']}<br>
                            <strong>Theme:</strong> {row['themes']}<br>
                            <strong>Subtheme:</strong> {row['subthemes']}<br><br><br>
                            <strong>Geography:</strong> {row['geography']}<br>
                            <strong>Funding (USD):</strong> {row['amntUSD']}<br><br><br>
                            <strong>Details:</strong> {row['details']}<br>
                            <strong>Source:</strong> {row['src']}<br>
                            <strong>Updates:</strong> {row['upd']}
                        </div>
                    </div>
                </div>
            </details>
            """
            st.markdown(expander_html, unsafe_allow_html=True)

with col2:
    fig_map = px.choropleth(
        africa,
        geojson=africa.geometry,
        locations=africa.index,
        color='Number of commitments relevant',
        hover_name='name',
        color_continuous_scale='Blues',
    )
    fig_map.update_layout(coloraxis_showscale=False, showlegend=False)
    fig_map.update_geos(fitbounds="locations", visible=False, projection_type="mercator")
    st.plotly_chart(fig_map, use_container_width=True)

    fig_type = px.pie(type_counts_df, names='Type', values='Number of commitments', title='Number of commitments by type:', color='Type', 
                    color_discrete_map={'Financial': 'green', 'Political': 'orange', 'In-kind': 'brown'})
    st.plotly_chart(fig_type, use_container_width=True)
    
    fig_theme = px.pie(theme_counts_df, names='Theme', values='Number of commitments', title='Number of commitments by theme:', color='Theme',
                    color_discrete_map={'Manufacturing': 'royalblue', 'Regulatory': 'red', 'Clinical trials': 'purple'})
    st.plotly_chart(fig_theme, use_container_width=True)
