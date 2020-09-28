import re
import pandas as pd
import numpy as np
from pandas_profiling import ProfileReport

def cuenta_tipo_de_dato(df,tipo):
    vars_type = df.dtypes
    vars_type = pd.DataFrame(vars_type, columns = ['tipo'])

    if tipo == 'numerico':
        cantidad_tipo = len(vars_type.loc[vars_type["tipo"] == "int64"])
        cantidad_tipo = cantidad_tipo + len(vars_type.loc[vars_type["tipo"] == "float64"])
    else:
        cantidad_tipo = len(vars_type.loc[vars_type["tipo"] == tipo])

    return cantidad_tipo


def cuenta_nulos_por_columnas(df):
    """
    Función que realiza una tabla con la cuenta de missing values por columna y obtiene la proporción que estos missing
    values representan del total.
    """
    valores_nulos = df.isnull().sum()
    porcentaje_valores_nulos = 100 * df.isnull().sum() / len(df)
    tabla_valores_nulos = pd.concat([valores_nulos, porcentaje_valores_nulos], axis=1)
    tabla_valores_nulos_ordenada = tabla_valores_nulos.rename(
        columns={0: 'Missing Values', 1: '% del Total'})
    tabla_valores_nulos_ordenada = tabla_valores_nulos_ordenada[
        tabla_valores_nulos_ordenada.iloc[:, 1] != 0].sort_values(
        '% del Total', ascending=False).round(1)
    print("El dataframe tiene " + str(df.shape[1]) + " columnas.\n"
                                                     "Hay " + str(tabla_valores_nulos_ordenada.shape[0]) +
          " columnas que tienen NA's.")
    return tabla_valores_nulos_ordenada


def genera_profiling_general(df):
    cuenta_de_variables = len(df.columns)
    cuenta_observaciones = len(df)
    total_celdas = cuenta_de_variables*cuenta_observaciones

    # Contamos el tipo de datos del dataset
    vars_type = df.dtypes
    vars_type = pd.DataFrame(vars_type, columns = ['tipo'])

    # Asignamos un valor para cada tipo

    ## Numéricas
    cantidad_numericas = len(vars_type.loc[vars_type["tipo"] == "int64"])
    cantidad_numericas = cantidad_numericas + len(vars_type.loc[vars_type["tipo"] == "float64"])
    #print(cantidad_numericas)

    ## Fechas
    cantidad_fecha = len(vars_type.loc[vars_type["tipo"] == "Date"])
    #print(cantidad_fecha)

    ## Categoricas
    cantidad_categoricas = len(vars_type.loc[vars_type["tipo"] == "category"])
    #print(cantidad_categoricas)

    ## Texto
    cantidad_texto = len(vars_type.loc[vars_type["tipo"] == "object"])
    #print(cantidad_texto)

    # Contamos los faltantes
    nulos_totales = cuenta_nulos_por_columnas(df)['Missing Values'].sum()
    #print(nulos_totales)

    # Obtenemos el porcentaje de datos que son faltantes
    nulos_porcentaje = ((nulos_totales/(total_celdas))*100).round(1).astype(str)+'%'
    #print(nulos_porcentaje)

    # Obtenemos el total de columnas duplicadas
    ds_duplicados = df.duplicated(subset=None, keep='first')
    ds_duplicados = pd.DataFrame(ds_duplicados,columns = ['duplicated'])
    numero_de_duplicados = len(ds_duplicados.loc[ds_duplicados["duplicated"] == True])
    #print(numero_de_duplicados)

    # Obtenemos el porcentaje de duplicados
    porcentaje_de_duplicados = str(((numero_de_duplicados/(total_celdas))*100))+'%'
    #print(porcentaje_de_duplicados)

    estadisticas = ['Total de variables','Conteo de observaciones','Total de celdas',
                        'Cantidad de variables numericas','Cantidad de variables de fecha',
                        'Cantidad de variables categóricas', 'Cantidad de variables de texto',
                        'Valores faltantes','Porcentaje de valores faltantes',
                        'Renglones duplicados', 'Porcentaje de valores duplicados']

    valores_estadisticas = [cuenta_de_variables,cuenta_observaciones,total_celdas,cantidad_numericas,
                        cantidad_fecha,cantidad_categoricas,cantidad_texto,nulos_totales,nulos_porcentaje,
                        numero_de_duplicados,porcentaje_de_duplicados]

    valores = {'Estadisticas':estadisticas,'Resultado':valores_estadisticas}

    df_perfilamiento_general = pd.DataFrame(data=valores)
    return df_perfilamiento_general

