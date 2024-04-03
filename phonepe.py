import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly.express as px
import requests
import json
from PIL import Image

# Dataframe_creation
# sql_connection
mydb = psycopg2.connect(host = "localhost",
                        user = "postgres",
                        port= 5432,
                        database = "phonepe_data",
                        password = "arjunsoman123"
                           )
cursor = mydb.cursor()

# aggregated_transaction df

cursor.execute("SELECT * FROM aggregated_transaction")
mydb.commit()
table1 = cursor.fetchall()

Aggre_transaction = pd.DataFrame(table1,columns = ("States","Years","Quarter","Transaction_type",
                                                   "Transaction_count","Transaction_amount"))

# aggregated_user df

cursor.execute("SELECT * FROM aggregated_user")
mydb.commit()
table2 = cursor.fetchall()

Aggre_user = pd.DataFrame(table2,columns = ("States","Years","Quarter","Brands",
                                                   "Transaction_count","Percentage"))

# map_transaction df

cursor.execute("SELECT * FROM map_transaction")
mydb.commit()
table3 = cursor.fetchall()

Map_transaction = pd.DataFrame(table3,columns = ("States","Years","Quarter","Districts",
                                                   "Transaction_count","Transaction_amount"))


# map_user df

cursor.execute("SELECT * FROM map_user")
mydb.commit()
table4 = cursor.fetchall()

Map_user = pd.DataFrame(table4,columns = ("States","Years","Quarter","Districts",
                                                   "RegisteredUsers","AppOpens"))

# top_transaction df

cursor.execute("SELECT * FROM top_transaction")
mydb.commit()
table5 = cursor.fetchall()

Top_transaction = pd.DataFrame(table5,columns = ("States","Years","Quarter","Pincodes",
                                                   "Transaction_count","Transaction_amount"))

# top_user df

cursor.execute("SELECT * FROM top_user")
mydb.commit()
table6 = cursor.fetchall()

Top_user = pd.DataFrame(table6,columns = ("States","Years","Quarter","Pincodes",
                                                   "RegisteredUsers"))



#Transaction_year_based
def Transaction_amount_count_Y(df, year):
    mydb = psycopg2.connect(host = "localhost",
                           user = "postgres",
                           port= 5432,
                           database = "phonepe_data",
                           password = "arjunsoman123"
                              )
    cursor = mydb.cursor()

   #plot_1
    query1 = f'''SELECT * FROM {df}
                WHERE years = {year}'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    tacy = pd.DataFrame(table_1,columns = ("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount"))

    query2 = f'''SELECT states,SUM(transaction_count) AS transaction_count,
                SUM(transaction_amount) AS transaction_amount
                FROM {df}
                WHERE years = {year}
                GROUP BY states;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    tacyg = pd.DataFrame(table_2,columns = ("States","Transaction_count","Transaction_amount"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x = "States", y = "Transaction_amount",title = f"{year} TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height = 650, width = 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x = "States", y = "Transaction_count",title = f"{year} TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height = 650, width = 600)
        st.plotly_chart(fig_count)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    states_name = []
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()
    col1,col2 = st.columns(2)
    with col1:

        fig_india_1 = px.choropleth(tacyg, geojson = data1, locations = "States",featureidkey="properties.ST_NM",
                                    color = "Transaction_amount",color_continuous_scale="Rainbow",
                                    range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                    hover_name="States", title = f"{year} TRANSACTION AMOUNT",fitbounds= "locations",
                                    height = 600, width = 600)
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth(tacyg, geojson = data1, locations = "States",featureidkey="properties.ST_NM",
                                    color = "Transaction_count",color_continuous_scale="Rainbow",
                                    range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                    hover_name="States", title = f"{year} TRANSACTION COUNT",fitbounds= "locations",
                                    height = 600, width = 600)
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)

    return tacy

