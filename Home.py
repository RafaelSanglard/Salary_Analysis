import streamlit as st

with st.container():
    img = 'https://raw.githubusercontent.com/RafaelSanglard/4POA/e56ef29364141507467350fb2d1b0ed20df2f3e3/logo.jpg'
    st.sidebar.image(img, width=200)
    st.sidebar.markdown('# Salary analysis')
    st.sidebar.markdown('''---''')
    st.sidebar.markdown('## Simplifying the business')
    st.sidebar.markdown('''---''')
    st.sidebar.markdown('''### Powered by RaelSan''')

st.markdown(
    """
    Desenvolvido para acompanhar as métricas salariais de diferentes cargos, Optei por criar 3 dashboards.
### Como utilizar?

- Salário - métricas gerais sobre a base de dados
  - Overview - maiores, menores, médias e medianas
  - Ranking - top 5 maiores e 5 menores salários
  - Representação gráfica - gráfico e mapa mostrando a distribuição de salários

- Idade - Métricas relacionadas à idade versus salário dos colaboradores
  - Overview - maiores, menores, médias e medianas
  - Gráfico - representação gráfica do Overview

- Software Engineer - Métricas específicas do cargo, selecionado por ser um dos que possui o maior número de colaboradores.
  - Overview - dados e gráfico sobre idade versus salário para engenheiros de software
  - Gênero e raça - análise da divisão salarial usando gênero e raça como parâmetro
  - Salário por País - representação gráfica da distribuição salarial


    """
)