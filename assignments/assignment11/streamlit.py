import streamlit as st
import pandas as pd
import pydeck as pdk

df = pd.read_csv(
    '/home/nopparuj/chula/2110446/assignments/assignment11/RainDaily_Tabular.csv')

province = st.sidebar.selectbox(
    'Select Province',
    ['All'] + list(df['province'].unique()))
date = st.sidebar.selectbox(
    'Select Date',
    ['All'] + list(df['date'].unique()))


filtered_df = df
if province != 'All':
    filtered_df = filtered_df[filtered_df['province'] == province]
if date != 'All':
    filtered_df = filtered_df[filtered_df['date'] == date]

# Bar chart
st.subheader('Bar Chart: Average Rainfall by Area')
bar_chart_data = filtered_df.groupby('province')['rain'].mean()
st.bar_chart(bar_chart_data)

# Line chart
st.subheader('Line Chart: Average Rainfall over Time')
line_chart_data = filtered_df.groupby('date')['rain'].mean()
st.line_chart(line_chart_data)


def create_map(dataframe):
    layer = pdk.Layer(
        "ScatterplotLayer",
        dataframe,
        get_position=["longitude", "latitude"],
        get_color=[255, 0, 0],
        get_radius="rain",
        radius_scale=100,
        opacity=0.5,
        pickable=True
    )

    view_state = pdk.ViewState(
        longitude=dataframe['longitude'].mean(),
        latitude=dataframe['latitude'].mean(),
        zoom=5
    )

    return pdk.Deck(layers=[layer], initial_view_state=view_state)


st.subheader('Map: Rainfall by Area')
st.pydeck_chart(create_map(filtered_df))

st.subheader('Summary Analysis')
if len(filtered_df) > 0:
    summary_stats = filtered_df.describe().transpose()
    st.write(summary_stats)
else:
    st.write("No data available for the selected province and date range.")

st.subheader('Show Code')
with st.expander("Click to view code"):
    with open(__file__) as f:
        code = f.read()
    st.code(code, language='python')