#Map_Transaction_year_based
def Transaction_amount_count_YY(df, year):
    mydb = psycopg2.connect(host = "localhost",
                           user = "postgres",
                           port= 5432,
                           database = "phonepe_data",
                           password = "arjunsoman123"
                              )
    cursor = mydb.cursor()

   #plot_1
    query1 = f'''SELECT * FROM {df}
                WHERE years = {year}'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    tacy = pd.DataFrame(table_1,columns = ("States","Years","Quarter","Districts","Transaction_count","Transaction_amount"))

    query2 = f'''SELECT states,SUM(transaction_count) AS transaction_count,
                SUM(transaction_amount) AS transaction_amount
                FROM {df}
                WHERE years = {year}
                GROUP BY states;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    tacyg = pd.DataFrame(table_2,columns = ("States","Transaction_count","Transaction_amount"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x = "States", y = "Transaction_amount",title = f"{year} TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height = 650, width = 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count = px.bar(tacyg, x = "States", y = "Transaction_count",title = f"{year} TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height = 650, width = 600)
        st.plotly_chart(fig_count)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    states_name = []
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()
    col1,col2 = st.columns(2)
    with col1:

        fig_india_1 = px.choropleth(tacyg, geojson = data1, locations = "States",featureidkey="properties.ST_NM",
                                    color = "Transaction_amount",color_continuous_scale="Rainbow",
                                    range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                    hover_name="States", title = f"{year} TRANSACTION AMOUNT",fitbounds= "locations",
                                    height = 600, width = 600)
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2 = px.choropleth(tacyg, geojson = data1, locations = "States",featureidkey="properties.ST_NM",
                                    color = "Transaction_count",color_continuous_scale="Rainbow",
                                    range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                    hover_name="States", title = f"{year} TRANSACTION COUNT",fitbounds= "locations",
                                    height = 600, width = 600)
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)

    return tacy

