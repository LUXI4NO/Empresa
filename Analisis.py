# Importar las bibliotecas necesarias
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

# Configurar la página Streamlit
st.set_page_config(page_title="Empresa", page_icon="🗂", layout="wide")

# Cargar datos desde el archivo CSV
df = pd.read_csv('Empresa.CSV', encoding='utf-8')

# Crear una estructura de columna para el diseño
with st.container():
    # Dividir la página en dos columnas: columna de texto e imagen
    text_column, image_column = st.columns((3, 3))

    # En la columna de imagen, mostrar la imagen del proyecto
    with image_column:
        image = Image.open("Images/app.webp")
        st.image(image, use_column_width=True)

    # En la columna de texto, mostrar información sobre el proyecto
    with text_column:
        st.write("##")
        st.title("¡Bienvenido a este Proyecto de Análisis Empresarial!")
        st.write("Explora con nosotros este conjunto de datos detallado sobre una tienda de supermercado.")
        st.write("En nuestra plataforma, transformamos datos en insights significativos para facilitar decisiones informadas. Proporcionamos una experiencia visual interactiva que te permite adentrarte en diversos aspectos de tu negocio.")
        st.write("Desde evaluar el rendimiento de tus segmentos de clientes hasta analizar la distribución geográfica de tus productos, cada sección de nuestra plataforma te sumerge en un viaje de descubrimiento. Te invitamos a explorar, visualizar y comprender tus datos como nunca antes.")
        st.write("¡Prepárate para desbloquear el potencial de tu negocio a través de la inteligencia de datos!")


