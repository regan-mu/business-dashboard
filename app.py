import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit.components.v1 as components


st.set_page_config(layout="wide", initial_sidebar_state="expanded", page_icon="⚡", page_title='Deja Vu Stores Dashboard')
# set_page_config => https://github.com/streamlit/streamlit/issues/1770

path = "./data/dataonline.csv"
st.sidebar.header("DejaVu Stores")
data = st.sidebar.file_uploader("Upload Dataset", type=['csv'])

def load_data(dataframe):
    df = pd.read_csv(dataframe, encoding="ISO-8859-1", low_memory=False)
    df["Revenue"] = df["UnitPrice"] * df["Quantity"]
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    df["InvoiceMonth"] = df["InvoiceDate"].dt.month
    df["InvoiceYear"] = df["InvoiceDate"].dt.year
    return df

if data is not None:
    dt = load_data(data)
else:
    dt = load_data(path)

# Select box
menu = ["Business Snapshot", "Analysis", "About"]
selection = st.sidebar.selectbox("Key Performance Indicators ", menu)
st.sidebar.write('''Retail analytics is the process of providing analytical data on inventory levels, 
supply chain movement, consumer demand, sales, etc. ... The analytics on demand and supply data can be 
used for maintaining procurement level and also inform marketing strategies.''')

if selection == "Business Snapshot":
    st.subheader("Display Data")
    st.dataframe(dt.head())

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Monthly Revenue Overview")
        df_revenue = dt.groupby(["InvoiceMonth", "InvoiceYear"])["Revenue"].sum().reset_index()
        plt.figure(figsize=(15, 10))
        sns.barplot(x="InvoiceMonth", y="Revenue", hue="InvoiceYear", data=df_revenue)
        plt.title("Monthly Revenue")
        plt.xlabel("Month")
        plt.ylabel("Revenue")
        st.pyplot(plt)
    with col2:
        st.subheader("Monthly Items Sold Overview")
        df_quantity = dt.groupby(["InvoiceMonth", "InvoiceYear"])["Quantity"].sum().reset_index()
        plt.figure(figsize=(15, 10))
        sns.barplot(x="InvoiceMonth", y="Quantity", data=df_quantity)
        plt.title("Monthly Items Sold")
        plt.xlabel("Month")
        plt.ylabel("Items Sold")
        st.pyplot(plt)

    col3, col4 = st.columns(2)
    with col3:
        st.subheader("Monthly Active Customers")
        df_active = dt.groupby(["InvoiceMonth", "InvoiceYear"])["CustomerID"].nunique().reset_index()
        plt.figure(figsize=(15, 10))
        sns.barplot(x="InvoiceMonth", y="CustomerID", hue="InvoiceYear", data=df_active)
        plt.title("Monthly Active Users")
        plt.xlabel("Month")
        plt.ylabel("Active Users")
        st.pyplot(plt)

    with col4:
        st.subheader("Average Revenue per Month")
        df_revenue_avg = dt.groupby(["InvoiceMonth", "InvoiceYear"])["Revenue"].mean().reset_index()
        plt.figure(figsize=(15, 10))
        sns.barplot(x="InvoiceMonth", y="Revenue", data=df_revenue)
        plt.title("Monthly Average Revenue ")
        plt.xlabel("Month")
        plt.ylabel("Revenue")
        st.pyplot(plt)

    col5, col6 = st.columns(2)
    with col5:
        st.subheader("Best countries (Revenue)")
        df_sales = dt.groupby('Country').Revenue.sum().reset_index()
        df_sales.columns = ['Country', 'Sales']
        df_sales.sort_values(by='Sales', inplace=True, ascending=False)
        df_sales.reset_index(inplace=True, drop=True)
        top_5_sales = df_sales.iloc[:5]
        plt.figure(figsize=(15, 10))
        plt.pie(top_5_sales['Sales'],
                labels=top_5_sales['Country'],
                wedgeprops={'edgecolor': 'black'},
                startangle=90,
                radius=1.1,
                counterclock=False,
                autopct='%1.1f%%'
                )
        plt.title('Best performing Countries')
        st.pyplot(plt)

    with col6:
        st.subheader("Worst Countries (Revenue)")
        bottom_5_sales = df_sales.iloc[-5:]
        plt.figure(figsize=(15, 10))
        plt.pie(bottom_5_sales['Sales'],
                labels=bottom_5_sales['Country'],
                wedgeprops={'edgecolor': 'black'},
                startangle=90,
                radius=1.1,
                counterclock=False,
                autopct='%1.1f%%'
                )
        plt.title('Best performing Countries')
        st.pyplot(plt)

    # New vs Existing Users
    st.header("New vs Existing Users")
    df_first_purchase = dt.groupby(["CustomerID"])["InvoiceDate"].min().reset_index()
    df_first_purchase.columns = ["CustomerID", "FirstPurchaseDate"]
    dt = pd.merge(dt, df_first_purchase, on="CustomerID")
    dt["UserType"] = "New"
    dt.loc[dt["InvoiceDate"] > dt["FirstPurchaseDate"], "UserType"] = "Existing"

    dt.head()
    # New vs Existing User Revenue Analysis
    df_new_revenue = dt.groupby(["InvoiceMonth", "InvoiceYear", "UserType"])["Revenue"].sum().reset_index()
    plt.figure(figsize=(30, 20))
    sns.relplot(x="InvoiceMonth", y="Revenue", hue="UserType", data=df_new_revenue, kind="line", height=12,
                aspect=18 / 10)
    plt.title("New vs Existing Customer Revenue Overview")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    st.pyplot(plt)