def cuenta_nulos_por_renglones(df):
    """
    Función que cuenta la cantidad de valores nulos por cada renglón, para valorar si es posible o no realizar
    imputaciones o se tendrían que tirar las columnas o renglones correspondientes.
    """
    df_aux = df.copy()
    valores_nulos_totales = sum(df_aux.apply(lambda x: sum(x.isnull().values), axis=1) > 0)
    print("Existen un total de: ", valores_nulos_totales, "renglones con al menos un valor nulo\n")
    numero_de_lineas = len(df_aux)
    porcentaje_de_lineas_con_nulos = valores_nulos_totales / numero_de_lineas
    texto = "Representan el {:.2%} del total de renglones.". \
        format(porcentaje_de_lineas_con_nulos)
    print(texto)
    return valores_nulos_totales

def cuenta_nulos_por_renglones_tabla(df):
    arreglo_nulos=[]
    arreglo_renglones=[]
    for i in range(len(df.index)):
        string = "Nan in row "+ str(i)
        valor = df.iloc[i].isnull().sum()
        arreglo_renglones.append(string)
        arreglo_nulos.append(valor)
        #print("Nan in row ", i, " : ", df.iloc[i].isnull().sum())
    sum([True for idx, row in df.iterrows() if any(row.isnull())])
    list(df.index[df.isnull().sum(axis=1) > 0])
    data={'renglon':arreglo_renglones,'valores_nulos':arreglo_nulos}
    tabla_valores_nulos_ordenada = pd.DataFrame(data=data)
    tabla_valores_nulos_ordenada_solonulos = pd.DataFrame(tabla_valores_nulos_ordenada)
    tabla_valores_nulos_ordenada_solonulos = tabla_valores_nulos_ordenada_solonulos.loc[tabla_valores_nulos_ordenada_solonulos["valores_nulos"] > 0]
    tabla_valores_nulos_ordenada_solonulos=tabla_valores_nulos_ordenada_solonulos.sort_values('valores_nulos', ascending = False)

    return tabla_valores_nulos_ordenada_solonulos.head(10)

