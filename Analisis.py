import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

# Configuración de la página de la aplicación
st.set_page_config(page_title="Empresa", page_icon="🗂", layout="wide")

# Cargar datos desde el archivo CSV
df = pd.read_csv('Empresa.CSV', encoding='utf-8')

# ---- SERVICES ---- #
with st.container():
    text_column,image_column = st.columns((3,3))
    with image_column:
        image = Image.open("Images/app.webp")
        st.image(image, use_column_width=True)
    with text_column:
        st.write("##")
        st.write("##")
        st.title("¡Bienvenido a la Plataforma de Análisis Empresarial!")
        st.write("Explora con nosotros este conjunto de datos detallado sobre una tienda de supermercado.")
        st.write("En nuestra plataforma, transformamos datos en insights significativos para facilitar decisiones informadas. Proporcionamos una experiencia visual interactiva que te permite adentrarte en diversos aspectos de tu negocio.")
        st.write("Desde evaluar el rendimiento de tus segmentos de clientes hasta analizar la distribución geográfica de tus productos, cada sección de nuestra plataforma te sumerge en un viaje de descubrimiento. Te invitamos a explorar, visualizar y comprender tus datos como nunca antes.")
        st.write("¡Prepárate para desbloquear el potencial de tu negocio a través de la inteligencia de datos!")


with st.container():
    # ---- Tabla Financiera ---- #
    st.markdown("<h1 style='text-align: center;'>Exploración Profunda del Rendimiento Financiero</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Le damos la bienvenida a una exploración profunda de nuestro rendimiento financiero, donde revelamos las claves detrás de nuestro desempeño económico. Este análisis meticuloso proporciona una visión integral de nuestras ventas, ingresos y beneficios, suministrando información esencial para la toma de decisiones estratégicas. Cada unidad vendida cuenta una historia de éxito, y cada ingreso desvela nuestra sólida trayectoria financiera. Brindaré un análisis enriquecedor y significativo de este desempeño financiero.</p>", unsafe_allow_html=True)
    st.write("##")

    # Seleccionar columnas relevantes
    selected_columns = ['Sales', 'Profit']

    # Calcular estadísticas
    stats = {
        'Suma Total': df[selected_columns].sum(),
        'Promedio': df[selected_columns].mean(),
        'Mediana': df[selected_columns].median(),
        'Desviación Estándar': df[selected_columns].std(),
        'Varianza': df[selected_columns].var(),
        'Mínimo': df[selected_columns].min(),
        'Máximo': df[selected_columns].max()
    }

    # Formatear valores con puntos para separar decimales, centenas y decenas
    formatted_stats = {key: value.apply('{:,.0f}'.format) for key, value in stats.items()}

    # Crear DataFrame con los resultados formateados
    result_df = pd.DataFrame(formatted_stats)

    # Transponer el DataFrame para intercambiar filas y columnas
    result_df_transposed = result_df.T

    # Mostrar el resultado en una tabla
    st.table(result_df_transposed)



# Encabezado y descripción
st.write("##")
st.markdown("<h3 style='text-align: center;'>Análisis Detallado de los Productos Más Vendidos</h3>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Este análisis detallado ofrece una visión integral de los productos más destacados en términos de ventas, cantidad de pedidos y beneficio. La información se presenta a través de gráficos interactivos, proporcionando una comprensión profunda del rendimiento de los productos clave en nuestra empresa. Explora el porcentaje de contribución de estos productos en las métricas de ventas, cantidad de pedidos y beneficio para obtener insights valiosos sobre el desempeño comercial.</p>", unsafe_allow_html=True)
st.write("##")

# Filtrar por categorías seleccionadas
selected_categories = st.multiselect('Seleccionar Categorías de Producto', sorted(df['Product Name'].unique()))
if not selected_categories:
    selected_categories = sorted(df['Product Name'].unique())

filtered_df = df[df['Product Name'].isin(selected_categories)]
st.write("##")

