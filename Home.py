import streamlit as st
from PIL import Image
import pandas as pd
import inflection
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# import
df = pd.read_csv('zomato.csv')
df1=df
# Funçoes para tratamento de dados
def country_name(country_id): 
    return COUNTRIES[country_id]

def rename_columns(dataframe):
    df1 = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df1.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df1.columns = cols_new
    return df1

def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"

def color_name(color_code):
    return COLORS[color_code]


# Tratamento dos dados
# Renomeando todos os títulos das colunas para manter o mesmo padrão no nome
df1 = rename_columns(df1)

# Excluindo a coluna 'Switch to order menu' por ter o valor 0 em todas linhas 
df1 = df1.drop(columns =['switch_to_order_menu'])

# Excluindo todas linhas duplicadas da coluna 'Restaurant ID'
df1 = df1.drop_duplicates(subset=['restaurant_id']).reset_index(drop = True)

# Criando um dicionário referente a todos os países e seus codigos respectivos
COUNTRIES = {
1: "India",
14: "Australia",
30: "Brazil",
37: "Canada",
94: "Indonesia",
148: "New Zeland",
162: "Philippines",
166: "Qatar",
184: "Singapure",
189: "South Africa",
191: "Sri Lanka",
208: "Turkey",
214: "United Arab Emirates",
215: "England",
216: "United States of America",
}

# Criando uma nova coluna em df1 com o nome de cada país e excluindo a antiga
df1['countries'] = df1['country_code'].apply(lambda x: country_name(x))
df1 = df1.drop(columns = ['country_code'])

# Criando uma nova coluna com a categoria do restaurante e substituindo a antiga coluna 'price_range'
df1['category_food'] = df1['price_range'].apply(lambda x: create_price_type(x))
df1 = df1.drop(columns = ['price_range'])

# Criando um dicionário com o as cores referentes aos codigos e substituindo a coluna 'rating_color' pelos nomes das cores
COLORS = {
        "3F7E00": "darkgreen",
        "5BA829": "green",
        "9ACD32": "lightgreen",
        "CDD614": "orange",
        "FFBA00": "red",
        "CBCBC8": "darkred",
        "FF7800": "darkred"
}
    
# Criando uma nova coluna chamada colors e excluindo a antiga
df1['colors'] = df1['rating_color'].apply(lambda x: color_name(x))
df1 = df1.drop(columns = ['rating_color'])

# Mudando a coluna de cousines para string e pegando apenas o primeiro tipo de culinária 
df1["cuisines"] = df1.loc[:, "cuisines"].astype(str)
df1["cuisines"] = df1.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

df1 = df1.loc[df1['cuisines']!= 'nan',:]

######################################################################

st.set_page_config(
    page_title="Home",
    layout='wide',
    page_icon='🎲'
)

# image_path = '/home/rafael/Documentos/repos/ftc_programacao_python/'
image = Image.open('logo.png')
st.sidebar.image(image,width=120)

st.sidebar.markdown('# Fome Zero')
st.sidebar.markdown( """---""" )
st.write("# Fome Zero!")

st.markdown(
    """
    ### O melhor lugar para encontrar o seu mais novo restaurante favorito!
    #### Temos as seguintes métricas dentro da nossa plataforma:
    """
)

paises_var = st.sidebar.checkbox('Todos Países', value=False)
if paises_var == True:
    paises_op = df1['countries'].unique()
else:
    paises = df1['countries'].unique()
    paises_op = st.sidebar.multiselect('Selecione os Países',paises)

df2=df1
##########Filtro########
df1 = df1.loc[df1['countries'].isin(paises_op),:]
########################

with st.container():
    cl1, cl2, cl3, cl4, cl5 = st.columns(5)
    with cl1:
        st.markdown('Restaurantes Cadastrados')
        st.markdown(f'## {df2["restaurant_id"].nunique()}')
        
    with cl2:
        st.markdown('Países Cadastrados')
        st.markdown(f'## {df2['countries'].nunique()}')
        
    with cl3:
        st.markdown('Cidades Cadastradas')
        st.markdown(f'## {df2['city'].nunique()}')
        
    with cl4:
        st.markdown('Avaliações Feitas na Plataforma')
        st.markdown(f'## {df2['votes'].sum()}')
        
    with cl5:
        st.markdown('Tipos de Culinárias Oferecidas')
        st.markdown(f'## {df2['cuisines'].nunique()}')


with st.container():
    dfa = df1
    map = folium.Map()
    
        
    cluster = MarkerCluster().add_to(map)
    for index, location_info in dfa.iterrows():
        folium.Marker(location=[location_info['latitude'],
                               location_info['longitude']],
                      popup=location_info[['restaurant_name','aggregate_rating']],
                      icon=folium.Icon(color=location_info['colors'],icon='home')).add_to(cluster)
    
    folium_static(map, width=1024, height= 600)