elif selection == "Analysis":
    st.subheader("Display Data")
    st.table(dt.head())
    if st.checkbox("Show Shape"):
        st.write("Data Shape")
        st.write(f"{dt.shape[0]} Rows; {dt.shape[1]} Columns")
        st.markdown("Descriptive Stats")
        st.write(dt.describe())

footer_temp = """
<!-- CSS  -->
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
<link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0/css/materialize.min.css" 
type="text/css" rel="stylesheet" media="screen,projection"/>
<link href="static/css/style.css" type="text/css" rel="stylesheet" media="screen,projection"/>
<link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.5.0/css/all.css" 
integrity="sha384-B4dIYHKNBt8Bc12p+WXckhzcICo0wtJAoU8YZTY5qE0Id1GSseTk6S+L3BlXeVIU" crossorigin="anonymous">
<footer class="page-footer grey darken-4">
<div class="container" id="aboutapp">
<div class="row">
<div class="col l6 s12">
<h5 class="white-text">Retail Analysis App</h5>
<h6 class="grey-text text-lighten-4">This is Africa Data School Streamlit Class practical.</h6>
<p class="grey-text text-lighten-4">October 2022 Cohort</p>
</div>
<div class="col l3 s12">
<h5 class="white-text">Connect With Us</h5>
<ul>
<a href="https://www.facebook.com/AfricaDataSchool/" target="_blank" class="white-text">
<i class="fab fa-facebook fa-4x"></i>
</a>
<a href="https://www.linkedin.com/company/africa-data-school" target="_blank" class="white-text">
<i class="fab fa-linkedin fa-4x"></i>
</a>
<a href="https://www.youtube.com/watch?v=ZRdlQwNTJ7o" target="_blank" class="white-text">
<i class="fab fa-youtube-square fa-4x"></i>
</a>
<a href="https://github.com/Africa-Data-School" target="_blank" class="white-text">
<i class="fab fa-github-square fa-4x"></i>
</a>
</ul>
</div>
</div>
</div>
<div class="footer-copyright">
<div class="container">
Made by <a class="white-text text-lighten-3" href="https://africadataschool.com/">Regan </a><br/>
<a class="white-text text-lighten-3" href="https://africadataschool.com/"></a>
</div>
</div>
</footer>
"""

if selection == "About":
    st.header("About App")
    components.html(footer_temp, height=500)
