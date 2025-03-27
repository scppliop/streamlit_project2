import streamlit as st
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
import seaborn as sns
import altair as alt

st.title("Welcome to Raincouver!")

background_image_url ='./rain.jpg'
st.image(background_image_url)

st.markdown(
    f"""
    <style>
        /* button */
        div.stButton > button {{
            width: 200px;
            height: 60px;
            font-size: 20px;
            font-weight: bold;
            background-color: #008CBA;
            color: white;
            border-radius: 10px;
        }}
    </style>
    """,
    unsafe_allow_html=True
)


if "button_clicked" not in st.session_state:
    st.session_state.button_clicked = False


if st.button("Click the Button"):
    st.session_state.button_clicked = True


if st.session_state.button_clicked:

    
    
    data = pd.read_csv('weatherstats_vancouver(2024_2015).csv')
    
    #try a subheader
    st.subheader('How much rain does Vancouver get?')

    st.sidebar.header("Filter Options")
    selected_category = st.sidebar.selectbox(
        "Select Category", 
        options=["All", "Rain", "Snow", "Rain,Snow", "Normal"], 
        key="category_select"
    )
    
    #streamlit scatter chart
    if selected_category !='All':
        #filter the data according to selected category
        filtered_data = data[data['weather']== selected_category]
    else:
        filtered_data = data
    
    grouped_data = filtered_data.groupby(['year', 'weather']).size().reset_index(name='count')
    st.write("Vancouver is a city with a lot of rainfall, often referred to as 'Raincouver' In this analysis, we focused on examining Vancouver's weather with an emphasis on rain using weather data.")
    
    
    st.subheader('The total number of Rainy/Snowing/Normal days over the past 10 years (2015-2024)')
    alt_chart = alt.Chart(grouped_data).mark_bar(size=30).encode(#mark_bar : bar chart encode : How to visualize the data(x,y,z)
        x='year',
        y='count', 
        color=alt.Color('weather', scale=alt.Scale(domain=['Rain','Snow','Rain,Snow','Normal'], range=['blue', 'skyblue', 'red','green'])),  
    ).properties(
        title='Weather Data by Year'
    )
    
    
    st.altair_chart(alt_chart)

    st.markdown("""
- From 2015 to 2024, the proportion of precipitation (rain and snow) and normal weather (green) has remained relatively stable each year.
- It appears that there are approximately 150 to 200 rainy days per year, maintaining a consistent level.
- Snowy days (gray) are rarely observed, and days with both rain and snow (red) are also very few.
- The consistent ratio of precipitation (rain + snow) and normal weather suggests that this region is likely not experiencing significant climate changes.
""")
    
    
    
    cloud_cover_range = st.slider(
        'Select cloud cover range (0-8)', 
        min_value=0, 
        max_value=8, 
        value=(0, 8)
    )
    
    filtered_data = data[
        (data['avg_cloud_cover_8'] >= cloud_cover_range[0]) & 
        (data['avg_cloud_cover_8'] <= cloud_cover_range[1])
    ]
    
    
    st.subheader('Correlation between humidity and temperature by 2024')
    st.scatter_chart(filtered_data, x='avg_temperature', y='avg_relative_humidity', color='avg_cloud_cover_8', x_label='Temperature', y_label='Humidity')
    
    

    st.markdown("""
- A negative correlation is observed between temperature and humidity.
- As the temperature increases, humidity tends to decrease, while lower temperatures are associated with higher humidity.
- In general, days with higher humidity also tend to have greater cloud cover.
- Data points with high cloud cover (darker dots) are primarily concentrated in lower temperature ranges.
- Conversely, in higher temperature ranges, there are more data points with lower cloud cover (lighter dots).
- This suggests that cloudy days may have a cooling effect on temperature.
""")


    
    st.subheader('Correlation between precipitation and temperature by 2024')
    st.scatter_chart(data,x='avg_temperature',y='precipitation',color='cloudy', x_label = 'Temperature', y_label='Precipitation')
    
    
    st.markdown("""
- The highest amount of precipitation appears to be recorded in the 10–15°C range.
- There are many data points with high precipitation in the 5–10°C range, suggesting that rainy days were frequent in this temperature range.
- The correlation between precipitation and temperature does not show a clear linear relationship but rather a pattern where precipitation is concentrated within specific temperature ranges.
- When the temperature is low or above 20°C, precipitation tends to be minimal.
""")
    
    
    
    
    
    
    
    st.subheader('The Weather Status of Vancouver')
    
    
    
    selected_data = data[data['year'] == 2024]
    
    cloudy_counts = selected_data['cloudy'].value_counts().reset_index()
    cloudy_counts.columns = ['cloudy', 'count']
    
    
    colors = ['#B0B0B0', '#1F5D91', '#2A8FC4', '#5FA3D3', '#F8E38C']
    
    
    fig = px.pie(cloudy_counts, names='cloudy', values='count',  title='Cloudy Distribution for 2024',color='cloudy',
                 color_discrete_sequence=colors)
    
    fig.update_layout(autosize=True,height=600,width=600)
    
    st.plotly_chart(fig)
    

    st.markdown("""
- The total proportion of cloudy days (Scattered, Broken, Overcast) was approximately 86.1%, indicating that Vancouver experienced mostly cloudy weather in 2024.
- Completely overcast days (Overcast) and days with significant cloud cover but some clear patches (Broken) accounted for a considerable portion, with Scattered clouds being the most frequently observed condition.
- The combined percentage of Clear (5.46%) and Few (8.47%) was only about 13.93%, meaning that fully clear or nearly cloudless days were relatively rare overall.
""")
    
    
    
    
    #heatmap
    st.subheader('2024 Monthly Daily Precipitation Heatmap')
    
    
    df = selected_data.pivot_table(index='day', columns='month', values='precipitation', aggfunc='sum')
    
    
    custom_colorscale = [[0, 'lightyellow'],[0.0001, 'skyblue'],[1, 'darkblue']]
    
    # Plotly heatmap
    fig = px.imshow(df, color_continuous_scale=custom_colorscale, labels={'x': 'Month', 'y': 'Day', 'color': 'Precipitation'})
    
    fig.update_layout(width=1000, height=800)
    
    st.plotly_chart(fig)

    st.markdown("""
- The month with the least rainfall was July.
- Rainfall was higher in the mid to late part of the month than in the early days.
- Winter had more rainfall compared to summer.
""")



