with st.container():
    dispersion_column, analisis_column = st.columns((3, 2))

    with dispersion_column:
        alt.themes.enable('opaque')

        scatter_chart = (
            alt.Chart(filtered_df)
            .mark_circle(opacity=0.7, size=100)
            .encode(
                x=alt.X('Sales:Q', title='Ventas').scale(zero=False),
                y=alt.Y('Profit:Q', title='Ganancia').scale(zero=False, padding=1),
                color=alt.Color('Product Name:N', scale=alt.Scale(range=['#F65300','#002FED','#F71000','#F71000'])),
                size='Profit:Q',
                tooltip=[
                    alt.Tooltip('Sales:Q', title='Ventas', format=',.0f'),
                    alt.Tooltip('Profit:Q', title='Ganancia', format=',.0f'),
                    alt.Tooltip('Product Name:N', title='Productos'),
                    alt.Tooltip('Order Date:T', title='Fecha')
                ],
            )
            .configure_legend(disable=True)
            .properties(
                width=800,
                height=500,
            )
            .interactive()
        )
        st.write("##")
        st.altair_chart(scatter_chart)

    with analisis_column:
        # Obtener los 10 productos principales por ventas
        top_productos_ventas = filtered_df.groupby('Product Name')['Sales'].sum().reset_index().nlargest(10, 'Sales')

        # Obtener los 10 productos principales por beneficio
        top_productos_profit = filtered_df.groupby('Product Name')['Profit'].sum().reset_index().nlargest(10, 'Profit')

        chart_ventas = alt.Chart(top_productos_ventas).mark_bar(color='#4C78A8').encode(
            y=alt.Y('Product Name:N', title='Productos', sort=alt.SortOrder('descending')),
            x=alt.X('Sales:Q', title='Ventas'),
            color=alt.value('#3469DE'),
            tooltip=[
                alt.Tooltip('Product Name:N', title='Productos'),
                alt.Tooltip('Sales:Q', title='Ventas', format=',.0f'),
            ],
        ).properties(
            width=550,
            height=460
        )

        chart_profit = alt.Chart(top_productos_profit).mark_bar(color='#F58518').encode(
            y=alt.Y('Product Name:N', title='Productos'),
            x=alt.X('Profit:Q', title='Beneficio', sort=alt.SortOrder('descending')),
            color=alt.value('#F65300'),
            tooltip=[
                alt.Tooltip('Product Name:N', title='Productos'),
                alt.Tooltip('Profit:Q', title='Beneficio', format=',.0f'),
            ],
        ).properties(
            width=550,
            height=460
        )

        grafico_combinado = alt.hconcat(chart_ventas + chart_profit).configure_axis(
            grid=False
        ).configure_axisY(
            orient='right'
        )

        st.altair_chart(grafico_combinado)


st.write("##")
with st.container():
    st.markdown("<h1 style='text-align: center;'>Tendencia a lo largo del tiempo</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Le damos la bienvenida a nuestro informe interactivo centrado en el análisis meticuloso de las ventas y ganancias a lo largo del tiempo. Este estudio exhaustivo proporciona una visión profunda del rendimiento comercial, permitiéndole descubrir patrones y tendencias clave. Exploraremos datos detallados para brindarle insights fundamentales sobre el desempeño de productos en diversas fechas. Le invitamos a adentrarse en la riqueza de nuestros gráficos interactivos y a extraer conocimientos estratégicos que impulsarán la toma de decisiones informada en su empresa.</p>", unsafe_allow_html=True)
    st.write("##")

    df['Order Date'] = pd.to_datetime(df['Order Date'])

    dispersion_column, analisis_column = st.columns((2, 2))
    with dispersion_column:
        selected_month = st.selectbox("Selecciona un mes", ['Todos'] + sorted(list(df['Order Date'].dt.month.unique())))
        st.write("##")
    with analisis_column:
        selected_year = st.selectbox("Selecciona un año", ['Todos'] + sorted(list(df['Order Date'].dt.year.unique())))
        st.write("##")

    filtered_df = df
    if selected_month != 'Todos':
        filtered_df = filtered_df[filtered_df['Order Date'].dt.month == selected_month]

    if selected_year != 'Todos':
        filtered_df = filtered_df[filtered_df['Order Date'].dt.year == selected_year]

    # Ordenar el DataFrame filtrado por 'Order Date'
    filtered_df = filtered_df.sort_values(by='Order Date')

    # Agrupar por fecha y calcular el total de ventas para el DataFrame filtrado
    ventas_por_fecha = filtered_df.groupby('Order Date')['Sales'].sum().reset_index()
    top_ventas_productos = ventas_por_fecha.sort_values(by='Sales', ascending=False).head(50)

    # Crear gráfico de ventas
    grafico_ventas_productos = (
        alt.Chart(top_ventas_productos)
        .mark_line(point=True, size=4)
        .encode(
            x=alt.X('Order Date:T', title='Fecha'),
            y=alt.Y('Sales:Q', title='Ventas'),
            color=alt.value('#3469DE'),
            tooltip=[
                alt.Tooltip('Order Date:T', title='Fecha'),
                alt.Tooltip('Sales:Q', title='Ventas', format=',.0f'),
            ],
        )
    )

    # Agrupar por fecha y calcular el total de ganancias para el DataFrame filtrado
    ganancias_por_fecha = filtered_df.groupby('Order Date')['Profit'].sum().reset_index()
    top_ganancias_productos = ganancias_por_fecha.sort_values(by='Profit', ascending=False).head(50)

    # Crear gráfico de ganancias
    grafico_ganancias_productos = (
        alt.Chart(top_ganancias_productos)
        .mark_line(point=True, size=4)
        .encode(
            x=alt.X('Order Date:T', title='Fecha'),
            y=alt.Y('Profit:Q', title='Ganancias'),
            color=alt.value('#F65300'),
            tooltip=[
                alt.Tooltip('Order Date:T', title='Fecha'),
                alt.Tooltip('Profit:Q', title='Ganancias', format=',.0f'),
            ],
        )
    )

    # Configuración del gráfico combinado
    grafico_combinado = (grafico_ventas_productos + grafico_ganancias_productos).properties(
        width=1600,  # Ajusta el ancho según tus necesidades
        height=400,  # Ajusta el alto según tus necesidades
    ).configure_axis(
        grid=False
    )

    # Mostrar el gráfico combinado en Streamlit
    st.altair_chart(grafico_combinado)