def genera_profiling_de_numericos(df,lista_numericas,vars_type):
    # Obtenemos los estadísticos de la columna si es numérica
    lista_perfilamiento_numerico = ['tipo','numero de observaciones', 'media', 'desviacion estándar',
                                    'cuartil 25%','cuartil 50%','cuartil 75%','minimo','maximo',
                                    'numero de observaciones unicas','top5 repetidos']
    datos_dataframe_profiling_numericas = {'metrica':lista_perfilamiento_numerico}
    dataframe_profiling_numericas = pd.DataFrame(data=datos_dataframe_profiling_numericas)
    for col in lista_numericas:
        # tipo de dato
        vars_type_num = pd.DataFrame(vars_type)
        #vars_type_num
        df_tipo = pd.DataFrame(data=vars_type_num.loc[vars_type_num["variable"] == col])
        tipo_dato=df_tipo['tipo'][0]
        #print(tipo_dato)

        # Obtenemos las métricas relevantes
        descr_col = df[col].describe()
        descr_col = pd.DataFrame(descr_col)
        descr_col['metrica']=descr_col.index
        descr_col.columns=['valor','metrica']

        # número de observaciones
        medida = 'count'
        metrica = descr_col.loc[descr_col["metrica"] == medida]
        num_observaciones_num = metrica['valor'][0]
        #print(num_observaciones_num)

        # media
        medida = 'mean'
        metrica = descr_col.loc[descr_col["metrica"] == medida]
        media_obs_num = metrica['valor'][0]
        media_obs_num = media_obs_num.round(2)
        #print(media_obs_num)

        # desviacion estándar
        medida = 'std'
        metrica = descr_col.loc[descr_col["metrica"] == medida]
        sd_obs_num = metrica['valor'][0]
        sd_obs_num = sd_obs_num.round(2)
        #print(sd_obs_num)

        # cuartil 25
        medida = '25%'
        metrica = descr_col.loc[descr_col["metrica"] == medida]
        cuant_25_obs_num = metrica['valor'][0]
        cuant_25_obs_num = cuant_25_obs_num.round(2)
        #print(cuant_25_obs_num)

        # cuartil 50
        medida = '50%'
        metrica = descr_col.loc[descr_col["metrica"] == medida]
        cuant_50_obs_num = metrica['valor'][0]
        cuant_50_obs_num = cuant_50_obs_num.round(2)
        #print(cuant_50_obs_num)
        #cuant_50_obs_num = agua.quantile(q=0.25)
        #print(cuant_50_obs_num)

        # cuartil 75
        medida = '75%'
        metrica = descr_col.loc[descr_col["metrica"] == medida]
        cuant_75_obs_num = metrica['valor'][0]
        cuant_75_obs_num = cuant_75_obs_num.round(2)
        #print(cuant_75_obs_num)
        #cuant_75_obs_num = agua.quantile(q=0.25)
        #print(cuant_75_obs_num)

        # minimo
        medida = 'min'
        metrica = descr_col.loc[descr_col["metrica"] == medida]
        minimo_obs_num = metrica['valor'][0]
        minimo_obs_num = minimo_obs_num.round(2)
        #print(minimo_obs_num)

        # maximo
        medida = 'max'
        metrica = descr_col.loc[descr_col["metrica"] == medida]
        maximo_obs_num = metrica['valor'][0]
        maximo_obs_num = maximo_obs_num.round(2)
        #print(maximo_obs_num)

        # numero de observaciones unicas
        num_obs_unicas_obs_num = df[col].nunique()
        #print(num_obs_unicas_obs_num)

        # top 5 observaciones repetidas
        df_resultado = df[col].value_counts(dropna=True)
        df_resultado = pd.DataFrame(df_resultado)
        df_resultado.columns=['conteo_top_5']
        df_resultado=df_resultado.sort_values('conteo_top_5', ascending = False)

        top5 = df_resultado.head(5)
        #print(top5)

        # Número de observaciones con valores faltantes
        obs_faltantes_obs_num = df[col].isna().sum()
        #print(obs_faltantes_obs_num)

        datos_variable = [tipo_dato,num_observaciones_num,media_obs_num,sd_obs_num,
                          cuant_25_obs_num, cuant_50_obs_num,cuant_75_obs_num,minimo_obs_num,
                          maximo_obs_num,num_obs_unicas_obs_num,top5]
        dataframe_profiling_numericas[col]=datos_variable
    return dataframe_profiling_numericas


