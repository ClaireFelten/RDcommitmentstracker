import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import os

# Logging function
def log_message(message):
    with open("log.txt", "a") as log_file:
        log_file.write(f"{message}\n")

try:
    # Set page config
    st.set_page_config(layout="wide")
    log_message("Page config set successfully.")

    # Embed option
    embed_code = """
    <a href="https://share.streamlit.io/" target="_blank" style="position: absolute; top: 10px; right: 10px; background-color: #008CBA; color: white; padding: 10px 15px; border-radius: 5px; text-decoration: none;">Embed</a>
    """
    st.markdown(embed_code, unsafe_allow_html=True)
    log_message("Embed code added successfully.")

    # data
    csv_path = 'RDcomtrack_v4.csv'
    if not os.path.exists(csv_path):
        log_message(f"CSV file not found: {csv_path}")
        st.error(f"CSV file not found: {csv_path}")
    else:
        data = pd.read_csv(csv_path)
        log_message("CSV file loaded successfully.")
except Exception as e:
    log_message(f"An error occurred: {e}")
    st.error("An unexpected error occurred. Please check the log file for more details.")

# Convert data to DataFrame
df = pd.DataFrame(data)
df['USD_display'] = df['amntUSD'].apply(lambda x: f"{x/1000000000:.2f} billion USD" if x > 1000000000 else (
                                        f"{x/1000000:.2f} million USD" if x > 1000000 else (
                                        f"{x/1000:.2f} thousand USD" if x > 1000 else "(NOT FINANCIAL COMMITMENT)")))
total_money_pledged = df['amntUSD'].sum()
df['header'] = "DETAILS +"

# Custom CSS and JavaScript for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Aptos:wght@400;600&display=swap');
    
    body {
        font-family: 'Aptos', sans-serif;
        background-color: #f7f7f7;
    }
    .commitment-card {
        background-color: #ee6c4d;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
        overflow: hidden;
    }
    .commitment-header {
        display: flex;
        background-color: #3d5a80;
        color: white;
        padding: 15px;
    }
    .commitment-header-left {
        flex: 1;
        background-color: #98c1d9;
        margin-right: 5px;
        padding: 10px;
    }
    .commitment-header-right {
        flex: 2;
        padding: 10px;
    }
    .commitment-title {
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .commitment-date {
        font-size: 0.9em;
        letter-spacing: 3px; /* wide letter spacing */
        text-transform: uppercase; /* all caps text */
    }
    .commitment-maker-type {
        font-size: 0.9em;
        letter-spacing: 3px; /* wide letter spacing */
        text-transform: uppercase; /* all caps text */
    }
    .under-titles {
        font-size: 0.9em;
        letter-spacing: 3px; /* wide letter spacing */
        text-transform: uppercase; /* all caps text */
    }
    .commitment-info {
        display: flex;
        flex-wrap: wrap;
        padding: 15px;
        background-color: #f8f9fa;
    }
    .info-item {
        flex: 1 0 50%;
        margin-bottom: 10px;
    }
    .info-subitem {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
    }
    .info-icon {
        margin-right: 10px;
        color: #ee6c4d;
    }
    .details-header {
        background-color: #ee6c4d;
        color: white;
        padding: 10px 15px;
        cursor: pointer;
    }
    .details-content {
        padding: 15px;
        background-color: #f8f9fa;
    }
    .submit-update {
        background-color: #ee6c4d;
        color: white;
        padding: 10px 15px;
        text-align: center;
        cursor: pointer;
        font-weight: bold;
    }
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
        }   
    .line {
        width: 75%;
        height: 2px; /* Adjust the height as needed */
        background-color: white;
        font-weight: bold;
    }
    .big-number {
        font-size: 6em; /* 3x larger font size */
        text-align: center;
    }
    .chart-container {
        padding: 10px !important; /* Remove padding around the charts */
        margin: 10px !important; /* Remove margin around the charts */
    }
