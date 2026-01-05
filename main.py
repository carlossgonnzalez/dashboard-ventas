import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# CONFIGURACIÓN DE PÁGINA
st.set_page_config(page_title='Dashboard Ventas', layout='wide', initial_sidebar_state='expanded')


# SIDEBAR
with st.sidebar:
    st.title('Configuración')
    st.divider()

    pagina = st.selectbox('Selecciona una sección', ['Visión global', 'Análisis por tienda', 'Análisis por estado', 'Insights'])

    st.divider()
    st.caption('Proyecto de Visualización de Datos')


df_global = pd.read_csv('parte_1.csv')
df_store = pd.read_csv('parte_2.csv')

st.title('Dashboard de Ventas')
st.divider()


# VISIÓN GLOBAL
if pagina == 'Visión global':

    st.header('Visión global de las ventas')

    # KPIs
    with st.container(border=True):
        st.subheader('KPIs generales')

        col1, col2, col3, col4 = st.columns(4)
        col1.metric('Tiendas', df_global['store_nbr'].nunique())
        col2.metric('Productos', df_global['family'].nunique())
        col3.metric('Estados', df_global['state'].nunique())
        col4.metric('Meses con datos', df_global[['year', 'month']].drop_duplicates().shape[0])

    # Análisis de ventas
    with st.container(border=True):
        st.subheader('Análisis de ventas')

        col_left, col_right = st.columns(2)

        top_products = df_global.groupby('family')['sales'].sum().sort_values(ascending=False).head(10)
        sales_store = df_global.groupby('store_nbr')['sales'].sum()

        with col_left:
            fig, ax = plt.subplots(figsize=(5.5, 4))
            top_products.sort_values().plot(kind='barh', ax=ax)
            ax.set_title('Top 10 productos más vendidos')
            ax.set_xlabel('Ventas')
            ax.set_ylabel('Producto')
            ax.grid(axis='x', alpha=0.3)
            st.pyplot(fig)

        with col_right:
            fig, ax = plt.subplots(figsize=(5.5, 4))
            ax.hist(sales_store, bins=25)
            ax.set_title('Distribución de ventas por tienda')
            ax.set_xlabel('Ventas')
            ax.set_ylabel('Número de tiendas')
            ax.grid(axis='y', alpha=0.3)
            st.pyplot(fig)

    # Ventas en promoción
    with st.container(border=True):
        st.subheader('Ventas en promoción')

        top_promo_stores = df_global[df_global['onpromotion'] > 0].groupby('store_nbr')['sales'].sum().sort_values(ascending=False).head(10)

        col_left, col_right = st.columns([2, 3])

        with col_left:
            fig, ax = plt.subplots(figsize=(4, 3))
            top_promo_stores.sort_values().plot(kind='barh', ax=ax)
            ax.set_title('Top 10 tiendas con ventas en promoción')
            ax.set_xlabel('Ventas')
            ax.set_ylabel('Tienda')
            ax.grid(axis='x', alpha=0.3)
            st.pyplot(fig)

    # Estacionalidad
    with st.expander('Estacionalidad de las ventas'):

        col1, col2, col3 = st.columns(3)

        orden_dias = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        dow_sales = df_global.groupby('day_of_week')['sales'].mean().reindex(orden_dias)

        fig, ax = plt.subplots(figsize=(4, 3))
        dow_sales.plot(kind='bar', ax=ax)
        ax.set_title('Por día de la semana')
        ax.set_ylabel('Ventas medias')
        ax.tick_params(axis='x', rotation=45)
        ax.grid(axis='y', alpha=0.3)
        col1.pyplot(fig)

        week_sales = df_global.groupby('week')['sales'].mean()
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.plot(week_sales.index, week_sales.values, marker='o')
        ax.set_title('Por semana del año')
        ax.set_xlabel('Semana')
        ax.set_ylabel('Ventas medias')
        ax.grid(alpha=0.3)
        col2.pyplot(fig)

        month_sales = df_global.groupby('month')['sales'].mean()
        fig, ax = plt.subplots(figsize=(4, 3))
        ax.plot(month_sales.index, month_sales.values, marker='o')
        ax.set_title('Por mes')
        ax.set_xlabel('Mes')
        ax.set_ylabel('Ventas medias')
        ax.grid(alpha=0.3)
        col3.pyplot(fig)


# ANÁLISIS POR TIENDA
elif pagina == 'Análisis por tienda':

    st.header('Análisis por tienda')

    store_selected = st.selectbox('Selecciona una tienda', sorted(df_store['store_nbr'].unique()))

    df_filtered = df_store[df_store['store_nbr'] == store_selected]

    with st.container(border=True):
        st.subheader('KPIs de la tienda')

        col1, col2, col3 = st.columns(3)
        col1.metric('Ventas totales', int(df_filtered['sales'].sum()))
        col2.metric('Productos vendidos', int(df_filtered['sales'].sum()))
        col3.metric('En promoción', int(df_filtered[df_filtered['onpromotion'] > 0]['sales'].sum()))

    with st.container(border=True):
        st.subheader('Ventas por año')

        sales_year = df_filtered.groupby('year')['sales'].sum().sort_index()

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(sales_year.index, sales_year.values, marker='o', linewidth=2)
        ax.set_title('Ventas totales por año')
        ax.set_xlabel('Año')
        ax.set_ylabel('Ventas')
        ax.set_xticks(sales_year.index)
        ax.set_xticklabels(sales_year.index.astype(int))
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)


