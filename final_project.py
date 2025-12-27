import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
import base64
# Image Configuration
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()
img_base64 = get_base64("imran.jpg")    
# Page configuration
st.set_page_config(layout="wide", page_title="World Happiness Dashboard")

st.markdown("""
    <style>
    div[data-baseweb="select"] > div {
        background-color: #0f172a;
        color: white;
    }
    div[data-baseweb="select"] > div:hover {
        background-color: #0f172a;
    }
    div[data-baseweb="select"] div[aria-selected="true"] {
        background-color: #0f172a;
    }
    </style>
""", unsafe_allow_html=True)

# CSS Configuration
st.markdown("""
    <style>
    .main {
        background-color: #1e3a8a;
        color: white;
    }
    .stSelectbox, .stMultiSelect {
        background-color: #1e40af;
    }
    .st-bw {
        background-color: #1e3a8a;
    }
    .st-emotion-cache-1y4p8pa {
        padding: 2rem 1rem;
    }
    .dataset-info {
        background-color: #1e3a8a;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .team-section {
        background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
        padding: 2rem;
        border-radius: 1rem;
        margin: 2rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .team-grid {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
        margin-top: 1.5rem;
    }
    .team-member {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 1rem;
        padding: 1.5rem;
        text-align: center;
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease;
        flex: 1;
        min-width: 250px;
        max-width: 300px;
    }
    .team-member:hover {
        transform: translateY(-5px);
    }
    .team-member img {
        width: 150px;
        height: 150px;
        border-radius: 50%;
        margin-bottom: 1rem;
        object-fit: cover;
        border: 3px solid #3b82f6;
    }
    .team-member h3 {
        color: #ffffff;
        margin-bottom: 0.5rem;
        font-size: 1.25rem;
    }
    .team-member p {
        color: #93c5fd;
        font-size: 0.875rem;
    }
    </style>
""", unsafe_allow_html=True)

# Disini untuk memuat dan menyiapkan data
@st.cache_data
def load_data():
    df = pd.read_csv("world-happiness-report-2021.csv")
    return df

# Disini fungsi untuk membuat link download
def get_table_download_link(df, filename, text):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="{filename}" class="download-button">{text}</a>'
    return href

data = load_data()

# Sidebar
with st.sidebar:
    st.image("fif-logo.png", width=500)
    st.title("World Happiness Analytics")
    
    # Deskripsi fakta menarik dalam sidebar
    st.subheader("For Your Information")
    st.markdown("""
    <div style="background-color: #0f172a; padding: 1.5rem; border-radius: 0.5rem; margin-bottom: 1rem; color: white;">
        <ul style="font-size: 1rem; margin-top: 1rem; line-height: 1.8;">
            <li>🌍 <strong>Happiest Country:</strong> Finlandia</li>
            <li>💰 <strong>Region with Highest GDP:</strong> North America</li>
            <li>🕒 <strong>Longest Life Expectancy:</strong> 76.5 Years</li>
            <li>😔 <strong>Unhappiest Country:</strong> Afghanistan</li>
            <li>🌟 <strong>Key Happiness Factor:</strong> Social Support</li>
        </ul>
    </div>
""", unsafe_allow_html=True)
    
     # Advanced Filters Section
    st.subheader("Advanced Filters")
    
    # Region filter
    selected_regions = st.multiselect(
        "Select Regions:",
        options=data["Regional indicator"].unique(),
        default=data["Regional indicator"].unique()
    )
    
   # GDP Range filter dengan tempat untuk input nya
    st.subheader("GDP Range")
    gdp_min = st.number_input("Min GDP", 
                             value=float(data["Logged GDP per capita"].min()),
                             step=0.1)
    gdp_max = st.number_input("Max GDP", 
                             value=float(data["Logged GDP per capita"].max()),
                             step=0.1)
    
    # Happiness Score Range dengan tempat untuk input nya
    st.subheader("Happiness Score Range")
    happiness_min = st.number_input("Min Score", 
                                  value=float(data["Ladder score"].min()),
                                  step=0.1)
    happiness_max = st.number_input("Max Score", 
                                  value=float(data["Ladder score"].max()),
                                  step=0.1)
    
    # Additional Filters
    show_top_n = st.slider("Show Top N Countries", 5, 20, 10)
    
    # Tombol untuk mengklik download
    st.markdown("### Download Data")
    st.markdown(get_table_download_link(data, "world_happiness_2021.csv", "Download Full Dataset"), 
               unsafe_allow_html=True)

# Filter data berdasarkan pilihan
filtered_data = data[
    (data["Regional indicator"].isin(selected_regions)) &
    (data["Logged GDP per capita"].between(gdp_min, gdp_max)) &
    (data["Ladder score"].between(happiness_min, happiness_max))
]

