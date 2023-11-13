import pandas as pd
import streamlit as st
import plotly.express as px
from datetime import datetime
#visão empresa

    
def load_df():
    #Load the content from a .csv file located on my github
    url= 'https://github.com/RafaelSanglard/4POA/raw/main/Salary.csv'
    df_raw = pd.read_csv(url)
    df_raw.head()
    
    #Fcreate a copy for preserve the original cvs
    df = df_raw.copy()
    
    
 
    
    return df
    
def cleaning_df(df):
    #remove empty spaces from the string using .strip()
    df['Race'] = df['Race'].str.strip()
    df['Country'] = df['Country'].str.strip()
    df['Gender'] = df['Gender'].apply(str.strip)
    df['Job_Title'] = df['Job_Title'].apply(str.strip)
    df['Job_Title'] = df['Job_Title'].replace(r'\_', ' ', regex=True)
    
    columns_to_clean = ['Age', 'Race', 'Salary', 'Senior', 'Country','Gender','Job_Title','Education_Level','Years_of_Experience']
    
    for column in columns_to_clean:
        linhas_selecionadas = (df[column] != 'NaN')
        df = df.loc[linhas_selecionadas, :].copy()
    
    #Converting type, string to int/float
    df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce').astype('float')
    df['Senior'] = pd.to_numeric(df['Senior'], errors='coerce').astype('Int64')
    df['Education_Level'] = pd.to_numeric(df['Education_Level'], errors='coerce').astype('Int64')
    #df['Years_of_Experience'] = pd.to_numeric(df['Years_of_Experience'], errors='coerce').astype('Int64')

    return df
    
def sidebar(df):
    # =============================================================================
    # Layout barra Lateral
    # =============================================================================
    img = 'https://raw.githubusercontent.com/RafaelSanglard/4POA/e56ef29364141507467350fb2d1b0ed20df2f3e3/logo.jpg'
    st.sidebar.image(img, width=200)
    st.sidebar.markdown('# Salary analysis')
    st.sidebar.markdown('## Simplifying the business')
    st.sidebar.markdown('''---''')
    st.sidebar.markdown('## Selecione um salario limite')
    date_slider = st.sidebar.slider(
        'Deslize',
        value= 250001,
        min_value=351,
        max_value=255000
    )
        

    st.sidebar.markdown('''---''')
    st.sidebar.markdown('''### Powered by RaelSan''')
    
    #Filtro de data
    linhas_selecionadas = df['Salary'] < date_slider
    df = df.loc[linhas_selecionadas,:]

    
    return df
    
def maiores_salarios_cargo_pais(df):
    st.subheader("Maiores salários")
    # Finding the highest paying job title
    highest_paying_job_title = df.loc[df['Salary'].idxmax(), 'Job_Title']
    
    # Find the corresponding salary
    highest_salary = df.loc[df['Salary'].idxmax(), 'Salary']
    
    # Find the corresponding Country
    highest_country = df.loc[df['Salary'].idxmax(), 'Country']
    
    col1, col2, col3= st.columns(3,gap='small')
    with col1:
        st.subheader('Cargo')
        col1.metric("", "", highest_paying_job_title)

    with col2:
        st.subheader('Maior salário')
        col2.metric('O maior salario é:', highest_salary)
    with col3:
        st.subheader('Localizado')
        col3.metric('em:', highest_country)
       
    
#def menores_salarios_cargo_pais(df):
    st.subheader("Menores salários")

    # Finding the highest paying job title
    lowest_paying_job_title = df.loc[df['Salary'].idxmin(), 'Job_Title']
    
    # Find the corresponding salary
    lowest_salary = df.loc[df['Salary'].idxmin(), 'Salary']
    
    # Find the corresponding Country
    lowest_country = df.loc[df['Salary'].idxmin(), 'Country']
    
    col1, col2, col3=  st.columns(3,gap='small')
    with col1:
        st.subheader('Cargo')
        col1.metric("", '', lowest_paying_job_title)

    with col2:
        st.subheader('Menor salário')
        col2.metric('O menor salario é:', lowest_salary)
    with col3:
        st.subheader('Localizado')
        col3.metric('em:',lowest_country)
 

def top5_maiores(df):
    st.subheader("Médias salariais")
    
    median_salaries = df.groupby('Job_Title')['Salary'].median().reset_index()
    
    # Count the number of employees for each job title
    job_title_counts = df['Job_Title'].value_counts().reset_index()
    job_title_counts.columns = ['Job_Title', 'Employee_Count']
    
    # Merge the median_salaries DataFrame with the job_title_counts DataFrame
    median_salaries = median_salaries.merge(job_title_counts, on='Job_Title')
    
    # Sort the DataFrame by median salary in descending order
    lower_median_salaries = median_salaries.sort_values(by='Salary', ascending=False)
    higher_median_salaries = median_salaries.sort_values(by='Salary', ascending=True)
    top_5_lower_jobs = lower_median_salaries.head(5)
    top_5_jobs = higher_median_salaries.head(5)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("5 menores médias salariais")

        # Display the top 5 jobs with employee count without showing the index column
        st.markdown(
            top_5_jobs[['Job_Title', 'Employee_Count', 'Salary']].to_markdown(index=False),
            unsafe_allow_html=True
        )
    with col2:
        st.subheader("5 maiores médias salariais")

        # Display the top 5 lower jobs with employee count without showing the index column
        st.markdown(
            top_5_lower_jobs[['Job_Title', 'Employee_Count', 'Salary']].to_markdown(index=False),
            unsafe_allow_html=True
        )




def graf_salarios(df):
    with st.container():
        fig = px.box(df, y='Salary', title='Distribuição de salários')
        st.plotly_chart(fig)


    with st.container():
        fig = px.choropleth(df,
                            locations='Country',  # Column with country codes or names
                            color='Salary',        # Column with values to be visualized
                            locationmode='country names',  # Use country names
                            color_continuous_scale='icefire',  # Choose a color scale
                            title='Distribuição da média salarial pelo mundo')
        st.plotly_chart(fig)
    


# =============================================================================
#Layout no streamlit
df=load_df()
df=cleaning_df(df)


st.header('Visão salário')
df = sidebar(df)

 # Define the tab labels
tab_labels = ['OverView', 'Ranking média', 'Visão Geográfica']
selected_tab = st.selectbox('Selecione a visão:', tab_labels)
st.markdown('''---''')
# Define the content for each tab
if selected_tab == 'OverView':
    print("OverView selected")
    maiores_salarios_cargo_pais(df)
    
elif selected_tab == 'Ranking média':
    print("Visão Tática selected")
    top5_maiores(df)
    
elif selected_tab == 'Visão Geográfica':
    print("Visão Geográfica selected")
    graf_salarios(df)