</style>
""", unsafe_allow_html=True)

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
type_counts = [filtered_df['type'].str.contains(t, case=False, na=False).sum() for t in typelist]
theme_counts = [filtered_df['themes'].str.contains(t, case=False, na=False).sum() for t in themelist]

type_counts_df = pd.DataFrame({'Type': typelist, 'Number of commitments': type_counts})
theme_counts_df = pd.DataFrame({'Theme': themelist, 'Number of commitments': theme_counts})

url = "https://github.com/datasets/geo-boundaries-world-110m/raw/master/countries.geojson"
world = gpd.read_file(url)

africa = world[world['continent'] == 'Africa']

african_countries = [
    'Algeria', 'Angola', 'Benin', 'Botswana', 'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cameroon', 'Central African Republic',
    'Chad', 'Comoros', 'Congo', 'Democratic Republic of the Congo', 'Djibouti', 'Egypt', 'Equatorial Guinea', 'Eritrea',
    'Eswatini', 'Ethiopia', 'Gabon', 'Gambia', 'Ghana', 'Guinea', 'Guinea-Bissau', 'Ivory Coast', 'Kenya', 'Lesotho', 'Liberia',
    'Libya', 'Madagascar', 'Malawi', 'Mali', 'Mauritania', 'Mauritius', 'Morocco', 'Mozambique', 'Namibia', 'Niger', 'Nigeria',
    'Rwanda', 'Sao Tome and Principe', 'Senegal', 'Seychelles', 'Sierra Leone', 'Somalia', 'South Africa', 'South Sudan', 
    'Sudan', 'Tanzania', 'Togo', 'Tunisia', 'Uganda', 'Zambia', 'Zimbabwe'
]

country_counts = [filtered_df['geography'].str.contains(c, case=False, na=False).sum() for c in african_countries]
country_counts_df = pd.DataFrame({'country': african_countries, 'Number of commitments relevant': country_counts})

africa = africa.merge(country_counts_df, left_on='name', right_on='country', how='left').infer_objects(copy=False)

# Calculate total money pledged in filtered group, and number of commitments
filtered_money_pledged = filtered_df['amntUSD'].sum()
total_commitments = len(filtered_df)

# Plotting the charts
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

fig_type = px.pie(type_counts_df, names='Type', values='Number of commitments', color='Type', 
                color_discrete_map={'Financial': 'green', 'Political': 'orange', 'In-kind': 'brown'})

fig_theme = px.pie(theme_counts_df, names='Theme', values='Number of commitments', color='Theme',
                color_discrete_map={'Manufacturing': 'royalblue', 'Regulatory': 'red', 'Clinical trials': 'purple'})

fig_type.update_traces(textposition='inside', textinfo='percent+label')
fig_type.update_layout(showlegend=False)

fig_theme.update_traces(textposition='inside', textinfo='percent+label')
fig_theme.update_layout(showlegend=False)

fig_money = px.bar(
    x=['Total money pledged', 'Money pledged (after filters applied)'],
    y=[total_money_pledged, filtered_money_pledged],
    labels={'x': '', 'y': 'USD'},
    color_discrete_map={'total_money_pledged': 'grey', 'filtered_money_pledged': 'green'},
    orientation='h'
)

# Display layout
left_col, right_col = st.columns([1, 1])

with left_col:
    st.plotly_chart(fig_map, use_container_width=True)

with right_col:
    with st.container():
        st.markdown(f"<div class='under-titles'> NUMBER OF COMMITMENTS LOGGED: </div><br><div class='big-number'>{total_commitments}</div>", unsafe_allow_html=True)


left_col2, right_col2 = st.columns([1, 1])

with left_col2:
    st.markdown(f"<div class='under-titles'> COMMITMENT TYPES: </div>", unsafe_allow_html=True)
    st.plotly_chart(fig_type, use_container_width=True, container_props={"className": "chart-container"})
        
with right_col2: 
    st.markdown(f"<div class='under-titles'> COMMITMENT THEMES: </div>", unsafe_allow_html=True)
    st.plotly_chart(fig_theme, use_container_width=True, container_props={"className": "chart-container"})

left_col3, right_col3 = st.columns([1, 1])
 
#with right_col3:
#    st.markdown(f"<div class='under-titles'> FUNDING COMMITTED: </div>", unsafe_allow_html=True)
#    st.plotly_chart(fig_money, use_container_width=True, container_props={"className": "chart-container"})

# Divider
st.markdown("---")

# Display commitments
st.subheader("List of commitments:")
for index, row in filtered_df.iterrows():
    st.markdown(f"""
        <div class="commitment-header">
                <div class="commitment-header-left">
                    <div class="commitment-maker-type"> {row['entityType']}</div>
                    <div class="line"></div>
                    <br>
                    <div class="commitment-title">{row['entity']}</div>
                </div>
                <div class="commitment-header-right">
                    <div class="commitment-date"> COMMITMENT DATE: {row['date']}</div>
                    <div class="line"></div>
                    <br>
                    <div class="commitment-title">{row['commName']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with st.expander(f"{row['header']}"):
        st.markdown(f"""
        <div class="commitment-card">
            <div class="commitment-info">
                <div class="info-item">
                    <div class="info-subitem">
                        <span class="info-icon">👤</span>
                        <div class="under-titles"> THEME: </div> 
                        {row['themes']}
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-subitem">
                        <span class="info-icon">🤝</span>
                        <div class="under-titles"> TYPE: </div> 
                        {row['type']}
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-subitem">
                        <span class="info-icon">🏭</span> 
                        <div class="under-titles"> SUBTHEME: </div> 
                        {row['subthemes']}
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-subitem">
                        <span class="info-icon">🌍</span>
                        <div class="under-titles"> {row['geography']} </div>
                    </div>
                </div>
                <div><br></div>
                <div class="info-item">
                    <div class="info-subitem">
                        <span class="info-icon">💰</span>
                        <div class="under-titles"> {row['USD_display']}</div>
                    </div>
                </div>
            </div>
            <div class="details-header">DETAILS</div>
            <div class="details-content">
                <p>{row['details']}</p>
                <p><strong>OTHER PARTNERS INVOLVED:</strong> {row.get('partners', 'N/A')}</p>
                <p><strong>UPDATES:</strong> {row['upd']}</p>
                <p><strong>SOURCE:</strong> <a href="{row['src']}" target="_blank">{row['src']}</a></p>
            </div>
            <div class="submit-update">SUBMIT AN UPDATE</div>
        </div>
        """, unsafe_allow_html=True)
