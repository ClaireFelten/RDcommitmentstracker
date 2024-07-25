import streamlit as st
import pandas as pd
import plotly.express as px
import geopandas as gpd
import os
import base64
from pathlib import Path
import warnings

warnings.filterwarnings('ignore')

# Logging function
def log_message(message):
    with open("log.txt", "a") as log_file:
        log_file.write(f"{message}\n")

try:
    # Set page config
    st.set_page_config(layout="wide")
    log_message("Page config set successfully.")

    # Embed option
   # embed_code = """
    #<a href="https://share.streamlit.io/" target="_blank" style="position: absolute; top: 10px; right: 10px; background-color: #008CBA; color: white; padding: 10px 15px; border-radius: 5px; text-decoration: none;">Embed</a>
   # """
    #st.markdown(embed_code, unsafe_allow_html=True)
    #log_message("Embed code added successfully.")

    # data
    csv_path = 'RDcomtrack_v4.csv'
    if not os.path.exists(csv_path):
        log_message(f"CSV file not found: {csv_path}")
        st.error(f"CSV file not found: {csv_path}")
    else:
        log_message("CSV file loaded successfully.")
except Exception as e:
    log_message(f"An error occurred: {e}")
    st.error("An unexpected error occurred. Please check the log file for more details.")

data = pd.read_csv(csv_path)

# image and icon loading
#def img_to_base64(img_path):
#    with open(img_path, "rb") as img_file:
 #       return base64.b64encode(img_file.read()).decode('utf-8')

