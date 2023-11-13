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
    
    #
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
    

def overview(df):
    # Finding the highest paying job title
    # Filter the DataFrame to only include 'Software Engineer' job titles
    software_engineer_df = df[df['Job_Title'] == 'Software Engineer'].sort_values(by='Salary', ascending=False)
    highest_salary = software_engineer_df.iloc[0]['Salary']
    lowest_salary = software_engineer_df.iloc[-1]['Salary']
    media_salary = software_engineer_df['Salary'].mean()
    median_salary = software_engineer_df['Salary'].median()
   
    col1, col2 = st.columns(2, gap='small')
    
    with col1:
        st.subheader('Maior salário')
        col1.metric("é de:", highest_salary)

        st.subheader('Menor salário')
        col1.metric('é de:', lowest_salary)
    
    with col2:
        st.subheader('Salário médio')
        col2.metric('é:', media_salary.round(2))

        st.subheader('Mediana')
        col2.metric('é:', median_salary)

    fig = px.bar(software_engineer_df, x='Age', y='Salary', color='Education_Level',
                 title="Relação entre idade e salário de engenheiros de software, com filtro por níveis de educação.")
    st.plotly_chart(fig)

       
    
def gender_race(df):
    software_engineer_df = df[df['Job_Title'] == 'Software Engineer'].sort_values(by='Salary', ascending=False)

    software_engineer_df_sorted = software_engineer_df.sort_values(by='Salary')
    # Create the bar chart
    fig = px.bar(software_engineer_df_sorted, x='Age', y='Salary', color='Race',
             title='Relação entre idade e salário de engenheiros de software, com filtro por raça.')
    st.plotly_chart(fig)


    fig = px.scatter(software_engineer_df, x='Age', y='Salary', color='Gender',
             title='Relação entre idade e salário de engenheiros de software, com filtro por genero.')

    st.plotly_chart(fig)




def sal_per_county(df):
    software_engineer_df = df[df['Job_Title'] == 'Software Engineer'].sort_values(by='Salary', ascending=False)

    software_engineer_df_sorted = software_engineer_df.sort_values(by='Salary')
    with st.container():
        fig = px.scatter(software_engineer_df, x="Country", y="Salary", color = 'Age',
                     title='Relação entre Países e salário de engenheiros de software.')        
        st.plotly_chart(fig)
    


# =============================================================================
#Layout no streamlit
df=load_df()
df=cleaning_df(df)


st.header('Cargo: Software Engineer')
df = sidebar(df)

 # Define the tab labels
tab_labels = ['OverView', 'Genero e raça', 'Salario por País']
selected_tab = st.selectbox('Selecione a visão:', tab_labels)
st.markdown('''---''')
# Define the content for each tab
if selected_tab == 'OverView':
    print("OverView selected")
    overview(df)
    
elif selected_tab == 'Genero e raça':
    gender_race(df)
    
elif selected_tab == 'Salario por País':
    sal_per_county(df)