def genera_profiling_de_categorias(df, lista_category,vars_type):
    # Obtenemos los estadísticos de la columna si es catagorica
    lista_perfilamiento_categorico = ['tipo','numero de categorias', 'numero de observaciones',
                                      'observaciones nulas',
                                    '% observaciones nulas']
    datos_dataframe_profiling_categoricos = {'metrica':lista_perfilamiento_categorico}
    dataframe_profiling_categoricas = pd.DataFrame(data=datos_dataframe_profiling_categoricos)
    for col in lista_category:
        # tipo de dato
        vars_type_cat = pd.DataFrame(vars_type)
        #vars_type_cat
        df_tipo = pd.DataFrame(data=vars_type_cat.loc[vars_type_cat["variable"] == col])
        tipo_dato=df_tipo['tipo'][0]

        # Obtenemos las métricas relevantes
        descr_col = df[col]
        descr_col = pd.DataFrame(descr_col)
        descr_col['metrica']=descr_col.index
        descr_col.columns=['valor','metrica']

        #Numero de categorias

        num_categorias=descr_col.nunique()["valor"]

        #Numero de observaciones

        num_observaciones=len(descr_col)

        #Valores nulos

        num_obs_nulas=df[col].isna().sum()

        #%Valores nulos

        por_obs_nulas=num_obs_nulas/num_observaciones

        datos_variable = [tipo_dato,num_categorias,num_observaciones,num_obs_nulas,por_obs_nulas]
        dataframe_profiling_categoricas[col]=datos_variable
    return dataframe_profiling_categoricas


def genera_profiling_de_texto(df,lista_texto,vars_type):
    # Obtenemos los estadísticos de la columna si es catagorica
    lista_perfilamiento_txt = ['tipo','numero de observaciones', 'observaciones unicas', '% observaciones unicas',
                                    'tamano promedio','tamano minmo','tamano maximo']
    datos_dataframe_profiling_txt = {'metrica':lista_perfilamiento_txt}
    dataframe_profiling_txt = pd.DataFrame(data=datos_dataframe_profiling_txt)
    for col in lista_texto:
        # tipo de dato
        vars_type_txt = pd.DataFrame(vars_type)
        #vars_type_txt
        df_tipo = pd.DataFrame(data=vars_type_txt.loc[vars_type_txt["variable"] == col])
        tipo_dato=df_tipo['tipo'][0]

        # Obtenemos las métricas relevantes
        descr_col = df[col]
        descr_col = pd.DataFrame(descr_col)
        descr_col['metrica']=descr_col.index
        descr_col.columns=['valor','metrica']

        #Numero de observaciones

        num_observaciones=len(descr_col)

        #Observaciones unicas

        num_obs_unicas=df[col].nunique()

        #%Observaciones nulas

        por_obs_unicas=num_obs_unicas/num_observaciones

        #%Tamaño promedio
        tam_prom=df[col].str.len().mean()
        #tam_prom=agua[col].apply(len).mean()

        #%Tamaño minimo
        tam_min=df[col].str.len().min()
        #tam_min=agua[col].apply(len).min()

        #%Tamaño maximo
        tam_max=df[col].str.len().max()
        #tam_max=agua[col].apply(len).max()

        datos_variable = [tipo_dato,num_observaciones,num_obs_unicas,por_obs_unicas,tam_prom,tam_min,tam_max]
        dataframe_profiling_txt[col]=datos_variable
    return dataframe_profiling_txt


def genera_profiling_por_variable(df):
    # Dividimos variables por tipo de datos
    vars_type = df.dtypes
    vars_type = pd.DataFrame(vars_type, columns = ['tipo'])
    vars_type['variable']=vars_type.index

    # variables numericas
    variables_int = vars_type.loc[vars_type["tipo"] == "int64"]
    variables_float = vars_type.loc[vars_type["tipo"] == "float64"]
    variables_numericas = variables_int.append(variables_float, ignore_index=True)
    lista_numericas = list(variables_numericas['variable'])

    # variables fecha
    variables_date = vars_type.loc[vars_type["tipo"] == "Date"]
    lista_date = list(variables_date['variable'])

    # variables categoricas
    variables_category = vars_type.loc[vars_type["tipo"] == "category"]
    lista_category = list(variables_category['variable'])

    # variables texto
    variables_texto = vars_type.loc[vars_type["tipo"] == "object"]
    lista_texto = list(variables_texto['variable'])

    if len(lista_numericas)==0:
        profiling_numericas = "No hay variables numéricas"
    else:
        profiling_numericas = genera_profiling_de_numericos(df,lista_numericas,vars_type)

    if len(lista_category)==0:
        profiling_categoricas = "No hay variables categóricas"
    else:
        profiling_categoricas = genera_profiling_de_categorias(df,lista_category,vars_type)

    if len(lista_texto)==0:
        profiling_texto = "No hay variables de tipo texto"
    else:
        profiling_texto = genera_profiling_de_texto(df,lista_texto,vars_type)

    return (profiling_numericas,profiling_categoricas,profiling_texto)