#Top_Transaction_year_based
def Transaction_amount_count_YYY(df, year):
    mydb = psycopg2.connect(host = "localhost",
                           user = "postgres",
                           port= 5432,
                           database = "phonepe_data",
                           password = "arjunsoman123"
                              )
    cursor = mydb.cursor()

   #plot_1
    query1 = f'''SELECT * FROM {df}
                WHERE years = {year}'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    tacy = pd.DataFrame(table_1,columns = ("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount"))

    query2 = f'''SELECT states,SUM(transaction_count) AS transaction_count,
                SUM(transaction_amount) AS transaction_amount
                FROM {df}
                WHERE years = {year}
                GROUP BY states;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    tacyg = pd.DataFrame(table_2,columns = ("States","Transaction_count","Transaction_amount"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(tacyg, x = "States", y = "Transaction_amount",title = f"{year} TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height = 650, width = 600)
        st.plotly_chart(fig_amount)
    with col2:

        fig_count = px.bar(tacyg, x = "States", y = "Transaction_count",title = f"{year} TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height = 650, width = 600)
        st.plotly_chart(fig_count)

    url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response = requests.get(url)
    data1 = json.loads(response.content)
    states_name = []
    for feature in data1["features"]:
        states_name.append(feature["properties"]["ST_NM"])

    states_name.sort()
    col1,col2 = st.columns(2)
    with col1:

        fig_india_1 = px.choropleth(tacyg, geojson = data1, locations = "States",featureidkey="properties.ST_NM",
                                    color = "Transaction_amount",color_continuous_scale="Rainbow",
                                    range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                    hover_name="States", title = f"{year} TRANSACTION AMOUNT",fitbounds= "locations",
                                    height = 600, width = 600)
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2 = px.choropleth(tacyg, geojson = data1, locations = "States",featureidkey="properties.ST_NM",
                                    color = "Transaction_count",color_continuous_scale="Rainbow",
                                    range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                    hover_name="States", title = f"{year} TRANSACTION COUNT",fitbounds= "locations",
                                    height = 600, width = 600)
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)

    return tacy


def Transaction_amount_count_Y_Q(df, quarter):
    tacy = df[df["Quarter"]== quarter]
    tacy.reset_index(drop = True, inplace = True)
    
    tacyg = tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1, col2 = st.columns(2)
    with col1:

        fig_amount = px.bar(tacyg, x = "States", y = "Transaction_amount",title = f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height = 650, width = 600)
        st.plotly_chart(fig_amount)

    with col2:

        fig_count = px.bar(tacyg, x = "States", y = "Transaction_count",title = f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height = 650, width = 600)
        st.plotly_chart(fig_amount)

    col1, col2 = st.columns(2)
    with col1:

        url = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response = requests.get(url)
        data1 = json.loads(response.content)
        states_name = []
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1 = px.choropleth(tacyg, geojson = data1, locations = "States",featureidkey="properties.ST_NM",
                                    color = "Transaction_amount",color_continuous_scale="Rainbow",
                                    range_color=(tacyg["Transaction_amount"].min(),tacyg["Transaction_amount"].max()),
                                    hover_name="States", title = f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",fitbounds= "locations",
                                    height = 600, width = 600)
        fig_india_1.update_geos(visible = False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2 = px.choropleth(tacyg, geojson = data1, locations = "States",featureidkey="properties.ST_NM",
                                    color = "Transaction_count",color_continuous_scale="Rainbow",
                                    range_color=(tacyg["Transaction_count"].min(),tacyg["Transaction_count"].max()),
                                    hover_name="States", title = f"{tacy["Years"].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",fitbounds= "locations",
                                    height = 600, width = 600)
        fig_india_2.update_geos(visible = False)
        st.plotly_chart(fig_india_2)

    return tacy

def aggre_transaction_type(df, state):

    tacy = df[df["States"]== state]
    tacy.reset_index(drop = True, inplace = True)

    tacyg = tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1, col2= st.columns(2)
    
    with col1:

        fig_pie_1 = px.pie(data_frame= tacyg, names="Transaction_type", values = "Transaction_amount",
                        width = 600, title = f"{state.upper()} TRANSACTION AMOUNT", hole = 0.5 )
        st.plotly_chart(fig_pie_1)

    with col2:

        fig_pie_2 = px.pie(data_frame= tacyg, names="Transaction_type", values = "Transaction_count",
                        width = 600, title = f"{state.upper()} TRANSACTION COUNT", hole = 0.5 )
        st.plotly_chart(fig_pie_2) 

# Aggre_user_analysis_1
def aggre_user_plot_1(df, year):
    mydb = psycopg2.connect(host = "localhost",
                           user = "postgres",
                           port= 5432,
                           database = "phonepe_data",
                           password = "arjunsoman123"
                              )
    cursor = mydb.cursor()

   #plot_1
    query1 = f'''SELECT * FROM {df}
                WHERE years = {year}'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    aguy = pd.DataFrame(table_1,columns = ("States","Years","Quarter","Brands","Transaction_count","Percentage"))

    query2 = f'''SELECT brands,SUM(transaction_count) AS transaction_count
                FROM {df}
                WHERE years = {year}
                GROUP BY brands;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    aguyg = pd.DataFrame(table_2,columns = ("Brands","Transaction_count"))

    fig_bar_1 = px.bar(aguyg,x = "Brands", y = "Transaction_count",title = f"{year} BRANDS AND TRANSACTION COUNT",
                    width = 1000,color_discrete_sequence=px.colors.sequential.haline,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguy 

# Aggre_user_analysis_2
def aggre_user_plot_2(df, quarter):
    aguyq = df[df["Quarter"] == quarter]
    aguyq.reset_index(drop = True,inplace = True)

    aguyqg = pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace = True)

    fig_bar_1 = px.bar(aguyqg,x = "Brands", y = "Transaction_count",title = f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",
                        width = 1000,color_discrete_sequence=px.colors.sequential.Magenta_r,hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq


# Aggre_user_analysis_3
def aggre_user_plot_3(df, state):
    auyqs = df[df["States"] == state]
    auyqs.reset_index(drop = True, inplace = True)

    fig_line_1 = px.line(auyqs, x= "Brands", y = "Transaction_count",hover_data = "Percentage",
                        title = f"{state.upper()} BRANDS, TRANSACTION COUNT, PERCENTAGE",width= 1000, markers = True)
    st.plotly_chart(fig_line_1)

# Map_transaction_District
def map_tran_Districts(df, state):

    tacy = df[df["States"]== state]
    tacy.reset_index(drop = True, inplace = True)

    tacyg = tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace = True)

    col1,col2 = st.columns(2)
    with col1:

        fig_bar_1 = px.bar(tacyg,x = "Transaction_amount", y = "Districts", orientation="h",height = 600,
                        title = f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Mint_r)
        st.plotly_chart(fig_bar_1)
    
    with col2:

        fig_bar_2 = px.bar(tacyg,x = "Transaction_count", y = "Districts", orientation="h", height = 600,
                        title = f"{state.upper()} DISTRICT AND TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_bar_2)


# map_user_plot_1
def map_user_plot_1(df,year):
    mydb = psycopg2.connect(host = "localhost",
                           user = "postgres",
                           port= 5432,
                           database = "phonepe_data",
                           password = "arjunsoman123"
                              )
    cursor = mydb.cursor()

   #plot_1
    query1 = f'''SELECT * FROM {df}
                WHERE years = {year}'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    muy = pd.DataFrame(table_1,columns = ("States","Years","Quarter","Districts","RegisteredUsers","AppOpens"))

    query2 = f'''SELECT states,SUM(registeredusers) AS registeredusers
                FROM {df}
                WHERE years = {year}
                GROUP BY states;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    muyg = pd.DataFrame(table_2,columns = ("States","RegisteredUsers"))
    col1,col2 = st.columns(2)
    with col1:
        fig_line_1 = px.line(muyg, x= "States", y = ["RegisteredUsers"],
                            title = f"{year} REGISTEREDUSER",width= 1000,height= 800, markers = True)
        st.plotly_chart(fig_line_1)

    query3 = f'''SELECT states,SUM(appopens) AS appopens
                FROM {df}
                WHERE years = {year}
                GROUP BY states;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    muyg1 = pd.DataFrame(table_3,columns = ("States","AppOpens"))
    with col2:
        fig_line_2 = px.line(muyg1, x= "States", y = ["AppOpens"],
                            title = f"{year} APPOPENS",width= 1000,height= 800, markers = True)
        st.plotly_chart(fig_line_2)

    return muy

# map_user_plot_2
def map_user_plot_2(df,quarter):
    muyq = df[df["Quarter"] == quarter]
    muyq.reset_index(drop = True,inplace = True)

    muyqg = muyq.groupby("States")[["RegisteredUsers","AppOpens"]].sum()
    muyqg.reset_index(inplace = True)

    fig_line_1 = px.line(muyqg, x= "States", y = ["RegisteredUsers","AppOpens"],
                        title = f"{df['Years'].min()} YEAR {quarter} QUARTER REGISTEREDUSER, APPOPENS",width= 1000,height= 800, markers = True,
                        color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_line_1)

    return muyq

# map_user_plot_3
def map_user_plot_3(df, states):

    muyqs = df[df["States"] == states]
    muyqs.reset_index(drop = True,inplace = True)

    col1,col2 = st.columns(2)
    with col1:

        fig_map_user_bar_1=px.bar(muyqs,x = "RegisteredUsers", y = "Districts", orientation= "h",
                                title = f"{states.upper()} REGISTERED USER", height = 800, color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_bar_1)
    with col2: 

        fig_map_user_bar_2=px.bar(muyqs,x = "AppOpens", y = "Districts", orientation= "h",
                                title = f"{states.upper()} APPOPENS", height = 800, color_discrete_sequence=px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_bar_2)

# top_transaction_plot_1
def Top_transaction_plot_1(df, state):
    tty = df[df["States"] == state]
    tty.reset_index(drop= True, inplace = True)

    col1,col2 = st.columns(2)
    with col1:

        fig_top_tran_bar_1=px.bar(tty,x = "Quarter", y = "Transaction_amount",hover_data="Pincodes",
                                title = "TRANSACTION AMOUNT", height = 650,width = 600, color_discrete_sequence=px.colors.sequential.GnBu_r)
        st.plotly_chart(fig_top_tran_bar_1)

    with col2:

        fig_top_tran_bar_2=px.bar(tty,x = "Quarter", y = "Transaction_count",hover_data="Pincodes",
                                title = "TRANSACTION COUNT", height = 650,width= 600, color_discrete_sequence=px.colors.sequential.Emrld_r)
        st.plotly_chart(fig_top_tran_bar_2)

# top_user_plot
def top_user_plot_1(df, year):
    mydb = psycopg2.connect(host = "localhost",
                           user = "postgres",
                           port= 5432,
                           database = "phonepe_data",
                           password = "arjunsoman123"
                              )
    cursor = mydb.cursor()

   #plot_1
    query1 = f'''SELECT * FROM {df}
                WHERE years = {year}'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    tuy = pd.DataFrame(table_1,columns = ("States","Years","Quarter","Pincodes","RegisteredUsers"))

    query2 = f'''SELECT states,quarter,
                SUM(registeredusers) as registeredusers
                FROM {df}
                WHERE years = {year}
                GROUP BY states,quarter;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    tuyg = pd.DataFrame(table_2,columns = ("States","Quarter","RegisteredUsers"))

    fig_top_plot_1= px.bar(tuyg, x = "States",y = "RegisteredUsers", color = "Quarter",width = 1000, height = 800,
                        color_discrete_sequence=px.colors.sequential.Burgyl, hover_name= "States",
                        title= f"{year} REGISTERED USERS")
    st.plotly_chart(fig_top_plot_1)

    return tuy


# top_user_plot_2
def top_user_plot_2(df,state):
    tuys = df[df["States"] == state]
    tuys.reset_index(drop = True,inplace = True)

    fig_top_plot_2 = px.bar(tuys, x = "Quarter", y = "RegisteredUsers",title = "REGISTERED USERS,PINCODES,QUARTER",
                            width = 1000, height = 800, color = "RegisteredUsers", hover_data = "Pincodes",
                            color_continuous_scale=px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_2)


# sql_connection
def top_chart_transaction_amount(table_name):
    mydb = psycopg2.connect(host = "localhost",
                           user = "postgres",
                           port= 5432,
                           database = "phonepe_data",
                           password = "arjunsoman123"
                              )
    cursor = mydb.cursor()

   #plot_1
    query1 = f'''SELECT states,SUM(transaction_amount) AS transaction_amount
               FROM {table_name}
               GROUP BY states
               ORDER BY transaction_amount DESC
               LIMIT 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1,columns = ("states","transaction_amount"))
   
    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x = "states", y = "transaction_amount",title = "TOP 10 OF TRANSACTION AMOUNT", hover_name = "states",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl,height = 650, width = 600)
        st.plotly_chart(fig_amount)

   # plot_2
    query2 = f'''SELECT states,SUM(transaction_amount) AS transaction_amount
               FROM {table_name}
               GROUP BY states
               ORDER BY transaction_amount
               LIMIT 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2,columns = ("states","transaction_amount"))
    
    with col2:
        fig_amount_2 = px.bar(df_2, x = "states", y = "transaction_amount",title = "LAST 10 OF TRANSACTION AMOUNT", hover_name = "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height = 650, width = 600)
        st.plotly_chart(fig_amount_2)

   # plot_3
    query3 = f'''SELECT states,AVG(transaction_amount) as transaction_amount
               FROM {table_name}
               group by states
               order by transaction_amount'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3,columns = ("states","transaction_amount"))

    fig_amount_3 = px.bar(df_3, y = "states", x = "transaction_amount",title = "AVERAGE OF TRANSACTION AMOUNT", hover_name = "states",orientation="h",
                           color_discrete_sequence=px.colors.sequential.Bluered_r,height = 800, width = 1000)
    st.plotly_chart(fig_amount_3)


# sql_connection
def top_chart_transaction_count(table_name):
    mydb = psycopg2.connect(host = "localhost",
                           user = "postgres",
                           port= 5432,
                           database = "phonepe_data",
                           password = "arjunsoman123"
                              )
    cursor = mydb.cursor()

   #plot_1
    query1 = f'''SELECT states,SUM(transaction_count) AS transaction_count
               FROM {table_name}
               GROUP BY states
               ORDER BY transaction_count DESC
               LIMIT 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1,columns = ("states","transaction_count"))
    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x = "states", y = "transaction_count",title = "TOP 10 OF TRANSACTION COUNT", hover_name = "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl,height = 650, width = 600)
        st.plotly_chart(fig_amount)

    # plot_2
    query2 = f'''SELECT states,SUM(transaction_count) AS transaction_count
               FROM {table_name}
               GROUP BY states
               ORDER BY transaction_count
               LIMIT 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2,columns = ("states","transaction_count"))
    with col2:
    
        fig_amount_2 = px.bar(df_2, x = "states", y = "transaction_count",title = "LAST 10 OF TRANSACTION COUNT", hover_name = "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height = 650, width = 600)
        st.plotly_chart(fig_amount_2)

    # plot_3
    query3 = f'''SELECT states,AVG(transaction_count) as transaction_count
               FROM {table_name}
               group by states
               order by transaction_count'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3,columns = ("states","transaction_count"))

    fig_amount_3 = px.bar(df_3, y = "states", x = "transaction_count",title = "AVERAGE OF TRANSACTION COUNT", hover_name = "states",orientation="h",
                           color_discrete_sequence=px.colors.sequential.Bluered_r,height = 800, width = 1000)
    st.plotly_chart(fig_amount_3)


# top_chart_registered_user
def top_chart_registered_user(table_name, state):
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port= 5432,
                            database = "phonepe_data",
                            password = "arjunsoman123"
                                )
    cursor = mydb.cursor()

    #plot_1
    query1 = f'''SELECT districts,SUM(registeredusers) as registeredusers 
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts
                ORDER BY registeredusers DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1,columns = ("districts","registeredusers"))

    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x = "districts", y = "registeredusers",title = "TOP 10 OF REGISTERED USER", hover_name = "districts",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl,height = 650, width = 600)
        st.plotly_chart(fig_amount)

    # plot_2
    query2 = f'''SELECT districts,SUM(registeredusers) as registeredusers 
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts
                ORDER BY registeredusers
                LIMIT 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2,columns = ("districts","registeredusers"))

    with col2:
        fig_amount_2 = px.bar(df_2, x = "districts", y = "registeredusers",title = "LAST 10 OF REGISTERED USER", hover_name = "districts",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height = 650, width = 600)
        st.plotly_chart(fig_amount_2)

    # plot_3
    query3 = f'''SELECT districts,AVG(registeredusers) as registeredusers 
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts
                ORDER BY registeredusers;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3,columns = ("districts","registeredusers"))

    fig_amount_3 = px.bar(df_3, y = "districts", x = "registeredusers",title = "AVERAGE OF REGISTERED USER", hover_name = "districts",orientation="h",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height = 800, width = 1000)
    st.plotly_chart(fig_amount_3)

