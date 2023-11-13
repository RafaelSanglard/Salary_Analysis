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
    

    df = df_raw.copy()
    
    
 
    
    return df
    
def cleaning_df(df):
    df['Race'] = df['Race'].str.strip()
    df['Country'] = df['Country'].str.strip()
    df['Gender'] = df['Gender'].apply(str.strip)
    df['Job_Title'] = df['Job_Title'].apply(str.strip)
    df['Job_Title'] = df['Job_Title'].replace(r'\_', ' ', regex=True)
    
    columns_to_clean = ['Age', 'Race', 'Salary', 'Senior', 'Country','Gender','Job_Title','Education_Level','Years_of_Experience']
    
    for column in columns_to_clean:
        linhas_selecionadas = (df[column] != 'NaN')
        df = df.loc[linhas_selecionadas, :].copy()
    
    df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce').astype('float')
    df['Senior'] = pd.to_numeric(df['Senior'], errors='coerce').astype('Int64')
    df['Education_Level'] = pd.to_numeric(df['Education_Level'], errors='coerce').astype('Int64')

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
    
    linhas_selecionadas = df['Salary'] < date_slider
    df = df.loc[linhas_selecionadas,:]
    

    
    return df
    
def idade_maior_menor_media(df):
    st.subheader("Idades")

    maior_idade = df.loc[df['Age'].idxmax()]
    media_idade = df['Age'].mean()
    menor_idade = df.loc[df['Age'].idxmin()]
    mediana_idade = df['Age'].median()
    col1, col2= st.columns(2, gap='small')

    with col1:
        st.subheader('Maior idade')
        max_age = maior_idade['Age']

        col1.metric(":", max_age)

        st.subheader('Menor idade')
        min_age = menor_idade['Age']
        
        col1.metric(":", min_age)

    with col2:
       

    
        st.subheader('Idade média')
        # Display the average and median age directly
        col2.metric(':', media_idade.round(2))
        st.subheader('Idade mediana')

        col2.metric(':', mediana_idade)


def graf_idade(df):
    # Plot a Plotly histogram for the salary distribution
    fig = px.histogram(df, x='Age', width=800, height=600, color_discrete_sequence=['skyblue'])
    fig.update_layout(title="Distribuição por idade", bargap=0.1)
    st.plotly_chart(fig)

   
 

# =============================================================================
#Layout no streamlit
df=load_df()
df=cleaning_df(df)


st.header('Idade')
df = sidebar(df)

 # Define the tab labels
tab_labels = ['OverView', 'Gráfico']
selected_tab = st.selectbox('Selecione a visão:', tab_labels)
st.markdown('''---''')
# Define the content for each tab
if selected_tab == 'OverView':
    idade_maior_menor_media(df)
    
elif selected_tab == 'Gráfico':
    graf_idade(df)