def StringLowercase(df):
    """
    Función cambiar todos los strings de un dataframe a lowercase
    (columnas y observaciones)

    Args:
        df: dataframe al que se desea hacer la modificación
    Return:
        df: dataframe modificado
    """

    ### Columnas

    DataFrameColumns = df.columns

    for col in DataFrameColumns:
        df.rename(columns={col:col.lower()}, inplace=True)

    ### Observaciones

    filtro = df.dtypes == np.object
    objects = df.dtypes[filtro]
    StringColumns = list(objects.index)

    for col in StringColumns:
        df[col] = df[col].str.lower()

    return df

def StringAcentos(df):
    """
    Función para eliminar acentos, dieresis y eñes de los strings de un
    dataframe (columnas y observaciones)

    Args:
        df: dataframe al que se desea hacer la modificación
    Return:
        df: dataframe modificado
    """

    ### Columnas

    df.columns = df.columns.str.replace('á', 'a')
    df.columns = df.columns.str.replace('é', 'e')
    df.columns = df.columns.str.replace('í', 'i')
    df.columns = df.columns.str.replace('ó', 'o')
    df.columns = df.columns.str.replace('ú', 'u')
    df.columns = df.columns.str.replace('ü', 'u')
    df.columns = df.columns.str.replace('ñ', 'n')

    ### Observaciones

    filtro = df.dtypes == np.object
    objects = df.dtypes[filtro]
    StringColumns = list(objects.index)

    for col in StringColumns:
        df[col] = df[col].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')

    return df

def StringStrip(df):
    """
    Función para eliminar espacios al inicio y al final de los strings de un
    dataframe (columnas y observaciones)

    Args:
        df: dataframe al que se desea hacer la modificación
    Return:
        df: dataframe modificado
    """

    ### Columnas

    df.columns = [col.strip() for col in df.columns]

    ### Observaciones

    filtro = df.dtypes == np.object
    objects = df.dtypes[filtro]
    StringColumns = list(objects.index)

    for col in StringColumns:
        df[col] = df[col].apply(lambda x: x.strip() if isinstance(x, str) else x)

    return df

def StringEspacios(df):
    """
    Función para eliminar espacios dobles (o mas) de los strings de un
    dataframe (columnas y observaciones)

    Args:
        df: dataframe al que se desea hacer la modificación
    Return:
        df: dataframe modificado
    """

    ### Columnas

    df.columns = [re.sub(' +', ' ', col) for col in df.columns]

    ### Observaciones

    filtro = df.dtypes == np.object
    objects = df.dtypes[filtro]
    StringColumns = list(objects.index)

    for col in StringColumns:
        df[col] = df[col].apply(lambda x: re.sub(' +', ' ', x) if isinstance(x, str) else x)

    return df

def EstandarizaFormato(df):
    """
    Función para estandarizar un dataframe: minúsculas, sin espacios en blanco, sin signos de puntuación

    Args:
        df: dataframe al que se desea hacer la modificación
    Return:
        df: dataframe modificado
    """

    ### Quita espacios en columnas
    df.columns = df.columns.str.replace(' ', '_')

    ### Minúsculas
    df = StringLowercase(df)

    ### Acentos
    df = StringAcentos(df)

    ### Quitamos espacios al principio y al final
    df = StringStrip(df)

    ### Quitamos espacios
    df = StringEspacios(df)

    return df