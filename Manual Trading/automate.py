import streamlit as st
from api import buyBook,buy
import pandas as pd
import matplotlib.pyplot as plt
from transform import transform
import time

def plot_custom_bar_chart(df, title):
    fig, ax = plt.subplots()
    ax.bar(df['X'], df['Y'], color="skyblue")
    ax.set_title(title)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.xticks(rotation=45, ha='right')
    
    for idx, row in df.iterrows():
        ax.text(row['X'], row['Y'], f"{row['X']}", ha='center', va='bottom')

    st.pyplot(fig)

st.title('PROBO YT')
selected_value = None

col1, col2 = st.columns(2)

if 'run' not in st.session_state:
    st.session_state.run = True

eventId = 3223536

while st.session_state.run:
    data_1 = transform(buyBook(eventId)['buyData'])
    data_2 = transform(buyBook(eventId)['sellData'])
    print("updating")
    df_1 = pd.DataFrame(list(data_1.items()), columns=['X', 'Y'])
    df_2 = pd.DataFrame(list(data_2.items()), columns=['X', 'Y'])

    with col1:
        st.write("YES")
        plot_custom_bar_chart(df_1, "Bar Chart for Data Set 1")

    with col2:
        try:
            st.write("NO")
            plot_custom_bar_chart(df_2, "Bar Chart for Data Set 2")
        except:
            st.write("SOLDOUT")

    nine_cols = st.columns(9)

    x = 1
    for nine_col in nine_cols :
        with nine_col :
            if st.button("Y " +str(x)):
                selected_value = x
                buy(eventId,float(selected_value),'yes')
            x += 1
    nine_cols = st.columns(9)

    x = 3
    for nine_col in nine_cols :
        with nine_col :
            if st.button("Y " +str(x/2)):
                selected_value = x/2
                buy(eventId,float(selected_value),'yes')
            x += 2

    second_nine_cols = st.columns(9)

    x = 1
    for nine_col in second_nine_cols :
        with nine_col :
            if st.button("N "+ str(x)):
                selected_value = x
                buy(eventId,float(selected_value),'no')
            x += 1

    second_nine_cols = st.columns(9)

    x = 3
    for nine_col in second_nine_cols :
        with nine_col :
            if st.button("N "+ str(x/2)):
                selected_value = x/2
                buy(eventId,float(selected_value),'no')
            x += 2
    time.sleep(0.1)
    st.experimental_rerun()