# Crear un contenedor para organizar la presentación en Streamlit
with st.container():

    # Título principal y descripción de la exploración estadística de ventas y ganancias
    st.markdown("<h1 style='text-align: center;'>Exploración Estadística de Ventas y Ganancias en un Conjunto de Datos</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'> Proporcionaremos un análisis conciso de las columnas 'Sales' y 'Profit' en un conjunto de datos, presentando estadísticas clave como suma total, promedio y desviación estándar. La información se organiza en una tabla intuitiva, facilitando la comprensión de la distribución y las características destacadas de las ventas y ganancias. Valioso para la toma de decisiones informada en el ámbito empresarial.</p>", unsafe_allow_html=True)
    
    # Separador visual
    st.write("##")

    # Definir las columnas seleccionadas para la exploración estadística
    selected_columns = ['Sales', 'Profit']

    # Crear un DataFrame con estadísticas clave
    stats = pd.DataFrame({
        'Categoria': ['Sales', 'Profit'],
        'Suma Total': df[selected_columns].sum(),
        'Promedio': df[selected_columns].mean(),
        'Mediana': df[selected_columns].median(),
        'Desviación Estándar': df[selected_columns].std(),
        'Varianza': df[selected_columns].var(),
        'Mínimo': df[selected_columns].min(),
        'Máximo': df[selected_columns].max()
    })

    # Mostrar el resultado en una tabla con formato y estilos
    st.table(stats.set_index('Categoria', drop=True).style 
        .set_properties(**{'text-align': 'center', 'font-size': '18px'})
        .bar(subset=['Suma Total', 'Promedio', 'Mediana', 'Desviación Estándar','Varianza','Mínimo','Máximo'], color='#83B7E2')
        .highlight_max(axis=0, color='#ECF3FD')
        .format({'Suma Total': '{:,.0f}', 'Promedio': '{:,.0f}%', 'Mediana': '{:,.0f}', 'Desviación Estándar': '{:,.0f}', 'Varianza': '{:,.0f}', 'Mínimo': '{:,.0f}', 'Máximo': '{:,.0f}'})
        .set_table_styles([
                {'selector': 'th', 'props': [('background-color', '#ECF3FD'), ('color', '#000000'),
                                              ('font-size', '18px'), ('border', '1px solid #000000')]},
                {'selector': 'td', 'props': [('border', '1px solid #000000'), ('color', 'black')]}, 
                {'selector': 'tr:hover', 'props': [('background-color', '#000000')]},
                {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#EDF3FD')]},
                {'selector': 'tr:nth-child(odd)', 'props': [('background-color', '#EDF3FD')]},
                {'selector': 'td:hover', 'props': [('background-color', '#F58518'), ('color', 'White')]}
             ])
        )

# Agregar espaciado en la página
st.write("##")
st.write("##")

# Crear un contenedor para organizar la presentación en Streamlit
with st.container():
    # Título principal y descripción de la visualización interactiva de ventas y ganancias por categorías de producto
    st.markdown("<h1 style='text-align: center;'>Visualización Interactiva de Ventas y Ganancias por Categorías de Producto</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Este código permite explorar de manera interactiva las ventas y ganancias asociadas a categorías específicas de productos en un conjunto de datos. Utilizando una interfaz de selección múltiple, puedes filtrar las categorías de productos que deseas analizar.</p>", unsafe_allow_html=True)

    # Crear un cuadro de selección múltiple para elegir las categorías de productos
    selected_categories = st.multiselect('Seleccionar Categorías de Producto', sorted(df['Product Name'].unique()))
    
    # Si no se seleccionan categorías, mostrar todas las categorías por defecto
    if not selected_categories:
        selected_categories = sorted(df['Product Name'].unique())

    # Filtrar el DataFrame según las categorías seleccionadas
    filtered_df = df[df['Product Name'].isin(selected_categories)]
    
    # Dividir la página en dos columnas: dispersión y análisis
    dispersion_column, analisis_column = st.columns((3, 2))

    # En la columna de dispersión, mostrar un gráfico de dispersión interactivo
    with dispersion_column:
        alt.themes.enable('opaque')

        scatter_chart = (
            alt.Chart(filtered_df).mark_circle(opacity=0.7, size=100).encode(
                alt.X('Sales:Q', title='Ventas').scale(zero=False),
                alt.Y('Profit:Q', title='Ganancia').scale(zero=False, padding=1),
                alt.Color('Product Name:N', scale=alt.Scale(range=['#F65300','#002FED','#F71000','#F71000'])),
                size='Profit:Q',
                tooltip=[
                    alt.Tooltip('Sales:Q', title='Ventas', format=',.0f'),
                    alt.Tooltip('Profit:Q', title='Ganancia', format=',.0f'),
                    alt.Tooltip('Product Name:N', title='Productos'),
                    alt.Tooltip('Order Date:T', title='Fecha')
                ],
            ).configure_legend(disable=True).properties(width=600, height=550).interactive()
        )

        # Mostrar el gráfico de dispersión en la aplicación
        st.altair_chart(scatter_chart, use_container_width=True)

    # En la columna de análisis, mostrar gráficos de barras para las 10 principales categorías en ventas y ganancias
    with analisis_column:
        # Obtener las 10 principales categorías por ventas y ganancias
        top_productos_ventas = filtered_df.groupby('Product Name')['Sales'].sum().reset_index().nlargest(10, 'Sales')
        top_productos_profit = filtered_df.groupby('Product Name')['Profit'].sum().reset_index().nlargest(10, 'Profit')

        # Crear gráfico de barras para las 10 principales categorías por ventas
        chart_ventas = alt.Chart(top_productos_ventas).mark_bar(color='#4C78A8').encode(
            alt.Y('Product Name:N', title='Productos', sort=alt.SortOrder('descending')),
            alt.X('Sales:Q', title='Ventas'),
            color=alt.value('#F65300'),
            tooltip=[
                alt.Tooltip('Product Name:N', title='Productos'),
                alt.Tooltip('Sales:Q', title='Ventas', format=',.0f')]
        )

        # Crear gráfico de barras para las 10 principales categorías por ganancias
        chart_profit = alt.Chart(top_productos_profit).mark_bar(color='#F58518').encode(
            alt.Y('Product Name:N', title='Productos'),
            alt.X('Profit:Q', title='Beneficio', sort=alt.SortOrder('descending')),
            color=alt.value('#3469DE'),
            tooltip=[
                alt.Tooltip('Product Name:N', title='Productos'),
                alt.Tooltip('Profit:Q', title='Beneficio', format=',.0f')]
        )

        # Combinar los dos gráficos de barras
        combined_chart = (chart_ventas + chart_profit).properties(width=300, height=550).configure_axis(grid=False).configure_axisY(orient='right').configure_legend(orient='top')

        # Mostrar el gráfico combinado en la aplicación
        st.altair_chart(combined_chart, use_container_width=True)


# Agregar espaciado en la página
st.write("##")
st.write("##")

# Crear un contenedor para organizar la presentación en Streamlit
with st.container():
    # Título principal y descripción de la visualización interactiva de ventas y ganancias por fechas
    st.markdown("<h1 style='text-align: center;'>Visualización Interactiva de Ventas y Ganancias por fechas</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Este código permite explorar de manera interactiva las ventas y ganancias asociadas a una tendencia específica por fechas en un conjunto de datos. Utilizando una interfaz de selección múltiple, puedes filtrar las categorías de productos que deseas analizar.</p>", unsafe_allow_html=True)

    # Convertir la columna 'Order Date' a formato de fecha
    df['Order Date'] = pd.to_datetime(df['Order Date'])

    # Crear dos columnas para seleccionar mes y año
    dispersion_column, analisis_column = st.columns((2, 2))
    with dispersion_column:
        selected_month = st.selectbox("Selecciona un mes", ['Todos'] + sorted(list(df['Order Date'].dt.month.unique())))
    with analisis_column:
        selected_year = st.selectbox("Selecciona un año", ['Todos'] + sorted(list(df['Order Date'].dt.year.unique())))

    # Filtrar el DataFrame según el mes y el año seleccionados
    filtered_df = df
    if selected_month != 'Todos':
        filtered_df = filtered_df[filtered_df['Order Date'].dt.month == selected_month]

    if selected_year != 'Todos':
        filtered_df = filtered_df[filtered_df['Order Date'].dt.year == selected_year]

    # Ordenar el DataFrame por fecha
    filtered_df = filtered_df.sort_values(by='Order Date')

    # Calcular las ventas por fecha y las 50 mejores
    ventas_por_fecha = filtered_df.groupby('Order Date')['Sales'].sum().reset_index()
    top_ventas_productos = ventas_por_fecha.sort_values(by='Sales', ascending=False).head(50)

    # Calcular las ganancias por fecha y las 50 mejores
    ganancias_por_fecha = filtered_df.groupby('Order Date')['Profit'].sum().reset_index()
    top_ganancias_productos = ganancias_por_fecha.sort_values(by='Profit', ascending=False).head(50)

    # Configurar la selección de puntos en el gráfico
    punto_seleccionado = alt.selection_interval(empty='all', encodings=['x'])

    # Crear gráfico de ventas
    grafico_ventas_productos = (alt.Chart(top_ventas_productos).mark_line(point=True, size=4).encode(
            alt.X('Order Date:T', title='Fecha'),
            alt.Y('Sales:Q', title='Ventas'),
            color=alt.value('#F65300'),
            tooltip=[
                alt.Tooltip('Order Date:T', title='Fecha'),
                alt.Tooltip('Sales:Q', title='Ventas', format=',.0f'),
            ],
        )
    ).add_selection(punto_seleccionado)

    # Crear gráfico de ganancias
    grafico_ganancias_productos = (alt.Chart(top_ganancias_productos).mark_line(point=True, size=4).encode(
            alt.X('Order Date:T', title='Fecha'),
            alt.Y('Profit:Q', title='Ganancias'),
            color=alt.value('#3469DE'),
            tooltip=[
                alt.Tooltip('Order Date:T', title='Fecha'),
                alt.Tooltip('Profit:Q', title='Ganancias', format=',.0f'),
            ],
        )
    ).add_selection(punto_seleccionado)

    # Combinar los dos gráficos en uno solo
    grafico_combinado = (grafico_ventas_productos + grafico_ganancias_productos).properties(width=1450, height=500).configure_axis(grid=False)

    # Mostrar el gráfico combinado en la aplicación
    st.altair_chart(grafico_combinado,  use_container_width=True)


# Agregar espaciado en la página
st.write("##")
st.write("##")

# Título principal y descripción del análisis integral de clientes y ventas por región y provincia
st.markdown("<h1 style='text-align: center;'> Análisis Integral de Clientes y Ventas por Región y Provincia</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Este código proporciona una visión detallada del desempeño comercial, destacando la distribución de clientes y ventas en diferentes regiones y provincias. La información se presenta de manera clara y visualmente atractiva, facilitando la identificación de patrones y oportunidades clave.</p>", unsafe_allow_html=True)

# Crear un expander para mostrar la tabla de clientes y regiones
with st.expander("Tabla de Clientes y Regiones"):
    # Calcular el número de clientes únicos por región y provincia
    clientes_por_region_provincia = df.groupby(['Province', 'Region'])['Customer Name'].nunique().reset_index()

    # Calcular el total de clientes por región
    clientes_totales_por_region = clientes_por_region_provincia.groupby('Region')['Customer Name'].sum().reset_index()

    # Renombrar columnas para mayor claridad
    clientes_totales_por_region.columns = ['Región', 'Clientes Totales']

    # Configurar la tabla para mostrar en la aplicación
    tabla_final_display = clientes_totales_por_region.set_index('Región')

    # Mostrar la tabla en la aplicación con formato y estilos
    st.table(
        tabla_final_display.style
        .set_properties(**{'text-align': 'center', 'font-size': '18px'})
        .bar(subset=['Clientes Totales'], color='#83B7E2')
        .highlight_max(axis=0, color='#ECF3FD')
        .format({'Clientes Totales': '{:,.0f}'})
        .set_table_styles([
            {'selector': 'th', 'props': [('background-color', '#ECF3FD'), ('color', '#000000'),
                                        ('font-size', '18px'), ('border', '1px solid #000000')]},
            {'selector': 'td', 'props': [('border', '1px solid #000000'), ('color', 'black')]},  
            {'selector': 'tr:hover', 'props': [('background-color', '#000000')]},
            {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#EDF3FD')]},
            {'selector': 'tr:nth-child(odd)', 'props': [('background-color', '#EDF3FD')]},
            {'selector': 'td:hover', 'props': [('background-color', '#F58518'), ('color', 'White')]}
        ])
    )


# Crear un contenedor para organizar la presentación en Streamlit
with st.container():

    # Crear un slider para seleccionar el rango de ventas
    sales_range = st.slider("Seleccione el rango:", 0, 100000, (0, 100000))

    # Filtrar el DataFrame según el rango de ventas seleccionado
    df_filtered = df[(df['Sales'].between(sales_range[0], sales_range[1]))]

    # Dividir la página en dos columnas: análisis y dispersión
    columna_analisis, columna_dispersion = st.columns((2, 2))

    # En la columna de dispersión, mostrar gráficos de barras para las 10 principales regiones y provincias por ventas
    with columna_dispersion:

        # Calcular las 10 principales regiones por ventas
        top_productos_por_region = df_filtered.groupby('Region')['Sales'].sum().reset_index().nlargest(10, 'Sales')

        # Calcular las 10 principales provincias por ventas
        top_productos_por_provincia = df_filtered.groupby('Province')['Sales'].sum().reset_index().nlargest(10, 'Sales')

        # Crear gráfico de barras para las 10 principales regiones por ventas
        grafico_por_region = alt.Chart(top_productos_por_region).mark_bar(color='#F58518').encode(
            y=alt.Y('Region:N', title='Región'),
            x=alt.X('Sales:Q', title='Ventas', sort=alt.SortOrder('descending')),
            color=alt.value('#F65300'),
            tooltip=[
                alt.Tooltip('Region:N', title='Región'),
                alt.Tooltip('Sales:Q', title='Ventas', format=',.0f'),
            ],
        )

        # Crear gráfico de barras para las 10 principales provincias por ventas
        grafico_por_provincia = alt.Chart(top_productos_por_provincia).mark_bar(color='#F58518').encode(
            y=alt.Y('Province:N', title='Provincia'),
            x=alt.X('Sales:Q', title='Ventas', sort=alt.SortOrder('descending')),
            color=alt.value('#3469DE'),
            tooltip=[
                alt.Tooltip('Province:N', title='Provincia'),
                alt.Tooltip('Sales:Q', title='Ventas', format=',.0f'),
            ],
        )

        # Combinar los dos gráficos de barras
        combined_chart = (grafico_por_region + grafico_por_provincia).configure_legend(orient='top').properties(width=300, height=550).configure_axis(grid=False).configure_axisY(orient='right')

        # Mostrar el gráfico combinado en la aplicación
        st.altair_chart(combined_chart, use_container_width=True)


    # En la columna de análisis, mostrar gráficos de barras para las 10 principales regiones y provincias por ganancias
    with columna_analisis:

        # Calcular las 10 principales regiones por ganancias
        top_productos_profit = df_filtered.groupby('Region')['Profit'].sum().reset_index().nlargest(10, 'Profit')

        # Calcular las 10 principales provincias por ganancias
        top_productos_category = df_filtered.groupby('Province')['Profit'].sum().reset_index().nlargest(10, 'Profit')

        # Crear gráfico de barras para las 10 principales regiones por ganancias
        chart_profit = alt.Chart(top_productos_profit).mark_bar().encode(
            alt.Y('Region:N', title='Región'),
            alt.X('Profit:Q', title='Ganancias'),
            color=alt.value('#F65300'),
            tooltip=[
                alt.Tooltip('Region:N', title='Región'),
                alt.Tooltip('Profit:Q', title='Ganancias', format=',.0f'),
            ]
        )

        # Crear gráfico de barras para las 10 principales provincias por ganancias
        chart_category = alt.Chart(top_productos_category).mark_bar(color='#F58518').encode(
            alt.Y('Province:N', title='Provincia'),
            alt.X('Profit:Q', title='Ganancias'),
            color=alt.value('#3469DE'),
            tooltip=[
                alt.Tooltip('Province:N', title='Provincia'),
                alt.Tooltip('Profit:Q', title='Ganancias', format=',.0f')],
        )

        # Combinar los dos gráficos de barras
        combined_chart = (chart_profit + chart_category).properties(width=300, height=550).configure_axis(grid=False)

        # Mostrar el gráfico combinado en la aplicación
        st.altair_chart(combined_chart, use_container_width=True)


st.write("##")
with st.container():

    # Título principal y descripción del análisis de envíos y costos por segmento de clientes y modo de envío
    st.markdown("<h1 style='text-align: center;'>Análisis de Envíos y Costos por Segmento de Clientes y Modo de Envío</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Análisis interactivo que destaca la relación entre los envíos y los costos asociados, centrándose en el segmento de clientes y el modo de envío. La información se organiza de manera intuitiva para identificar patrones y tendencias clave.</p>", unsafe_allow_html=True)
    
    # Dividir la página en dos columnas: envíos y ventas
    column_envios, column_ventas = st.columns((2,2))

    # En la columna de envíos, mostrar gráfico de barras interactivo para la cantidad de envíos por segmento de clientes
    with column_envios:

        # Calcular la cantidad total de envíos por segmento de clientes
        df_envios = filtered_df.groupby('Customer Segment')['Order Quantity'].sum().reset_index()
        df_envios_sorted = df_envios.sort_values(by='Order Quantity', ascending=False)

        # Configurar la selección interactiva para el gráfico de barras
        interval = alt.selection_single(encodings=['color'])

        # Crear gráfico de barras para la cantidad de envíos por segmento de clientes
        chart_envios = (alt.Chart(df_envios_sorted).mark_bar(color='#F58518', opacity=0.8).encode(
                x=alt.X('Customer Segment:N', title='Segmento de Clientes', sort='-y', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('Order Quantity:Q', title='Cantidad de Envíos', axis=alt.Axis(grid=False)),
                color=alt.Color("Customer Segment:N", title="Segmento de Clientes", scale=alt.Scale(domain=['Consumer', 'Corporate', 'Home Office', 'Small Business'], range=['#042259', '#FF5F00', '#3469DE', '#4C78A8'])),
                tooltip=[alt.Tooltip('Customer Segment:N', title='Segmento de Clientes'),
                         alt.Tooltip('Order Quantity:Q', title='Cantidad de Envíos', format=',.0f')]
            )
            .add_selection(interval)
            .transform_filter(interval)  
        )

        # Agregar etiquetas de texto a las barras del gráfico
        text = (
            alt.Chart(df_envios_sorted)
            .mark_text(dx=0, dy=30, color='white', fontSize=14)
            .encode(
                x=alt.X('Customer Segment:N').stack('zero'),
                y=alt.Y('Order Quantity:Q'),
                detail='Customer Segment:N',
                text=alt.Text('Order Quantity:Q', format=',.0f')
            )
        )

        # Combinar el gráfico de barras y las etiquetas de texto
        chart_envios = alt.layer(chart_envios, text).properties(width=300, height=500).configure_legend(orient='top')

        # Mostrar el gráfico interactivo en la aplicación
        st.altair_chart(chart_envios, use_container_width=True)

    with column_ventas:
        # Análisis de ventas por modo de envío
        df_ventas = filtered_df.groupby('Ship Mode')['Shipping Cost'].sum().reset_index()
        df_ventas_sorted = df_ventas.sort_values(by='Shipping Cost', ascending=False)

        # Configuración del gráfico de ventas utilizando Altair
        interval = alt.selection_single(encodings=['color'])


        # Crear el gráfico con la interactividad
        chart_ventas = (
            alt.Chart(df_ventas_sorted)
            .mark_bar(color='#4C78A8', opacity=0.8)
            .encode(
                x=alt.X('Ship Mode:N', title='Modo de Envío', axis=alt.Axis(labelAngle=0)),
                y=alt.Y('Shipping Cost:Q', title='Costo de Envío', axis=alt.Axis(grid=False)),
                color=alt.Color("Ship Mode:N", title="Modo de Envío", scale=alt.Scale(
                    domain=['Regular Air', 'Express Air', 'Delivery Truck'],
                    range=['#FF5F00', '#042259', '#3469DE']
                )),
                tooltip=[
                    alt.Tooltip('Ship Mode:N', title='Modo de Envío'),
                    alt.Tooltip('Shipping Cost:Q', title='Costo de Envío', format=',.0f')
                ]
            )
            .add_selection(interval)
            .transform_filter(interval)  # Filtrar los datos según la selección de intervalo
        )

        text = (
            alt.Chart(df_ventas_sorted)
            .mark_text(dx=0, dy=30, color='white', fontSize=14)
            .encode(
                x=alt.X('Ship Mode:N').stack('zero'),
                y=alt.Y('Shipping Cost:Q'),
                detail='Ship Mode:N',
                text=alt.Text('Shipping Cost:Q', format=',.0f')
            )
        )

        # Añadir la configuración directamente al gráfico de capas
        chart_ventas = alt.layer(chart_ventas, text).properties(width=300, height=500).configure_legend(orient='top')

        # Mostrar el gráfico con Streamlit
        st.altair_chart(chart_ventas, use_container_width=True)

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





