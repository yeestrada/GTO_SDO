import arff, csv
import statistics as stats
from csv import reader
import numpy as np
import rpy2.robjects as R
import rpy2.robjects.packages as R_packages
from rpy2.robjects import DataFrame
from translation import tr as _, lang
import GTO

R.r['options'](warn=-1)

# Importando librerias
R_fitdistrplus, R_actuar = R.packages.importr('fitdistrplus'), R.packages.importr('actuar')
R_gofstat = R.r['gofstat']

distributions = [
    ('norm', R.r['rnorm']),
    ('logis', R.r['rlogis']),
    ('llogis', R.r['rllogis']),
    ('exp', R.r['rexp']),
    ('gamma', R.r['rgamma']),
    ('weibull', R.r['rweibull']),
    ('lnorm', R.r['rlnorm']),
    ('geom', R.r['rgeom']),
    ('pois', R.r['rpois']),
    ('cauchy', R.r['rcauchy']),
    ('beta', R.r['rbeta']),
    ('nbinom', R.r['rnbinom']),
    ('phyper', R.r['rhyper']),
    ('f', R.r['rf'], {'start': DataFrame({'df1': 1, 'df2': 1})}),
    ('t', R.r['rt'], {'start': DataFrame({'df': 1})}),
    ('binom', R.r['rbinom'], {'start': DataFrame({'prob': 0.5})}),
    ('wilcox', R.r['rwilcox'], {'start': DataFrame({'m': 1, 'n': 1})}),
    ('chisq', R.r['rchisq'], {'start': DataFrame({'df': 1})})
]


def rows_to_columns(data):
    items = np.transpose(data).tolist()
    data_type, round = [], []
    for line in items:
        if isinstance(line, list):
            is_float = len([i for i in line if '.' in i])
            data_type.append('integer' if len(line) - is_float > is_float else 'float')
            num = stats.mode([len(j[j.find('.') + 1:]) for j in [i for i in line if '.' in i]]) if is_float else 0
        else:
            is_float = isinstance(line, float)
            data_type.append('float' if isinstance(line, float) else 'integer')
            num = len(str(line)[str(line).find('.') + 1:])
        round.append(num)

    return items, data_type, round


# @summary: Genera datos aleatorios
# @param data: Contiene los datos de la distribución
# seleccionada @param size: Cantidad de elementos a generar @param repeated: Si se detecta que la
# columna contiene solo un elemento repetido, se mantiene el mismo elemento
def get_random_data_r(data, size, repeated=None):
    try:
        if repeated is not None: return [repeated for i in range(size)]
        return data['dist'][1](int(size), **data['args'])
    except Exception as e:
        print(e)


# @summary: Cargar los datos y los separar en clases
# @param filename: Nombre del fichero
# @param column: Columna que identifica a que clase pertenece cada registro
def load_data(file_name, column=-1):
    data = {'a': [], 'b': [], 'max': None, 'min': None, 'all': [], 'min_col': 1}
    with open(file_name, 'r') as obj:
        csv_reader = reader(obj)
        column_class_a = None
        for row in csv_reader:
            data['all'].append(row[:])
            selector = row[column]
            if column_class_a is None: column_class_a = selector
            row.pop()
            data['a'].append(row) if selector == column_class_a else data['b'].append(row)

    data['max'] = 'a' if len(data['a']) > len(data['b']) else 'b'
    data['min'] = 'a' if len(data['a']) < len(data['b']) else 'b'
    data['min_col'] = selector if len(data['a']) > len(data['b']) else int(not int(selector))
    return data


# @summary: Almacenar los datos generados
# @param file_name: Nombre del fichero donde se almacenan los datos
# @param data_to_save: Datos generados para almacenar
# @param data_type: Tipos de datos por columnas
# @param round_to: Decimales por columna a los que se debe redondear los valores
# @param prev_data: Datos iniciales que fueron cargados
# @param min_col: valor identificador de la clase minoritaria
def save_data(file_name, data_to_save, data_type, round_to, prev_data=None, min_col=1, is_AGT=False):
    try:
        # for i in range(len(data_type)):
        #     string = str(np.around(data_to_save[i], round_to[i]))
        #     data_to_save[i] = string
        for i in range(len(data_type)):
            for j in range(len(data_to_save[i])):
                string = round(data_to_save[i][j], round_to[i])
                data_to_save[i][j] = string

        data = np.transpose(data_to_save).tolist()

        for i in range(len(data)): data[i].append(min_col)

        # if prev_data is not None: data = data + prev_data
        with open(file_name, 'w', newline='') as file:
            csv_writer = csv.writer(file)
            for row in data: csv_writer.writerow(row)
            for row in prev_data: csv_writer.writerow(row)
        return True
    except Exception as e:
        print(e)
        return False


