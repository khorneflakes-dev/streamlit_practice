import pandas as pd
import plotly.express as px
import streamlit as st
import plotly.graph_objects as go

st.set_page_config(page_title='Sales Dashboard', layout='wide', initial_sidebar_state='collapsed')


df_venta = pd.read_csv('./tablas/venta.csv', encoding='latin1')
df_sucursal = pd.read_csv('./tablas/sucursal.csv', encoding='latin1')
df_canalVenta = pd.read_csv('./tablas/canal_venta.csv', encoding='latin1')

df_venta['Ventas'] = df_venta['Precio'] * df_venta['Cantidad']
ventas = pd.merge(df_venta, df_sucursal, on='IdSucursal', how='left')
ventas_totales =  ventas.groupby(['Sucursal'], as_index=False).agg({'Ventas':'sum'}).sort_values(['Ventas'], ascending=False)


# CSS to inject contained in a string
hide_table_row_index = """
            <style>
            thead tr th:first-child {display:none}
            tbody th {display:none}
            </style>
            """

# Inject CSS with Markdown
st.markdown(hide_table_row_index, unsafe_allow_html=True)

#usar metodo de tabla para inyectar CSS

# SIDEBAR
st.sidebar.header('Options')

# MAINPAGE
st.title('Dashboard de Ventas')

fig_product_sales = px.bar(
    ventas_totales.head(7).sort_values(['Ventas'],ascending=True),
    x="Ventas",
    y='Sucursal',
    orientation="h",
    title="SUCURSALES CON MAS VENTAS",
    color_discrete_sequence=["#EDDCB1"] * len(ventas_totales),
    template="plotly_white",
    
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=True))
)

demo2 = st.plotly_chart(fig_product_sales, use_container_width=True)