# top_chart_appopens
def top_chart_appopens(table_name, state):
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port= 5432,
                            database = "phonepe_data",
                            password = "arjunsoman123"
                                )
    cursor = mydb.cursor()

    #plot_1
    query1 = f'''SELECT districts,SUM(appopens) as appopens 
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1,columns = ("districts","appopens"))

    col1,col2= st.columns(2)
    with col1:

        fig_amount = px.bar(df_1, x = "districts", y = "appopens",title = "TOP 10 OF APPOPENS", hover_name = "districts",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl,height = 650, width = 600)
        st.plotly_chart(fig_amount)

    # plot_2
    query2 = f'''SELECT districts,SUM(appopens) as appopens 
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts
                ORDER BY appopens
                LIMIT 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2,columns = ("districts","appopens"))

    with col2:

        fig_amount_2 = px.bar(df_2, x = "districts", y = "appopens",title = "LAST 10 OF APPOPENS", hover_name = "districts",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height = 650, width = 600)
        st.plotly_chart(fig_amount_2)

    # plot_3
    query3 = f'''SELECT districts,AVG(appopens) as appopens 
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY districts
                ORDER BY appopens;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3,columns = ("districts","appopens"))

    fig_amount_3 = px.bar(df_3, y = "districts", x = "appopens",title = "AVERAGE OF APPOPENS", hover_name = "districts",orientation="h",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height = 800, width = 1000)
    st.plotly_chart(fig_amount_3)


# top_chart_registered_user
def top_chart_registered_users(table_name):
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port= 5432,
                            database = "phonepe_data",
                            password = "arjunsoman123"
                                )
    cursor = mydb.cursor()

    #plot_1
    query1 = f'''SELECT states,SUM(registeredusers) as registeredusers1
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers1 DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1,columns = ("states","registeredusers1"))
    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x = "states", y = "registeredusers1",title = "TOP 10 OF REGISTERED USER", hover_name = "states",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl,height = 650, width = 600)
        st.plotly_chart(fig_amount)

    # plot_2
    query2 = f'''SELECT states,SUM(registeredusers) as registeredusers1
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers1
                LIMIT 10;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2,columns = ("states","registeredusers1"))
    with col2:
        fig_amount_2 = px.bar(df_2, x = "states", y = "registeredusers1",title = "LAST 10 OF REGISTERED USER", hover_name = "states",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height = 650, width = 600)
        st.plotly_chart(fig_amount_2)

    # plot_3
    query3 = f'''SELECT states,AVG(registeredusers) as registeredusers1
                FROM {table_name}
                GROUP BY states
                ORDER BY registeredusers1;'''
    cursor.execute(query3)
    table_3 = cursor.fetchall()
    mydb.commit()

    df_3 = pd.DataFrame(table_3,columns = ("states","registeredusers1"))

    fig_amount_3 = px.bar(df_3, y = "states", x = "registeredusers1",title = "AVERAGE OF REGISTERED USER", hover_name = "states",orientation="h",
                            color_discrete_sequence=px.colors.sequential.Bluered_r,height = 800, width = 1000)
    st.plotly_chart(fig_amount_3)

# top_chart_brands
def top_chart_brands(table_name, state):
    mydb = psycopg2.connect(host = "localhost",
                            user = "postgres",
                            port= 5432,
                            database = "phonepe_data",
                            password = "arjunsoman123"
                                )
    cursor = mydb.cursor()

    #plot_1
    query1 = f'''SELECT brands,SUM(transaction_count) AS transaction_count
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY brands
                ORDER BY transaction_count DESC
                LIMIT 5;'''
    cursor.execute(query1)
    table_1 = cursor.fetchall()
    mydb.commit()

    df_1 = pd.DataFrame(table_1,columns = ("brands","transaction_count"))
    col1,col2 = st.columns(2)
    with col1:
        fig_amount = px.bar(df_1, x = "brands", y = "transaction_count",title = "TOP 5 OF BRANDS",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl,height = 650, width = 600)
        st.plotly_chart(fig_amount)

    # plot_2
    query2 = f'''SELECT brands,SUM(transaction_count) AS transaction_count
                FROM {table_name}
                WHERE states = '{state}'
                GROUP BY brands
                ORDER BY transaction_count
                LIMIT 5;'''
    cursor.execute(query2)
    table_2 = cursor.fetchall()
    mydb.commit()

    df_2 = pd.DataFrame(table_2,columns = ("brands","transaction_count"))
    with col2:
        fig_amount_2 = px.bar(df_2, x = "brands", y = "transaction_count",title = "LAST 5 OF BRANDS",
                                color_discrete_sequence=px.colors.sequential.Aggrnyl_r,height = 650, width = 600)
        st.plotly_chart(fig_amount_2)



# Streamlit part
st.set_page_config(layout = "wide")
st.title("PHONEPE DATA VISUALIZATION AND EXPLORATON")

with st.sidebar:
    select = option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select == "HOME":
    
    col1,col2 = st.columns(2)
    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("Phonepe is an Indian digital payments app and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit and Debit card linking****")
        st.write("****Bank Balance Check****")
        st.write("****Money Storage****")
        st.write("****Pin Authorization****")
        st.download_button("DOWNLOAD THE APP NOW","https://wwww.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\ADMIN\New folder\download.jfif"),width = 600)

    col3,col4 = st.columns(2)
    with col3:
        st.image(Image.open(r"C:\Users\ADMIN\New folder\download1.jfif"),width = 600)
    
    with col4:
        st.write("****Easy Transaction****")
        st.write("****One App For  All Your Payments****")
        st.write("****Your Bank Account is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****Phonepe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfefr and More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6 = st.columns(2)
    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up required****")
        st.write("****Pay Directly From Any Bank To Any Bank Account****")
        st.write("****Instantly & Free****")

    with col6:
        st.video(r"C:\Users\ADMIN\New folder\phonepead.mp4"
                 )
    


elif select == "DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis","Map Analysis","Top Analysis"])

    with tab1:
        
        method = st.radio("Select The Method",["Transaction Analysis","User Analysis"])

        if method == "Transaction Analysis":

            col1, col2 = st.columns(2)  
            with col1:   

                years = st.slider("Select The Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            tac_Y = Transaction_amount_count_Y("aggregated_transaction", years)

            col1, col2 = st.columns(2)
            with col1:

                states = st.selectbox("Select The State",tac_Y["States"].unique())

            aggre_transaction_type(tac_Y, states)

            col1, col2 = st.columns(2)  
            with col1:   

                quarters = st.slider("Select The Quarter",Aggre_transaction["Quarter"].min(),Aggre_transaction["Quarter"].max(),Aggre_transaction["Quarter"].min())
            tac_Y_Q = Transaction_amount_count_Y_Q(Aggre_transaction, quarters)

            col1, col2 = st.columns(2)
            with col1:

                states = st.selectbox("Select The State Ty",tac_Y_Q["States"].unique())

            aggre_transaction_type(tac_Y_Q, states)


        elif method == "User Analysis":
            
            col1, col2 = st.columns(2)  
            with col1:   

                years = st.slider("Select The Year au",Aggre_user["Years"].min(),Aggre_user["Years"].max(),Aggre_user["Years"].min())
            Aggre_user_Y = aggre_user_plot_1("aggregated_user", years)

            col1, col2 = st.columns(2)  
            with col1:   

                quarters = st.slider("Select The Quarter au",Aggre_user_Y["Quarter"].min(),Aggre_user_Y["Quarter"].max(),Aggre_user_Y["Quarter"].min())
            Aggre_user_Y_Q = aggre_user_plot_2(Aggre_user_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:

                states = st.selectbox("Select The State au",Aggre_user_Y_Q["States"].unique())

            aggre_user_plot_3(Aggre_user_Y_Q, states)





    with tab2:

        method_2 = st.radio("Select The Method",["Map Transaction","Map User"])

        if method_2 == "Map Transaction":
            
            col1, col2 = st.columns(2)  
            with col1:   

                years = st.slider("Select The Year mt",Map_transaction["Years"].min(),Map_transaction["Years"].max(),Map_transaction["Years"].min())
            map_tran_tac_Y = Transaction_amount_count_YY("map_transaction", years)

            col1, col2 = st.columns(2)
            with col1:
                states = st.selectbox("Select The State mt",map_tran_tac_Y["States"].unique())

            map_tran_Districts(map_tran_tac_Y, states)

            col1, col2 = st.columns(2)  
            with col1:   

                quarters = st.slider("Select The Quarter mt",map_tran_tac_Y["Quarter"].min(),map_tran_tac_Y["Quarter"].max(),map_tran_tac_Y["Quarter"].min())
            map_tran_tac_Y_Q = Transaction_amount_count_Y_Q(map_tran_tac_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:

                states = st.selectbox("Select The State mtt",map_tran_tac_Y_Q["States"].unique())

            map_tran_Districts(map_tran_tac_Y_Q, states)



        elif method_2 == "Map User":
            
            col1, col2 = st.columns(2)  
            with col1:   

                years = st.slider("Select The Year mu",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
            map_user_Y = map_user_plot_1("map_user", years)

            col1, col2 = st.columns(2)  
            with col1:   

                quarters = st.slider("Select The Quarter mut",map_user_Y["Quarter"].min(),map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
            map_user_Y_Q = map_user_plot_2(map_user_Y, quarters)

            col1, col2 = st.columns(2)
            with col1:

                states = st.selectbox("Select The State mut",map_user_Y_Q["States"].unique())

            map_user_plot_3(map_user_Y_Q, states)


    with tab3:

        method_3 = st.radio("Select The Method",["Top Transaction","Top User"])

        if method_3 == "Top Transaction":
            col1, col2 = st.columns(2)  
            with col1:   

                years = st.slider("Select The Year tt",Top_transaction["Years"].min(),Top_transaction["Years"].max(),Top_transaction["Years"].min())
            Top_tran_tac_Y = Transaction_amount_count_YYY("top_transaction", years)

            col1, col2 = st.columns(2)
            with col1:

                states = st.selectbox("Select The State tt",Top_tran_tac_Y["States"].unique())

            Top_transaction_plot_1(Top_tran_tac_Y, states)
            
            col1, col2 = st.columns(2)  
            with col1:   

                quarters = st.slider("Select The Quarter mu",Top_tran_tac_Y["Quarter"].min(),Top_tran_tac_Y["Quarter"].max(),Top_tran_tac_Y["Quarter"].min())
            Top_tran_tac_Y_Q = Transaction_amount_count_Y_Q(Top_tran_tac_Y, quarters)




        elif method_3 == "Top User":

            col1, col2 = st.columns(2)  
            with col1:   

                years = st.slider("Select The Year tu",Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())
            Top_user_Y = top_user_plot_1("top_user", years)

            col1, col2 = st.columns(2)
            with col1:

                states = st.selectbox("Select The State tu",Top_user_Y["States"].unique())

            top_user_plot_2(Top_user_Y, states)
               

elif select == "TOP CHARTS":
    question = st.selectbox("Select The Question",["1. Transaction Amount and count of Aggregated Transaction",
                                                   "2. Transaction Amount and count of Map Transaction",
                                                   "3. Transaction Amount and count of Top Transaction",
                                                   "4. Transaction count of Aggregated User",
                                                   "5. Registered Users of Map User",
                                                   "6. App opens of Map User",
                                                   "7. Registered Users of Top User",
                                                   "8. Brands of Aggregated User"
                                                  ])
    

    if question == "1. Transaction Amount and count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif question == "2. Transaction Amount and count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif question == "3. Transaction Amount and count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif question == "4. Transaction count of Aggregated User":
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif question == "5. Registered Users of Map User":
        
        states =st.selectbox("Select the State",Map_user["States"].unique())
        st.subheader("REGISTERED USER")
        top_chart_registered_user("map_user",states)

    elif question == "6. App opens of Map User":
        
        states =st.selectbox("Select the State",Map_user["States"].unique())
        st.subheader("APPOPENS")
        top_chart_appopens("map_user",states)

    elif question == "7. Registered Users of Top User":
        
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_user")

    
    elif question == "8. Brands of Aggregated User":
        
        states =st.selectbox("Select the State",Aggre_user["States"].unique())
        st.subheader("BRANDS")
        top_chart_brands("aggregated_user",states)

   