# @summary: Ajusta los datos, obteniendo los valores que mejor se ajustan.
# @param items: Conjunto de datos
# @param data_type: Tipo mayoritario del conjunto de datos
# @param distribution: Distribución a la cual se desea ajustar
def get_fitdistr(items, data_type, distribution):
    data = {}
    args = distribution[2] if len(distribution) > 2 else {}
    t = R.FloatVector(items) if data_type == 'float' else R.IntVector(items)
    while True:
        try:
            response = R_fitdistrplus.fitdist(t, distribution[0], **args)
            break
        except Exception as e:
            return None, None

    if distribution[0] == 'norm':
        data['mean'], data['sd'] = response[0]
    elif distribution[0] == 'exp':
        data['rate'] = response[0][0]
    elif distribution[0] == 'geom':
        data['prob'] = response[0][0]
    elif distribution[0] == 'pois':
        data['lambda'] = response[0][0]
    elif distribution[0] == 'cauchy':
        data['location'], data['scale'] = response[0]
    elif distribution[0] == 'gamma':
        data['shape'], data['rate'] = response[0]
    elif distribution[0] == 'lnorm':
        data['meanlog'], data['sdlog'] = response[0]
    elif distribution[0] == 'logis':
        data['location'], data['scale'] = response[0]
    elif distribution[0] == 'llogis':
        data['shape'], data['scale'] = response[0]
    elif distribution[0] == 'weibull':
        data['shape'], data['scale'] = response[0]
    elif distribution[0] == 'unif':
        data['min'], data['max'] = response[0]
    elif distribution[0] == 'beta':
        data['shape1'], data['shape2'] = response[0]
    elif distribution[0] == 'f':
        data['df1'], data['df2'] = response[0]
    elif distribution[0] == 't':
        data['df'] = response[0]
    elif distribution[0] == 'binom':
        data['size'], data['prob'] = response[0]
    elif distribution[0] == 'nbinom':
        data['mu'], data['size'] = response[0]
    elif distribution[0] == 'hyper':
        data['m'], data['n'], data['k'] = response[0]
    elif distribution[0] == 'wilcox':
        data['m'], data['n'] = response[0]
    elif distribution[0] == 'chisq':
        data['df'] = response[0]

    return data, response


# @summary: Realiza las pruebas de bondad a los datos dados según una distribución dada
# @param fit_dist_result: Parámetros resultantes de ajustar la distribución
# @param difference_umbral: umbral de diferencia
# @param distribution: Distribución a la cual se hará brueba de bondad
# @param args: listado de argumentos
def gofstat(fit_dist_result, distribution, args):
    response = []
    try:
        val = R_gofstat(fit_dist_result)
        data = dict(zip(val.names, val))
        response.append(({'ad': list(data['ad'])[0],
                          'ks': list(data['ks'])[0],
                          'cvm': list(data['cvm'])[0],
                          'aic': list(data['aic'])[0],
                          'bic': list(data['bic'])[0]}, distribution, args))
        return response
    except Exception as e:
        print(e)
        return []


# @summary: Selecciona la distribución que mejor se ajusta
# @param values: valores resultantes de $gofstat$
# @param difference_umbral: umbral de diferencia
# @param test: prueba que se debe usar (ad,ks,cvm)
# @param check_test: criterio de a utilizar (aic, bic)
def selectAIC(values, difference_umbral=0.01, test='all', check_test='aic'):
    try:
        minor_val = None
        # Por cada resultado de pruebas para cada distribución
        for v in values:
            # Se seleccionan las variable siguientes
            ad, ks, cvm, aic, bic = v[0]['ad'], v[0]['ks'], v[0]['cvm'], v[0]['aic'], v[0]['bic']
            # Inicialmente se toma el primero de los resultados
            if minor_val is None:
                minor_val = {'ad': ad, 'ks': ks, 'cvm': cvm, 'aic': aic, 'Average': (ad + ks + cvm)/3,
                             'bic': bic, 'dist': v[1], 'args': v[2]}
            elif test == _[lang]['average']:
                if ad + ks + cvm < minor_val['ad'] + minor_val['ks'] + minor_val['cvm']:
                    minor_val = {'ad': ad, 'ks': ks, 'cvm': cvm, 'aic': aic, 'Average': (ad + ks + cvm)/3,
                                 'bic': bic, 'dist': v[1], 'args': v[2]}

            # si existe alguno con iguales de resultados
            elif abs(locals()[test] - minor_val[test]) < difference_umbral:
                # se valida segun el criterio seleccionado
                if locals()[check_test] < minor_val[check_test]:
                    minor_val = {'ad': ad, 'ks': ks, 'cvm': cvm, 'aic': aic, 'Average': (ad + ks + cvm)/3,
                                 'bic': bic, 'dist': v[1], 'args': v[2]}
            elif locals()[test] < minor_val[test]:
                minor_val = {'ad': ad, 'ks': ks, 'cvm': cvm, 'aic': aic, 'Average': (ad + ks + cvm)/3,
                             'bic': bic, 'dist': v[1], 'args': v[2]}
        return minor_val
    except Exception as e:
        print(e)