# ANÁLISIS POR ESTADO
elif pagina == 'Análisis por estado':

    st.header('Análisis por estado')

    state_selected = st.selectbox('Selecciona un estado', sorted(df_store['state'].unique()))

    df_state = df_store[df_store['state'] == state_selected]

    with st.container(border=True):
        st.subheader('KPIs del estado')

        col1, col2, col3 = st.columns(3)
        col1.metric('Tiendas', df_state['store_nbr'].nunique())
        col2.metric('Productos', df_state['family'].nunique())
        col3.metric('Ventas totales', int(df_state['sales'].sum()))

    with st.container(border=True):
        st.subheader('Ventas por año')

        sales_year_state = df_state.groupby('year')['sales'].sum().sort_index()

        fig, ax = plt.subplots(figsize=(5, 3))
        ax.plot(sales_year_state.index, sales_year_state.values, marker='o', linewidth=2)
        ax.set_title('Ventas totales por año')
        ax.set_xlabel('Año')
        ax.set_ylabel('Ventas')
        ax.set_xticks(sales_year_state.index)
        ax.set_xticklabels(sales_year_state.index.astype(int))
        ax.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        st.pyplot(fig)

    with st.container(border=True):
        st.subheader('Ranking de tiendas del estado')

        top_stores_state = df_state.groupby('store_nbr')['sales'].sum().sort_values(ascending=False).head(10)

        fig, ax = plt.subplots(figsize=(5.5, 4))
        top_stores_state.sort_values().plot(kind='barh', ax=ax)
        ax.set_title('Top tiendas por ventas')
        ax.set_xlabel('Ventas')
        ax.set_ylabel('Tienda')
        ax.grid(axis='x', alpha=0.3)
        st.pyplot(fig)

    with st.container(border=True):
        st.subheader('Producto más vendido en el estado')

        top_product_state = df_state.groupby('family')['sales'].sum().sort_values(ascending=False).head(1)

        product_name = top_product_state.index[0]
        product_sales = int(top_product_state.values[0])

        st.metric(label='Producto', value=product_name, delta=f'{product_sales} ventas')


# INSIGHTS
elif pagina == 'Insights':

    st.header('Insight estratégico: optimización del negocio')

    with st.container(border=True):
        st.subheader('Productos clave según contribución a ventas')

        porcentaje_objetivo = st.slider('Porcentaje de ventas totales a cubrir', min_value=0, max_value=100, value=80, step=5)

        sales_by_product = df_global.groupby('family')['sales'].sum().sort_values(ascending=False)

        total_sales = sales_by_product.sum()
        cumulative_pct = sales_by_product.cumsum() / total_sales * 100

        productos_core = cumulative_pct[cumulative_pct <= porcentaje_objetivo]

        st.metric('Número de productos necesarios', len(productos_core))

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.plot(range(1, len(cumulative_pct) + 1), cumulative_pct.values, marker='o')
        ax.axhline(porcentaje_objetivo, linestyle='--')
        ax.set_xlabel('Número de productos')
        ax.set_ylabel('Ventas acumuladas (%)')
        ax.set_title('Contribución acumulada de productos')
        ax.grid(alpha=0.3)
        st.pyplot(fig)

        with st.expander('Ver productos que componen este porcentaje'):
            st.write(productos_core.index.tolist())

    with st.container(border=True):
        st.subheader('Tiendas con bajo rendimiento relativo')

        umbral = st.slider('Umbral de rendimiento', min_value=25, max_value=100, value=50, step=5)

        sales_by_store = df_global.groupby('store_nbr')['sales'].sum()

        media_ventas = sales_by_store.mean()
        tiendas_bajo_rendimiento = sales_by_store[sales_by_store < media_ventas * (umbral / 100)]

        st.metric(f'Tiendas candidatas a seguimiento continuo', len(tiendas_bajo_rendimiento))

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(sales_by_store.index, sales_by_store.values)
        ax.axhline(media_ventas, linestyle='--', label='Media de ventas')
        ax.axhline(media_ventas * (umbral / 100), linestyle=':', label='Umbral')
        ax.set_xlabel('Tienda')
        ax.set_ylabel('Ventas')
        ax.set_title('Ventas por tienda vs media')
        ax.legend()
        ax.grid(axis='y', alpha=0.3)
        st.pyplot(fig)

        with st.expander('Ver tiendas candidatas a seguimiento continuo'):
            st.write(tiendas_bajo_rendimiento.index.tolist())
