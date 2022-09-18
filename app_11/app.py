from unittest.case import DIFF_OMITTED
import pandas as pd
# import plotly.express as px
# import streamlit as st
# import plotly.graph_objects as go

# st.set_page_config(page_title='Sales Dashboard', layout='wide', initial_sidebar_state='collapsed')


df_venta = pd.read_csv('./tablas/venta.csv', encoding='latin1')
df_sucursal = pd.read_csv('./tablas/sucursal.csv', encoding='latin1')
df_canalVenta = pd.read_csv('./tablas/canal_venta.csv', encoding='latin1')
df_gasto = pd.read_csv('./tablas/gasto.csv', encoding='latin1')
df_tipoProducto = pd.read_csv('./tablas/tipo_producto.csv', encoding='latin1')
df_compra = pd.read_csv('./tablas/compra.csv', encoding='latin1')
df_producto = pd.read_csv('./tablas/producto.csv', encoding='latin1')
# 6) Cuál es la sucursal con mayor venta (venta = Precio * Cantidad)? *\

df_venta['Ventas'] = df_venta['Precio'] * df_venta['Cantidad']
df_venta['Fecha'] = pd.to_datetime(df_venta['Fecha'])
df_venta['Anio'] = df_venta['Fecha'].dt.year
df_venta['Mes'] = df_venta['Fecha'].dt.month

ventas = pd.merge(df_venta, df_sucursal, on='IdSucursal', how='left')
ventas_totales =  ventas.groupby(['Sucursal','Anio','Mes'], as_index=False).agg({'Ventas':'sum'}).sort_values(['Ventas'], ascending=False)

# 7) La ganancia neta por sucursal es la venta menos los gastos (Ganancia = Venta - Gasto) 
# ¿Cuál es la sucursal con mayor ganancia neta en 2020? *

df_gasto['Fecha'] = pd.to_datetime(df_gasto['Fecha'])
df_gasto['Anio'] = df_gasto['Fecha'].dt.year
df_gasto['Mes'] = df_gasto['Fecha'].dt.month

gastos = pd.merge(df_gasto, df_sucursal, on=['IdSucursal'], how='left')
gastos_totales = gastos.groupby(['Sucursal','Anio','Mes'], as_index=False).agg({'Monto':'sum'})

ganancia = pd.merge(ventas_totales, gastos_totales, how='left', left_on=['Sucursal','Anio','Mes'], right_on=['Sucursal', 'Anio', 'Mes'])
ganancia['Ganancia_Neta'] = ganancia['Ventas'] - ganancia['Monto']

ganancia_tabular = ganancia.groupby(['Sucursal', 'Anio'], as_index=False).agg({'Ganancia_Neta': 'sum'})
ganancia_tabular = ganancia_tabular[ganancia_tabular['Anio']==2020].sort_values('Ganancia_Neta', ascending=False)

# 8) La ganancia neta por producto es las ventas menos las compras (Ganancia = Venta - Compra)
# ¿Cuál es el tipo de producto con mayor ganancia neta en 2020? *

df_compra['Fecha'] = pd.to_datetime(df_compra['Fecha'])
df_compra['Anio'] = df_compra['Fecha'].dt.year
df_compra['Mes'] = df_compra['Fecha'].dt.month
df_compra['Compras'] = df_compra['Cantidad'] * df_compra['Precio']
df_compras = pd.merge(df_compra, df_producto, on='IdProducto', how='left')
compras_idprodcuto = pd.merge(df_compras, df_tipoProducto, on='IdTipoProducto', how='left')
compras_por_producto = compras_idprodcuto.groupby(['TipoProducto', 'Anio'], as_index=False).agg({'Compras':'sum'})

df_ventas = pd.merge(ventas, df_producto, on='IdProducto', how='left')

ventas_idproducto = pd.merge(df_ventas, df_tipoProducto, on='IdTipoProducto', how='left')
ventas_por_producto = ventas_idproducto.groupby(['TipoProducto', 'Anio'], as_index=False).agg({'Ventas': 'sum'})

print(ventas_por_producto)





















# # CSS to inject contained in a string
# hide_table_row_index = """
#             <style>
#             thead tr th:first-child {display:none}
#             tbody th {display:none}
#             </style>
#             """

# # Inject CSS with Markdown
# st.markdown(hide_table_row_index, unsafe_allow_html=True)

# #usar metodo de tabla para inyectar CSS

# # SIDEBAR
# st.sidebar.header('Options')

# # MAINPAGE
# st.title('Dashboard de Ventas')

# fig_product_sales = px.bar(
#     ventas_totales.head(7).sort_values(['Ventas'],ascending=True),
#     x="Ventas",
#     y='Sucursal',
#     orientation="h",
#     title="SUCURSALES CON MAS VENTAS",
#     color_discrete_sequence=["#EDDCB1"] * len(ventas_totales),
#     template="plotly_white",
    
# )
# fig_product_sales.update_layout(
#     plot_bgcolor="rgba(0,0,0,0)",
#     xaxis=(dict(showgrid=True))
# )

# demo2 = st.plotly_chart(fig_product_sales, use_container_width=True)