# ----------------funciones visuales ------------------------------------
# @summary: Identifica las distribuciones para cada columna de un conjunto de datos
# @param fixed_data: datos a los cuales se les busca su distribuciión
# @param data_type: tipos d datos por columnas
# @param difference_umbral: umbral de diferencia
# @param prueba: prueba que se debe usar (ad,ks,cvm)
# @param check_test: criterio de a utilizar (aic, bic)
def getDistributionInfo(fixed_data, data_type, difference_umbral, test, criteria):
    selected_values = []

    # Por cada lista de numeros en la columna
    for i in range(len(fixed_data)):
        vector = R.FloatVector(fixed_data[i]) if 'float' in data_type[i] else R.IntVector(fixed_data[i])
        values = []

        for j in distributions:
            # se llama get_fitdistr con o sin argumentos
            data, response = get_fitdistr(vector, data_type[i], j)

            # si la distribucion retorna algun error, devuelve el valor None
            if data is None: continue
            # Se adiciona el mayor valor de pvalue para la dist corresp, en caso de devolver un
            # error retorna None
            values += gofstat(response, j, data)

        # Se limpian los valores None que dieron errores
        values = [e for e in values if e is not None]

        # verificar si son valores repetidos en la columna si es asi significa que no se aproxima
        # a ninguna distribucion estadistica y se genera el mismo numero
        repeated = vector[0] if len([e for e in vector if e == vector[0]]) == len(vector) else None

        if repeated is None:
            selected = selectAIC(values, difference_umbral, test, criteria)
            selected_values.append(selected)
        else:
            selected_values.append({'dist': (_[lang]['repeated_value'].format(repeated),)})

    return selected_values


# @summary: Genera datos haciendo uso del resto de las funcionalidades
# @param fixed_data: datos a los cuales se les busca su distribuciión
# @param data_type: tipos de datos por columnas
# @param fdata: resultados de load_data
# @param difference_umbral: umbral de diferencia
# @param prueba: prueba que se debe usar (ad,ks,cvm)
# @param check_test: criterio de a utilizar (aic, bic)
def generateData(fixed_data, data_type, fdata, difference_umbral, prueba, criterio, GTO_data=None):
    generated_data = []

    # Por cada lista de numeros en la columna
    for i in range(len(fixed_data)):
        vector = R.FloatVector(fixed_data[i]) if data_type[i] == 'float' else R.IntVector(fixed_data[i])
        values = []
        if GTO_data is not None:
            GTO_data['lower_bound'] = min(vector)
            GTO_data['upper_bound'] = max(vector)

        for j in distributions:
            # se llama get_fitdistr con o sin argumentos
            data, response = get_fitdistr(vector, data_type[i], j)

            # si la distribucion retorna algun error, devuelve el valor None
            if data is None: continue
            values += gofstat(response, j, data)

        # Se limpian los valores None que dieron errores
        values = [e for e in values if e is not None]

        repeated = vector[0] if len([e for e in vector if e == vector[0]]) == len(vector) else None

        if repeated is None:
            selected = selectAIC(values, difference_umbral, prueba, criterio)
        number = 1 if GTO_data is None else GTO_data['variables_no']
        length = (len(fdata[fdata['max']]) - len(fdata[fdata['min']]))
        valor = length * number if repeated is None else length
        response = get_random_data_r(selected, length * number if repeated is None else length, repeated)

        if GTO_data is not None and repeated is None:
            gto_data = np.array(response)
            gto_data = gto_data.reshape(number,length)
            _gto = GTO.GTOClass()
            _gto.setStatisticData(difference_umbral, prueba, criterio, data_type[i], selected)
            generated_data.append(_gto.execGTO(gto_data, number, GTO_data['max_iter'], length, GTO_data['upper_bound'], GTO_data['lower_bound']))
        else:
            generated_data.append(np.array(response))
    return generated_data