# Main content
st.markdown("""
    <div style='text-align: center;'>
        <h1 style='color: white; margin-bottom: 0.5rem;'>World Happiness Report 2021</h1>
        <div style='background-color: #1e40af; padding: 1rem; border-radius: 0.5rem; margin-bottom: 1rem;'>
            <h4 style='color: white; margin: 0;'>Last updated: {}</h4>
        </div>
    </div>
""".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

# Team Section
st.markdown(f"""
<div class="team-section">
    <h2 style="text-align:center;color:white;">Project Author</h2>
    <div style="text-align:center;">
        <img src="data:image/jpg;base64,{img_base64}"
             width="180"
             style="border-radius:12px;">
        <h3>Imran Zulkarnaen</h3>
        <p>203012420041</p>
        <p>Informatics Faculty Students</p>
        <p>Telkom University</p>
    </div>
</div>
""", unsafe_allow_html=True)


# Dataset Information Box
st.markdown("""
<div class="dataset-info">
    <h3 style='color: #ffffff; margin-bottom: 1rem;'>World Happiness Report Dataset</h3>
    <p style='color: #e2e8f0; margin-bottom: 1rem;'>
        This dataset comes from annual reports on happiness levels in various countries. 
        The data includes variables such as GDP per capita, social support, life expectancy, freedom, and levels of corruption.
    </p>
    <h4 style='color: #ffffff; margin-bottom: 0.5rem;'>Objectives of the analysis:</h4>
    <ul style='color: #e2e8f0; list-style-type: disc; margin-left: 1.5rem;'>
        <li>To help readers compare happiness levels across countries</li>
        <li>To explore factors that influence happiness</li>
        <li>To improve understanding of global quality of life</li>
        <li>To support data-driven decision-making</li>
        <li>To identify trends and patterns in global well-being</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Key metrics row
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Average Happiness",
        f"{filtered_data['Ladder score'].mean():.2f}",
        f"{filtered_data['Ladder score'].mean() - data['Ladder score'].mean():.2f}"
    )

with col2:
    st.metric(
        "Highest Score",
        f"{filtered_data['Ladder score'].max():.2f}",
        f"Top: {filtered_data.nlargest(1, 'Ladder score')['Country name'].iloc[0]}"
    )

with col3:
    st.metric(
        "Average GDP",
        f"{filtered_data['Logged GDP per capita'].mean():.2f}",
        f"{filtered_data['Logged GDP per capita'].mean() - data['Logged GDP per capita'].mean():.2f}"
    )

with col4:
    st.metric(
        "Social Support",
        f"{filtered_data['Social support'].mean():.2f}",
        f"{filtered_data['Social support'].mean() - data['Social support'].mean():.2f}"
    )

with col5:
    st.metric(
        "Life Expectancy",
        f"{filtered_data['Healthy life expectancy'].mean():.2f}",
        f"{filtered_data['Healthy life expectancy'].mean() - data['Healthy life expectancy'].mean():.2f}"
    )

# Membuat dua kolom untuk charts
st.subheader("Happiness Score vs GDP per Capita")

fig1 = px.scatter(
    filtered_data,
    x="Logged GDP per capita",
    y="Ladder score",
    size="Social support",
    color="Regional indicator",
    hover_name="Country name",
    size_max=20,
    template="plotly_dark"
)

fig1.update_layout(
    plot_bgcolor="#1e40af",
    paper_bgcolor="#0f172a",
    font_color="white"
)

st.plotly_chart(fig1, use_container_width=True)


st.subheader("Regional Happiness Distribution")

fig2 = px.box(
    filtered_data,
    x="Regional indicator",
    y="Ladder score",
    color="Regional indicator",
    template="plotly_dark"
)

fig2.update_layout(
    plot_bgcolor="#1e40af",
    paper_bgcolor="#0f172a",
    font_color="white",
    xaxis={'tickangle': 45}
)

st.plotly_chart(fig2, use_container_width=True)


# Correlation heatmap
st.subheader("Factors Affecting Happiness")
correlation_cols = [
    "Ladder score", "Logged GDP per capita", "Social support",
    "Healthy life expectancy", "Freedom to make life choices",
    "Generosity", "Perceptions of corruption"
]

correlation_matrix = filtered_data[correlation_cols].corr()

fig3 = px.imshow(
    correlation_matrix,
    template="plotly_dark",
    color_continuous_scale="RdBu"
)
fig3.update_layout(
    plot_bgcolor="#1e40af",
    paper_bgcolor="#0f172a",
    font_color="white"
)
st.plotly_chart(fig3, use_container_width=True)

 # Factor Analysis
st.subheader("Factor Contribution to Happiness")
factors = ["Social support", "Healthy life expectancy", 
            "Freedom to make life choices", "Generosity", 
            "Perceptions of corruption"]
    
fig4 = go.Figure()
for factor in factors:
    fig4.add_trace(go.Scatter(
        x=filtered_data["Ladder score"],
        y=filtered_data[factor],
        mode='markers',
        name=factor,
        text=filtered_data["Country name"]
    ))
    
fig4.update_layout(
    template="plotly_dark",
    plot_bgcolor="#1e40af",
    paper_bgcolor="#0f172a",
    font_color="white",
    title="Factors vs Happiness Score"
)
st.plotly_chart(fig4, use_container_width=True)

# Data table dengan search
st.subheader("Detailed Country Data")
search_term = st.text_input("Search for a country:")
if search_term:
    display_data = filtered_data[filtered_data['Country name'].str.contains(search_term, case=False)]
else:
    display_data = filtered_data

st.dataframe(
    display_data[["Country name", "Regional indicator", "Ladder score", 
                 "Logged GDP per capita", "Social support", "Healthy life expectancy"]],
    use_container_width=True
)

# Rankings
col1, col2 = st.columns(2)
    
with col1:
    st.subheader(f"Top {show_top_n} Happiest Countries")
    top_n = filtered_data.nlargest(show_top_n, "Ladder score")[
        ["Country name", "Ladder score", "Regional indicator"]
    ]
    st.dataframe(top_n, use_container_width=True)
        
    # Visualisasi untuk negara-negara teratas
    fig5 = px.bar(
        top_n,
        x="Country name",
        y="Ladder score",
        color="Regional indicator",
        template="plotly_dark"
    )
    fig5.update_layout(
        plot_bgcolor="#1e40af",
        paper_bgcolor="#0f172a",
        font_color="white",
        xaxis={'tickangle': 45}
    )
    st.plotly_chart(fig5, use_container_width=True)
    
with col2:
    st.subheader(f"Bottom {show_top_n} Countries")
    bottom_n = filtered_data.nsmallest(show_top_n, "Ladder score")[
        ["Country name", "Ladder score", "Regional indicator"]
    ]
    st.dataframe(bottom_n, use_container_width=True)
        
    # Visualisasi untuk negara-negara terbawah
    fig6 = px.bar(
        bottom_n,
        x="Country name",
        y="Ladder score",
        color="Regional indicator",
        template="plotly_dark"
    )
    fig6.update_layout(
        plot_bgcolor="#1e40af",
        paper_bgcolor="#0f172a",
        font_color="white",
        xaxis={'tickangle': 45}
    )
    st.plotly_chart(fig6, use_container_width=True)

 # Insights and Statistics
st.subheader("Key Insights")
    
    # Regional Analysis
regional_stats = filtered_data.groupby("Regional indicator")["Ladder score"].agg([
    "mean", "std", "min", "max", "count"
]).round(2)
    
st.write("Regional Statistics")
st.dataframe(regional_stats, use_container_width=True)
    
# GDP vs Happiness Analysis
gdp_correlation = filtered_data["Logged GDP per capita"].corr(filtered_data["Ladder score"])
st.markdown(f"""
    ### GDP and Happiness Correlation
    The correlation coefficient between GDP per capita and Happiness Score is: **{gdp_correlation:.2f}**
""")
    
# Factors Impact Analysis
factors = ["Social support", "Healthy life expectancy", 
            "Freedom to make life choices", "Generosity", 
            "Perceptions of corruption"]
    
correlations = []
for factor in factors:
    corr = filtered_data["Ladder score"].corr(filtered_data[factor])
    correlations.append({"Factor": factor, "Correlation": corr})
    
correlations_df = pd.DataFrame(correlations)
    
fig7 = px.bar(
    correlations_df,
    x="Factor",
    y="Correlation",
    title="Correlation of Factors with Happiness Score",
    text="Correlation",
    template="plotly_dark",
    color="Correlation",
    color_continuous_scale="RdBu"
)
fig7.update_layout(
    plot_bgcolor="#1e40af",
    paper_bgcolor="#0f172a",
    font_color="white",
    xaxis={"title": "Factors"},
    yaxis={"title": "Correlation Coefficient"}
)
st.plotly_chart(fig7, use_container_width=True)


# Footer dengan deskripsi variabel
st.markdown("""
    ---
    ### Variable Explanation
    - **Ladder score**: Country happiness score (0-10)
    - **GDP per capita**: Gross Domestic Product per capita (in log form)
    - **Social support**: Perceived level of social support
    - **Healthy life expectancy**: Average number of years a person is expected to live in good health
    - **Freedom**: Freedom to make life choices
    - **Generosity**: Level of generosity
    - **Corruption**: Perception of corruption
""")