# Separar la creación de contenedores y contenido para mayor claridad
st.write("##")

# Contenedor principal
with st.container():
    # Títulos usando Markdown para un formato más limpio y centrado
    st.markdown("<h1 style='text-align: center;'>Exploración Clientes: Regiones y Provincias</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Bienvenido a nuestra plataforma de análisis de datos. Exploramos en profundidad la distribución y comportamiento de clientes en diferentes regiones y provincias. A través de este análisis detallado, obtenemos insights valiosos sobre la base de clientes, destacando tanto la cantidad total como el promedio por región. Acompáñanos en este viaje visual donde desglosamos la información para ofrecerte una comprensión clara y precisa de la dinámica de clientes en tu área geográfica.</p>", unsafe_allow_html=True)
    # Separador adicional para mejorar la presentación
    st.write("##")

    # Procesamiento de datos
    clientes_por_region_provincia = df.groupby(['Province', 'Region'])['Customer Name'].nunique().reset_index()
    clientes_totales_por_region = clientes_por_region_provincia.groupby('Region')['Customer Name'].sum().reset_index()
    clientes_promedio_por_region_provincia = clientes_por_region_provincia.groupby('Region')['Customer Name'].mean().reset_index()
    
    # Cambiar los nombres de las columnas a español
    clientes_totales_por_region.columns = ['Región', 'Clientes Totales']
    clientes_promedio_por_region_provincia.columns = ['Región', 'Clientes Promedio']

    tabla_final = pd.merge(clientes_totales_por_region, clientes_promedio_por_region_provincia, on='Región')

    # Eliminar la columna de índice antes de mostrar la tabla
    tabla_final_display = tabla_final.set_index('Región')
    
    # Visualización de la tabla
    st.table(tabla_final_display)

    # Separador adicional para mejorar la presentación
    st.write("##")

