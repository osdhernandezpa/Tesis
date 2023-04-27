from funciones import *

def graficador(resultados,
               puntos=0,
               num_bandas=6,
               pola='te',
               texto=0,
               param_red=0.0,
               rango=0.0,
               mostrar_velocidades=False
              ):
    
    if isinstance(texto, int):
        texto = { 'bandas' : { 'titulo' : lambda track,pola,identidad: 
                                             str(track+1) + " bandas " + pola.upper() + " con " + identidad,
                                 'ejex' : lambda _: 'Vector de onda (ka/2pi)',
                                 'ejey' : lambda _: 'Frecuencia (wa/2pic)'
                             },
                    'vels' : { 'titulo' : lambda track,pola,identidad: 
                                             "Velocidades de grupo para " + str(track+1) + " bandas "
                                             + pola.upper() + " con " + identidad,
                                 'ejex' : lambda _: 'Vector de onda (ka/2pi)',
                                 'ejey' : lambda _: 'Frecuencia (wa/2pic)'
                             }
                }
    
    if (pola=='te'):
        llaves = ['tefreqs', 'tevels',  'Ancho TE', 'Promedio TE', 'Porcentaje TE']
    elif (pola=='tm'):
        llaves = ['tmfreqs', 'tmvels',  'Ancho TM', 'Promedio TM', 'Porcentaje TM']
    
    try:
        with open('resultados-' + resultados + '.pkl', 'rb') as f:
            resultados = pickle.load(f)
    except:
        try:
            with open(resultados + '/resultados-' + resultados + '.pkl', 'rb') as f:
                resultados = pickle.load(f)
        except:
            pass
    
    if isinstance(puntos, int): puntos = resultados['puntos']
    
    if (param_red != 0.0):
        resultados = traductor(param_red, resultados)

    def func_indice(valor): 
        try:
            indice = int(np.where(puntos == valor)[0][0])
        except:
            indice = puntos.index(valor)
        return indice
    
    def graf_bandas(valor, num_bandas, track=num_bandas-1):
        indice = func_indice(valor)
        fig, ax = plt.subplots()
        for i in range(track+1):
            k_vector = np.linspace(-0.5, 0.5, int(len(resultados[llaves[0]][indice][i])))
            ax.scatter(k_vector, resultados[llaves[0]][indice][i], c='r', s=0.1)
        
        parametros = resultados['parametros'][indice]
        identidad = str(parametros[0])
        for i in range(len(parametros)-1):
            identidad = identidad + '-' + str(parametros[i+1])

        ax.set_xlabel(texto['bandas']['ejex'](0))
        ax.set_ylabel(texto['bandas']['ejey'](0))
        ax.set_title(texto['bandas']['titulo'](track,pola,identidad))
        
        if (rango != 0.0):
            ax.set_ylim(rango)

        plt.show()
    
    def graf_vels(valor, num_bandas, track=num_bandas-1):
        indice = func_indice(valor)
        fig, ax = plt.subplots()
        for i in range(track+1):
            k_vector = np.linspace(-0.5, 0.5, int(len(resultados[llaves[1]][indice][i])))
            ax.scatter(k_vector, resultados[llaves[1]][indice][i], c='r', s=0.1)
        
        parametros = resultados['parametros'][indice]
        identidad = str(parametros[0])
        for i in range(len(parametros)-1):
            identidad = identidad + '-' + str(parametros[i+1])

        ax.set_xlabel(texto['vels']['ejex'](0))
        ax.set_ylabel(texto['vels']['ejey'](0))
        ax.set_title(texto['vels']['titulo'](track,pola,identidad))
        
        if (rango != 0.0):
            ax.set_ylim(rango)

        plt.show()
   
    graf_bandas(puntos[0],6)
    if (mostrar_velocidades==True):
        graf_vels(puntos[0],6)

    return resultados

resultados = graficador('punto-2.41-1.0-0.81-0.19')

#print(resultados['gaps'])