def img_to_base64(img_path):
    if not os.path.isfile(img_path):
        return ''  # Return an empty string or a placeholder base64 string
    with open(img_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
    
theme_icons = {
    'Manufacturing': 'images/MANU.png',
    'Regulatory': 'images/REG.png',
    'Regulatory/Quality': 'images/REG.png',
    'Clinical Trial Strengthening': 'images/CT.png',
    'Clinical Trials': 'images/CT.png',
    'Clinical trials': 'images/CT.png'
}

icons_pies = {
    'Manufacturing': 'images/MANU-wh-icon.png',
    'Regulatory': 'images/REG-wh-icon.png',
    'Regulatory/Quality': 'images/REG-wh-icon.png',
    'Clinical Trial Strengthening': 'images/CT-wh-icon.png',
    'Clinical Trials': 'images/CT-wh-icon.png',
    'Clinical trials': 'images/CT-wh-icon.png',
    'Financial': 'images/fin-wh-icon.png',
    'Political': 'images/pol-wh-icon.png',
    'In-kind': 'images/ik-wh-icon.png'
}

type_icons = {
    'Financial': 'images/fin.png',
    'Political': 'images/pol.png',
    'In-kind': 'images/ik.png'
}

subtheme_icons = {
    'Medicines manufacturing - using imported API': 'images/MANU_medmanimp.png',
    'End-to-end medicines manufacturing - including manufacturing API': 'images/MANU_e2emedman.png',
    'Vaccines manufacturing - including mRNA vax': 'images/MANU_vax.png',
    'Diagnostics and other medical devices manufacturing': 'images/MANU_diagmeddev.png',
    'Tech transfer': 'images/MANU_techtran.png',
    'Other manufacturing': 'images/MANU_oth.png',
    'African Medicines Agency': 'images/REG_ama.png',
    'National/regional regulatory authorities capacity building': 'images/REG_nra.png',
    'Quality': 'images/REG_qual.png',
    'Other regulatory/quality': 'images/REG_oth.png',
    'Clinical trials capacity building/expansion': 'images/CT_capbuild.png',
    'Clinical trials technology and innovation': 'images/CT_techinnov.png',
    'Clinical trials data management': 'images/CT_dataman.png',
    'Other clinical trials': 'images/CT_oth.png'
}

africa_icon = 'images/africa-wh-icon.png'
manu_icon = 'images/MANU.png'
reg_icon = 'images/REG.png'
CT_icon = 'images/CT.png'

def get_icons(items, icon_dict, var):
    icons = []
    if isinstance(items,str):
        if ';' in items:
            split_items = items.split(';')
            #print('; GROUP - Items: '+items+"-- "+str(split_items))
        elif ',' in items: 
            split_items = items.split(',')
            #print(', GROUP - Items: '+items+"-- "+str(split_items))
        else:
            split_items = [items]
            #print('NO SPLIT GROUP - Items: '+items+"-- "+str(split_items))

            
        for item in split_items:
            item = item.strip()
            if item in icon_dict:
                img_path = icon_dict[item]
                img_base64 = img_to_base64(img_path)
                if img_base64 == '':
                    print(f"Image file not found: {img_path}")
                if var == 'type':
                    icons.append(f'<img src="data:image/png;base64,{img_base64}" style="width: 30px; height: 30px; margin-right: 5px;">')
                    #print('Appended theme icon - ' +str(item))
                else:
                    icons.append(f'<img src="data:image/png;base64,{img_base64}" style="width: 125px; height: 125px; margin-right: 5px;">')
                    #print('Appended non-theme icon - ' +str(item))
            else:
                print(f"Var = {var}; Item not found in dictionary: {item}")
        
        #print("returning joint icons")
        return '     '.join(icons)
    else:
        return ""

def get_pie_icons(item, icon_dict):
    if isinstance(item,str):
        if item in icon_dict:
            img_path = icon_dict[item]
            img_base64 = img_to_base64(img_path)
            if img_base64 == '':
                    print(f"Image file not found: {img_path}")
            else:
                return f'<img src="data:image/png;base64,{img_base64}" style="width: 25px; height: 25px; margin-right: 5px; vertical-align: middle;">'
        else:
            print(f"Error: {item} not found in icon dictionary")
    else:
        return ""

# Convert data to DataFrame
df = pd.DataFrame(data)

def format_number(value):
    if value >= 1_000_000_000:
        return f"${value / 1_000_000_000:.2f} billion"
    elif value >= 1_000_000:
        return f"${value / 1_000_000:.2f} million"
    elif value >= 1_000:
        return f"${value / 1_000:.2f} thousand"        
    elif value >= 1:
        return f"${value:,}"
    else:
        return ""

def add_money_icon(value):
    if value >= 1:
        return '💰'
    else:
        return ''
    
#df['USD_display'] = df['amntUSD'].apply(lambda x: f"${x/1000000000:.2f} billion USD" if x > 1000000000 else (
#                                        f"${x/1000000:.2f} million USD" if x > 1000000 else (
#                                        f"${x/1000:.2f} thousand USD" if x > 1000 else "")))

if 'amntUSD' in df.columns:
    data_type = df['amntUSD'].dtypes
    print(f"The data type of 'amntUSD' column is: {data_type}") 
    
    df['amntUSD'] = df['amntUSD'].fillna(0)
    total_money_pledged = df['amntUSD'].sum()
else:
    print("The DataFrame does not have a column named 'amntUSD'.")

    
total_money_pledged = df['amntUSD'].sum()
df['header'] = "DETAILS"

# Custom CSS and JavaScript for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Aptos:wght@400;600&display=swap');
    
    body {
        font-family: 'Aptos', sans-serif;
        background-color: #f7f7f7;
    }
    .link_button {
        background-color: #ee6c4d;
    }
    .chart-box {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
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
    .commitment-subheader {
        display: flex;
        background-color: #3d5a80;
        color: #e8eaeb;
        padding: 0px;
        margin-left: 15px
        margin-right: 15px
    }
    .commitment-subheader-left {
        flex: 2;
        margin-right: 5px;
        padding: 5px;
    }
    .commitment-subheader-middle {
        flex: 3;
        padding: 5px;
        margin-left: 30px
    }
    .commitment-subheader-right {
        flex: 1;
        padding: 5px;
        margin-right: 10px
    }
    .commitment-title {
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .commitment-date {
        font-size: 0.9em;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    .commitment-maker-type {
        font-size: 0.9em;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    .under-titles {
        font-size: 0.9em;
        letter-spacing: 3px;
        text-transform: uppercase;
    }
    .geog-titles {
        font-size: 0.75em;
        letter-spacing: 2px;
        text-transform: uppercase;
        flex-wrap: wrap;
        text-align: center;
        margin-bottom: 0px;
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
        text-align: center;
        display: flex;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
    }
    .type-icon-item {
        gap: 10px;
    }
    .info-icon {
        margin-right: 10px;
        margin-left: 10px;
        color: #ee6c4d;
    }
     .theme-icon {
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
        background-color: #ee6c4d !important;
        color: white !important;
        border: none !important;
        border-radius: 5px !important;
        padding: 10px !important;
        margin-bottom: 15px !important;
        font-size: 18px !important;
    }
    .line {
        width: 75%;
        height: 2px;
        background-color: white;
        font-weight: bold;
    }
    .big-number {
        font-size: 6em;
        text-align: center;
    }
    .chart-container {
        padding: 20px !important;
        margin: 20px !important;
    }
    .pie-chart-container {
        padding: 50px !important;
        margin-left: 100px !important;
        margin-right: 100px !important;
    }
    .submit-button {
        background-color: #ee6c4d;
        color: white;
        padding: 10px 15px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        border-radius: 5px;
        margin-top: 10px;
    }
    .pie-chart-title {
        text-align: center;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Streamlit app
st.title("R&D Commitments Tracker")

typelist = ['Financial', 'Political', 'In-kind']
themelist = ['Manufacturing','Regulatory', 'Clinical trials']
stlist = pd.concat([df['st1'], df['st2'], df['st3']]).dropna().unique().tolist()
if len(stlist) == 1:
    stlist = [stlist[0]]
    
entTypelist = df['entityType'].dropna().unique().tolist()
if len(entTypelist) == 1:
    entTypelist = [entTypelist[0]]

entlist = df['entity'].dropna().unique().tolist()
if len(entlist) == 1:
    entlist = [entlist[0]]
    
# Sidebar for filters
st.sidebar.title("Filter Commitments")
selected_type = st.sidebar.selectbox("Type of Commitment", ["All"] + typelist)
selected_theme = st.sidebar.selectbox("Theme", ["All"] + themelist)
selected_subtheme = st.sidebar.selectbox("Subtheme Area", ["All"] + stlist)
selected_entityType = st.sidebar.selectbox("Type of entity making commitment", ["All"] + entTypelist)
selected_entity = st.sidebar.selectbox("Entity making commitment", ["All"] + entlist)
search_query = st.sidebar.text_input("Search", "")

# Filter data based on sidebar inputs
filtered_df = df.copy()

if search_query:
    filtered_df = filtered_df[
        filtered_df['commName'].str.contains(search_query, case=False, na=False) |
        filtered_df['details'].str.contains(search_query, case=False, na=False)
    ]

if selected_type != "All":
    filtered_df = filtered_df[filtered_df['type'].str.contains(selected_type, case=False, na=False)]

if selected_theme != "All":
    filtered_df = filtered_df[filtered_df['themes'].str.contains(selected_theme, case=False, na=False)]

if selected_subtheme != "All":
    filtered_df = filtered_df[filtered_df['subthemes'].str.contains(selected_subtheme, case=False, na=False)]

if selected_entityType != "All":
    filtered_df = filtered_df[filtered_df['entityType'].str.contains(selected_entityType, case=False, na=False)]

if selected_entity != "All":
    filtered_df = filtered_df[filtered_df['entity'].str.contains(selected_entity, case=False, na=False)]
    
# Display overall count of filtered commitments
st.sidebar.divider()
st.sidebar.header(f"Number of commitments: {len(filtered_df)}")

# Pie charts for commitments
type_counts = [filtered_df['type'].str.contains(t, case=False, na=False).sum() for t in typelist]
theme_counts = [filtered_df['themes'].str.contains(t, case=False, na=False).sum() for t in themelist]
entType_counts = [filtered_df['entityType'].str.contains(t, case=False, na=False).sum() for t in entTypelist]

type_counts_df = pd.DataFrame({'Type': typelist, 'Number of commitments': type_counts})
theme_counts_df = pd.DataFrame({'Theme': themelist, 'Number of commitments': theme_counts})
entType_counts_df = pd.DataFrame({'Type of entity making commitment': entTypelist, 'Number of commitments': entType_counts})

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

# Display layout
with st.container():
    st.markdown(f"""
        <div class="details-content"> 
            <div class='under-titles'> ABOUT THIS DASHBOARD: <br></div>
                <p> Using this tool, you can explore information about commitments made by governments and private entities 
                worldwide to <strong>improving the end-to-end R&D ecosystem in Africa.</strong> 
                On the left side of the page, you can filter by: 
                * <strong>type of commitment</strong> (financial, political, or in-kind); 
                * <strong>broad topic theme(s) that the commitment focuses on</strong> (manufacturing, regulations, or clinical trials); 
                * <strong>a more specific list of detailed theme areas</strong>; and 
                * the <strong>entity who made the commitment</strong>.
                * You can also search all the commitments. </p>
                <p>Scroll down for the full list of commitments. Click on "DETAILS" under each commitment to see more information. </p>
        </div>
                """, unsafe_allow_html=True)
    st.link_button('SUBMIT INFORMATION ON A COMMITMENT', 'https://www.path.org', 
                   help='Help us keep this tracker up-to-date by letting us know about a new commitment not already included.', 
                   type="secondary", disabled=False, use_container_width=True)

# Plotting the charts
fig_map = px.choropleth(
    africa,
    geojson=africa.geometry,
    locations=africa.index,
    color='Number of commitments relevant',
    hover_name='name',
    color_continuous_scale='Blues',
    hover_data={'Number of commitments relevant': True},
)
fig_map.update_layout(
    coloraxis_showscale=False, 
    showlegend=False, 
    margin={"r":0,"t":0,"l":0,"b":0},
    height=600,  # Increase the height to fill the container
)
fig_map.update_geos(
    fitbounds="locations", 
    visible=False, 
    projection_type="mercator", 
)
fig_map.update_traces(
    hovertemplate="Country: %{hovertext}<br>Number of commitments that impact this country: %{z}"
)

fig_type = px.pie(type_counts_df, names='Type', values='Number of commitments', color='Type', 
                color_discrete_map={'Financial': '#1EAF5F', 'Political': '#ED7D31', 'In-kind': '#464F60'},
                hole=0.2)  # Add hole parameter for donut chart

fig_theme = px.pie(theme_counts_df, names='Theme', values='Number of commitments', color='Theme',
                color_discrete_map={'Manufacturing': '#37379C', 'Regulatory': '#A8001E', 'Clinical trials': '008C9B'},
                hole=0.2)  # Add hole parameter for donut chart

fig_entType = px.pie(entType_counts_df, names='Type of entity making commitment', values='Number of commitments', color='Type of entity making commitment',
                     hole=0.2)  # Add hole parameter for donut chart

fig_type.update_traces(textposition='inside', textinfo='label+percent')
#fig_type.for_each_trace(lambda t: t.update(text=[f"{get_pie_icons(label,icons_pies)}{label}" for label in t.labels]))

fig_theme.update_traces(textposition='inside', textinfo='label+percent')
#fig_theme.for_each_trace(lambda t: t.update(text=[f"{get_pie_icons(label,icons_pies)}{label}" for label in t.labels]))

fig_entType.update_traces(textposition='inside', textinfo='label+percent')

fig_type.update_layout(showlegend=False)
fig_theme.update_layout(showlegend=False)
fig_entType.update_layout(showlegend=False)

fig_money = px.bar(
    x=[total_money_pledged, filtered_money_pledged],
    y=['Total pledged', 'Amount pledged (with filters)'],
    orientation='h',
    color=['Total money pledged', 'Amount pledged (with filters)'],
    color_discrete_map={'Total money pledged': '#056E23', 'Amount pledged (with filters)': '#1EAF5F'}
)

fig_money.update_traces(
    texttemplate="%{y}: $%{x:.2f}",
    #text=[f'Total money pledged: ${format_number(total_money_pledged)}',
    #      f'Money pledged (after filters applied): ${format_number(filtered_money_pledged)}'],
    textposition='inside'
    )

fig_money.update_layout(
    bargap=0.2,
    margin=dict(l=20, r=20, t=20, b=20),
    height=200,
    showlegend=False,
    xaxis_title=None,
    yaxis_title=None,
    yaxis=dict(showticklabels=False)
)

l1_left_col, l1_right_col = st.columns([3,2])
with l1_left_col:
        with st.container():
            #st.markdown('<div class="chart-box">', unsafe_allow_html=True)
            st.markdown('<div class="under-titles"> COUNTRIES: </div>', unsafe_allow_html=True)
            st.plotly_chart(fig_map, use_container_width=True)
            #st.markdown('</div>', unsafe_allow_html=True)


with l1_right_col:
    #st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    with st.container():
        st.markdown(f"""
             <div class="commitment-header">
                <div class='under-titles'> NUMBER OF COMMITMENTS LOGGED: <br></div><div class='big-number'>{total_commitments}<br></div>
            </div>
            <p></p>
            <div class='under-titles'> <br>FUNDING COMMITTED: </div>
            """, unsafe_allow_html=True)
        st.plotly_chart(fig_money, use_container_width=True, container_props={"className": "chart-container"})
        #st.markdown('</div>', unsafe_allow_html=True)

l2_left_col, l2_mid_col, l2_right_col = st.columns([1, 1, 1])
with l2_left_col:
    #st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown(f"<div class='pie-chart-title under-titles'> COMMITMENT TYPES: </div>", unsafe_allow_html=True)
    st.plotly_chart(fig_type, use_container_width=True, container_props={"className": "pie-chart-container"})
    #st.markdown('</div>', unsafe_allow_html=True)
        
with l2_mid_col:
    #st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown(f"<div class='pie-chart-title under-titles'> COMMITMENT THEMES: </div>", unsafe_allow_html=True)
    st.plotly_chart(fig_theme, use_container_width=True, container_props={"className": "pie-chart-container"})
   # st.markdown('</div>', unsafe_allow_html=True)

with l2_right_col:
    #st.markdown('<div class="chart-box">', unsafe_allow_html=True)
    st.markdown(f"<div class='pie-chart-title under-titles'> ENTITIES MAKING COMMITMENTS: </div>", unsafe_allow_html=True)
    st.plotly_chart(fig_entType, use_container_width=True, container_props={"className": "pie-chart-container"})
    #st.markdown('</div>', unsafe_allow_html=True)

# Divider
st.markdown("---")

# Display commitments
st.subheader("List of commitments:")

if len(filtered_df)<1:
    st.text("No commitments match the filter criteria.")
    
# Display commitments
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
        <div class="commitment-subheader">
            <div class="commitment-subheader-left">
                <div class="info-item">
                    <div class="info-subitem">
                        <span class="info-icon">{get_icons(row['type'], type_icons,'type')}</span>
                        <div class="geog-titles" style="display: flex; align-items: center;"> {row['type']}</div>
                    </div>
                </div>
            </div>
            <div class="commitment-subheader-middle">
                <div class="info-item">
                    <div class="info-subitem">
                        <img src="data:image/png;base64,{img_to_base64(africa_icon)}" style="width: 30px; height: 30px; margin-right: 10px;">
                        <div class="geog-titles" style="display: flex; align-items: center;"> {row['geography']} </div>
                    </div>
                </div>
            </div>  
            <div class="commitment-subheader-right">
                <div class="info-item">
                    <div class="info-subitem">
                        <span class="info-icon">{add_money_icon(row['amntUSD'])}</span>
                        <div class="geog-titles"> {format_number(row['amntUSD'])}</div>
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    if pd.isna(row['upd']):
        row['upd'] = 'None'
        
    with st.expander(f"DETAILS"):
        st.markdown(f"""
        <div class="commitment-card">
            <div class="commitment-info">
                <div class="info-item">
                    <div class="info-subitem">
                        <div class="under-titles"> THEME(S): </div> 
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-subitem">
                        <div class="under-titles"> SUBTHEME(S): </div> 
                    </div>
                </div>
                <div class="info-item"></div>
                <div class="info-item"></div>
                <div class="info-item">
                    <div class="info-subitem">
                        <span class="info-icon">{get_icons(row['themes'], theme_icons,'themes')}</span>
                    </div>
                </div>
                <div class="info-item">
                    <div class="info-subitem">
                        <span class="info-icon">{get_icons(row.get('subthemes',), subtheme_icons, 'subthemes')}</span> 
                    </div>
                </div>
            </div>
            <div class="details-header">DESCRIPTION</div>
            <div class="details-content">
                <p>{row.get('details',)}</p>
                <p><strong>OTHER PARTNERS INVOLVED:</strong> {row.get('partners', 'N/A')}</p>
                <p><strong>UPDATES:</strong> {row['upd']}</p>
                <p><strong>SOURCE:</strong> <a href="{row['link']}" target="_blank">{row['src']}</a></p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.link_button('SUBMIT AN UPDATE', 'https://www.path.org', help=None, type="primary", disabled=False, use_container_width=True)