# Crear un contenedor en la interfaz
with st.container():

    # Encabezado y descripción en formato HTML
    st.markdown("<h1 style='text-align: center;'>Rendimiento de Productos por Región y Provincia</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Este panel interactivo de análisis de datos ha sido diseñado para proporcionar una visión profunda del rendimiento de productos en términos de ventas y beneficios. Con un control deslizante intuitivo, los usuarios pueden personalizar su análisis al seleccionar un rango específico de ventas. El panel presenta gráficos de barras detallados que destacan los 10 productos más rentables tanto a nivel regional como provincial. Permitiendo una toma de decisiones informada y estratégica en el ámbito de la gestión de ventas y beneficios.</p>", unsafe_allow_html=True)

    # Control deslizante para seleccionar rango de ventas
    sales_range = st.slider("Seleccione el rango:", 0, 100000, (0, 100000))

    # Filtrar el DataFrame original basándose en el rango seleccionado
    df_filtered = df[(df['Sales'].between(sales_range[0], sales_range[1]))]

    # Organizar la interfaz en dos columnas
    columna_analisis, columna_dispersion = st.columns((2, 1))

    # Gráficos de Barras para Beneficios por Región y Provincia
    with columna_dispersion:
        # Obtener los 10 productos más rentables por región y provincia
        top_productos_por_region = df_filtered.groupby('Region')['Sales'].sum().reset_index().nlargest(10, 'Sales')
        top_productos_por_provincia = df_filtered.groupby('Province')['Sales'].sum().reset_index().nlargest(10, 'Sales')

        # Crear gráficos de barras para ventas por región y provincia
        grafico_por_region = alt.Chart(top_productos_por_region).mark_bar(color='#F58518').encode(
            y=alt.Y('Region:N', title='Región'),
            x=alt.X('Sales:Q', title='Ventas', sort=alt.SortOrder('descending')),
            color=alt.value('#042259'),
            tooltip=[
                alt.Tooltip('Region:N', title='Región'),
                alt.Tooltip('Sales:Q', title='Ventas', format=',.0f'),
            ],
        ).properties(width=400, height=475)

        grafico_por_provincia = alt.Chart(top_productos_por_provincia).mark_bar(color='#F58518').encode(
            y=alt.Y('Province:N', title='Provincia'),
            x=alt.X('Sales:Q', title='Ventas', sort=alt.SortOrder('descending')),
            color=alt.value('#438EEF'),
            tooltip=[
                alt.Tooltip('Province:N', title='Provincia'),
                alt.Tooltip('Sales:Q', title='Ventas', format=',.0f'),
            ],
        ).properties(width=400, height=475)

        # Combinar gráficos en una presentación unificada
        grafico_combinado_dispersion = alt.hconcat(grafico_por_region + grafico_por_provincia).configure_axis(grid=False).configure_axisY(orient='right')

        st.write("##")
        st.altair_chart(grafico_combinado_dispersion)

    # Gráficos de Barras para Beneficios por Productos y Categoría
    with columna_analisis:
        # Obtener los 10 productos más rentables por región y provincia
        top_productos_profit = df_filtered.groupby('Region')['Profit'].sum().reset_index().nlargest(10, 'Profit')
        top_productos_category = df_filtered.groupby('Province')['Profit'].sum().reset_index().nlargest(10, 'Profit')

        # Crear gráficos de barras para beneficios por región y provincia
        chart_profit = alt.Chart(top_productos_profit).mark_bar(color='#F58518').encode(
            y=alt.Y('Region:N', title='Región'),
            x=alt.X('Profit:Q', title='Ganancias'),
            color=alt.value('#3469DE'),
            tooltip=[
                alt.Tooltip('Region:N', title='Región'),
                alt.Tooltip('Profit:Q', title='Ganancias', format=',.0f'),
            ],
        ).properties(width=550, height=475)

        chart_category = alt.Chart(top_productos_category).mark_bar(color='#F58518').encode(
            y=alt.Y('Province:N', title='Provincia'),
            x=alt.X('Profit:Q', title='Ganancias'),
            color=alt.value('#F65300'),
            tooltip=[
                alt.Tooltip('Province:N', title='Provincia'),
                alt.Tooltip('Profit:Q', title='Ganancias', format=',.0f')],
        ).properties(width=550, height=475)
        
        # Combinar ráficos en una presentación unificada
        grafico_combinado_analisis = alt.hconcat(chart_profit + chart_category).configure_axis(grid=False)

        st.write("##")
        st.altair_chart(grafico_combinado_analisis)

st.write("##")
# Crear un contenedor para organizar el diseño
with st.container():
    # Título principal utilizando HTML para estilos
    st.markdown("<h1 style='text-align: center;'>Logística Empresarial</h1>", unsafe_allow_html=True)
    
    # Descripción del análisis
    st.markdown("<p style='text-align: center;'>En este análisis estratégico, exploraremos la influencia de distintos segmentos de clientes en la gestión de envíos, así como el impacto de diversos modos de envío en los costos asociados. Los gráficos interactivos a continuación proporcionan una visión detallada de estos aspectos, brindándote la oportunidad de explorar y comprender en profundidad los patrones logísticos que impulsan el rendimiento de nuestra empresa.</p>", unsafe_allow_html=True)
    st.write("##")
    # Crear dos columnas para organizar los gráficos
    column_envios, column_ventas = st.columns((2,2))

    with column_envios:
        # Análisis de envíos por segmento de clientes
        df_envios = filtered_df.groupby('Customer Segment')['Order Quantity'].sum().reset_index()
        df_envios_sorted = df_envios.sort_values(by='Order Quantity', ascending=False)

        # Configuración del gráfico de envíos utilizando Altair
        chart_envios = (
            alt.Chart(df_envios_sorted)
            .mark_bar(color='#F58518', opacity=0.8)
            .encode(
                x=alt.X('Customer Segment:N', title='Segmento de Clientes', sort='-y', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('Order Quantity:Q', title='Cantidad de Envíos', axis=alt.Axis(grid=False)),
                color=alt.Color(
                    "Customer Segment:N",
                    title="Segmento de Clientes",
                    scale=alt.Scale(
                        domain=['Consumer', 'Corporate', 'Home Office', 'Small Business'],
                        range=['#042259','#FF5F00','#3469DE', '#4C78A8']
                    )
                )
            ).properties(width=800, height=500)
        )

        text = (
            alt.Chart(df_envios_sorted)
            .mark_text(dx=0, dy=30, color='white',fontSize=14)
            .encode(
                x=alt.X('Customer Segment:N').stack('zero'),
                y=alt.Y('Order Quantity:Q'),
                detail='Customer Segment:N',
                text=alt.Text('Order Quantity:Q', format='.0f')
            )
        )

        st.altair_chart(chart_envios + text)

    with column_ventas:
        # Análisis de ventas por modo de envío
        df_ventas = filtered_df.groupby('Ship Mode')['Shipping Cost'].sum().reset_index()
        df_ventas_sorted = df_ventas.sort_values(by='Shipping Cost', ascending=False)

        # Configuración del gráfico de ventas utilizando Altair
        chart_ventas = (
            alt.Chart(df_ventas_sorted)
            .mark_bar(color='#4C78A8', opacity=0.8)
            .encode(
                x=alt.X('Ship Mode:N', title='Modo de Envío', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('Shipping Cost:Q', title='Costo de Envío', axis=alt.Axis(grid=False)),
                color=alt.Color(
                    "Ship Mode:N",
                    title="Modo de Envío",
                    scale=alt.Scale(
                        domain=['Regular Air', 'Express Air', 'Delivery Truck'],
                        range=['#FF5F00','#042259','#3469DE']
                    ),
                )
            ).properties(width=800, height=500)
        )

        text = (
            alt.Chart(df_ventas_sorted)
            .mark_text(dx=0, dy=30, color='white', fontSize=14)
            .encode(
                x=alt.X('Ship Mode:N').stack('zero'),
                y=alt.Y('Shipping Cost:Q'),
                detail='Ship Mode:N',
                text=alt.Text('Shipping Cost:Q', format='.0f')
            )
        )

        st.altair_chart(chart_ventas + text, use_container_width=True)


st.write("---")
st.write("---")
with st.container():
    text_column,image_column = st.columns((3,3))
    with image_column:
        image = Image.open("Images/Ultimo.png")
        st.image(image, use_column_width=True)
    with text_column:
        st.write("##")
        st.write("##")
        st.write("##")
        # Pie de página
        with st.container():
            st.markdown("<h1 style='text-align: center;'>Contactame</h1>", unsafe_allow_html=True)

            st.markdown("<h5 style='text-align: center;'>Email: <a href='mailto:AlvarezLucianoEzequiel@gmail.com'>AlvarezLucianoEzequiel@gmail.com</a></h5>", unsafe_allow_html=True)
            st.markdown("<h5 style='text-align: center;'>LinkedIn: <a href='https://www.linkedin.com/in/luciano-alvarez-332843285/'>Luciano Alvarez</a></h5>", unsafe_allow_html=True)
            st.markdown("<h5 style='text-align: center;'>GitHub: <a href='https://github.com/LUXI4NO'>Luciano Alvarez</a></h5>", unsafe_allow_html=True)


            st.markdown("""
                <p style='text-align: center;'>¡Gracias por visitar mi sitio! Espero poder ayudarte con tus datos.</p>
            """, unsafe_allow_html=True)





