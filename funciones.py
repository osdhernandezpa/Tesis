import os
import re
import numpy as np
import matplotlib.pyplot as plt
import pickle
from functools import partial

def ctl_nmat(parametros, archivo, cifras=6):
    identidad = str(parametros[0])
    for i in range(len(parametros)-1):
        identidad = identidad + '-' + str(parametros[i+1])
    
    control = open(archivo, "r")
    cypris = open("cypris-" + identidad + "x.ctl" , "w")
    for i, lines in enumerate(control.readlines(), 0):
        if i == 12:
            n = int(len(parametros)/2)
            for j in range(n):
                centro = round(sum(parametros[n:(n+j+1)])-0.5*parametros[n+j],cifras+1)
                cypris.write( "                     (make block\n" )
                cypris.write( "                       (center " + str(centro) + " 0 0) (size " + str(parametros[n+j]) + " infinity infinity)\n" )
                cypris.write( "                       (material (make dielectric (epsilon " + str(parametros[j]) + ")) ) )\n" )
        else:
            cypris.write(lines)
    control.close()
    cypris.close()




def ctl_2mat(parametros, archivo, cifras=6):
    identidad = str(parametros[0])
    for i in range(len(parametros)-1):
        identidad = identidad + '-' + str(parametros[i+1])
    
    control = open(archivo, "r")
    cypris = open("cypris-" + identidad + "x.ctl" , "w")
    for i, lines in enumerate(control.readlines(), 0):
        if i == 12:
            cypris.write( "                       (center " + str(round(0.5*parametros[2],cifras+1)) + " 0 0) (size " + str(parametros[2]) + " infinity infinity)\n" )
        elif i == 13:
            cypris.write( "                       (material (make dielectric (epsilon " + str(parametros[0]) + ")) ) )\n" )
        elif i == 15:
            cypris.write( "                       (center " + str(round(parametros[2]+0.5*parametros[3],cifras+1)) + " 0 0) (size " + str(parametros[3]) + " infinity infinity)\n" )
        elif i == 16:
            cypris.write( "                       (material (make dielectric (epsilon " + str(parametros[1]) + ")) ) ) ))\n" )
        else:
            cypris.write(lines)
    control.close()
    cypris.close()


def ctl_3mat(parametros, archivo, cifras=6):
    identidad = str(parametros[0])
    for i in range(len(parametros)-1):
        identidad = identidad + '-' + str(parametros[i+1])

    control = open(archivo, "r")
    cypris = open("cypris-" + identidad + "x.ctl" , "w")
    for i, lines in enumerate(control.readlines(), 0):
        if i == 12:
            cypris.write( "                       (center " + str(round(0.5*parametros[3],cifras+1)) + " 0 0) (size " + str(parametros[3]) + " infinity infinity)\n" )
        elif i == 13:
            cypris.write( "                       (material (make dielectric (epsilon " + str(parametros[0]) + ")) ) )\n" )
        elif i == 15:
            cypris.write( "                       (center " + str(round(parametros[3]+0.5*parametros[4],cifras+1)) + " 0 0) (size " + str(parametros[4]) + " infinity infinity)\n" )
        elif i == 16:
            cypris.write( "                       (material (make dielectric (epsilon " + str(parametros[1]) + ")) ) )\n" )
        elif i == 18:
            cypris.write( "                       (center " + str(round(parametros[3]+parametros[4]+0.5*parametros[5],cifras+1)) + " 0 0) (size " + str(parametros[5]) + " infinity infinity)\n" )
        elif i == 19:
            cypris.write( "                       (material (make dielectric (epsilon " + str(parametros[2]) + "))))))\n" )
        else:
            cypris.write(lines)
    control.close()
    cypris.close()

def ctl_lineal(parametros, archivo):
    identidad = str(parametros[0])
    for i in range(len(parametros)-1):
        identidad = identidad + '-' + str(parametros[i+1])

    control = open(archivo, "r")
    cypris = open("cypris-" + identidad + "x.ctl" , "w")
    for i, lines in enumerate(control.readlines(), 0):
        if i == 12:
            cypris.write( "(define-param index-max " + str(parametros[0]) + ")\n" )
        else:
            cypris.write(lines)
    control.close()
    cypris.close()

def ctl_num(parametros, archivo):
    identidad = str(parametros[0])
    for i in range(len(parametros)-1):
        identidad = identidad + '-' + str(parametros[i+1])

    control = open(archivo, "r")
    nombre_final = "cypris-" + identidad + "x.ctl"
    cypris = open(nombre_final , "w")
    for i, lines in enumerate(control.readlines(), 0):
        if i == 0:
            cypris.write("(set! num-bands " + str(parametros[0]) + ")\n")
        elif i == 2:
            cypris.write( "(set! resolution " + str(parametros[1]) + ")\n" )
        elif i == 4:
            cypris.write( "(set! mesh-size " + str(parametros[2]) + ")\n" )
        elif i == 9:
            cypris.write( "(set! k-points (interpolate " + str(parametros[3]) + " k-points))\n" )
        else:
            cypris.write(lines)
    control.close()
    cypris.close()

    return nombre_final

def run(parametros, direccion=''):
    identidad = str(parametros[0])
    for i in range(len(parametros)-1):
        identidad = identidad + '-' + str(parametros[i+1])

    try:
        print("mpb cypris-" + identidad  + "x.ctl > cypris-" + identidad +  ".out")
        os.system("mpb cypris-" + identidad  + "x.ctl > cypris-" + identidad +  ".out")

        print("grep tefreqs cypris-" + identidad + ".out > cypris-" + identidad + ".te.dat")
        os.system("grep tefreqs cypris-" + identidad + ".out > cypris-" + identidad + ".te.dat")

        print("grep tevelocity cypris-" + identidad + ".out > cypris-" + identidad + ".tevel.dat")
        os.system("grep tevelocity cypris-" + identidad + ".out > cypris-" + identidad + ".tevel.dat")

        print("grep tmfreqs cypris-" + identidad + ".out > cypris-" + identidad + ".tm.dat")
        os.system("grep tmfreqs cypris-" + identidad + ".out > cypris-" + identidad + ".tm.dat")

        print("grep tmvelocity cypris-" + identidad + ".out > cypris-" + identidad + ".tmvel.dat")
        os.system("grep tmvelocity cypris-" + identidad + ".out > cypris-" + identidad + ".tmvel.dat")

        print("grep Gap cypris-" + identidad + ".out > cypris-" + identidad + ".gap.dat") 
        os.system("grep Gap cypris-" + identidad + ".out > cypris-" + identidad + ".gap.dat") 
        print()

    except:
        print("mpb " + direccion + "/cypris-" + identidad  + "x.ctl > " + direccion + "/cypris-" + identidad +  ".out")
        os.system("mpb " + direccion + "/cypris-" + identidad  + "x.ctl > " + direccion + "/cypris-" + identidad +  ".out")

        print("grep tefreqs " + direccion + "/cypris-" + identidad + ".out > " + direccion + "/cypris-" + identidad + ".te.dat")
        os.system("grep tefreqs " + direccion + "/cypris-" + identidad + ".out > " + direccion + "/cypris-" + identidad + ".te.dat")

        print("grep tevelocity " + direccion + "/cypris-" + identidad + ".out > " + direccion + "/cypris-" + identidad + ".tevel.dat")
        os.system("grep tevelocity " + direccion + "/cypris-" + identidad + ".out > " + direccion + "/cypris-" + identidad + ".tevel.dat")

        print("grep tmfreqs " + direccion + "/cypris-" + identidad + ".out > " + direccion + "/cypris-" + identidad + ".tm.dat")
        os.system("grep tmfreqs " + direccion + "/cypris-" + identidad + ".out > " + direccion + "/cypris-" + identidad + ".tm.dat")

        print("grep tmvelocity " + direccion + "/cypris-" + identidad + ".out > " + direccion + "/cypris-" + identidad + ".tmvel.dat")
        os.system("grep tmvelocity " + direccion + "/cypris-" + identidad + ".out > " + direccion + "/cypris-" + identidad + ".tmvel.dat")

        print("grep Gap " + direccion + "/cypris-" + identidad + ".out > " + direccion + "/cypris-" + identidad + ".gap.dat") 
        os.system("grep Gap " + direccion + "/cypris-" + identidad + ".out > " + direccion + "/cypris-" + identidad + ".gap.dat") 
        
        print("mv cypris-" + identidad  + "x-epsilon.h5 " + direccion + "/")
        os.system("mv cypris-" + identidad  + "x-epsilon.h5 " + direccion + "/")

        print()
       

def freqs(parametros, pola='te', directorio=''):
    identidad = str(parametros[0])
    for i in range(len(parametros)-1):
        identidad = identidad + '-' + str(parametros[i+1])

    try:
        freqs = open("cypris-" + identidad + "." + pola + ".dat", "r")
    except:
        freqs = open(directorio + "/cypris-" + identidad + "." + pola + ".dat", "r")

    freqs_parte = freqs.readlines()
    freqs_parte = freqs_parte[1:int(len(freqs_parte))]

    for i, lines in enumerate(freqs_parte,0):
        freqs_parte[i] = freqs_parte[i].split()
        freqs_parte[i] = freqs_parte[i][6:int(len(freqs_parte[i]))]
        for j in range(len(freqs_parte[i])):
            freqs_parte[i][j] = float(freqs_parte[i][j].split(",")[0])

    pola_freqs = np.array(freqs_parte).transpose()

    return pola_freqs

def vels(parametros, pola='te', directorio=''):
    identidad = str(parametros[0])
    for i in range(len(parametros)-1):
        identidad = identidad + '-' + str(parametros[i+1])

    try:
        vels = open("cypris-" + identidad + "." + pola + "vel.dat", "r")
    except:
        vels = open(directorio + "/cypris-" + identidad + "." + pola + "vel.dat", "r")

    vels_parte = vels.readlines()
    #vels_parte = vels_parte[1:int(len(vels_parte))]
    
    for i, lines in enumerate(vels_parte,0):
        vels_parte[i] = re.split(r'#', vels_parte[i])
        vels_parte[i] = vels_parte[i][1:len(vels_parte[i])]
        for j in range(len(vels_parte[i])):
            vels_parte[i][j] = float(vels_parte[i][j][1:int(len(vels_parte[i][j])-10)])
    
    pola_vels = np.array(vels_parte).transpose()

   
#    for i, lines in enumerate(vels_parte,0):
#        vels_parte[i] = vels_parte[i].split()
#        vels_parte[i] = vels_parte[i][6:int(len(vels_parte[i]))]
#        for j in range(len(vels_parte[i])):
#            vels_parte[i][j] = float(vels_parte[i][j].split(",")[0])

#    pola_vels = np.array(vels_parte).transpose()

    return pola_vels


def gaps(parametros, num_bandas=6, directorio=''):
    identidad = str(parametros[0])
    for i in range(len(parametros)-1):
        identidad = identidad + '-' + str(parametros[i+1])

    try:
        gaps = open("cypris-" + identidad + ".gap.dat" , "r")
    except:
        gaps = open(directorio + "/cypris-" + identidad + ".gap.dat" , "r")

    gaps_parte = gaps.readlines()

    gaps_todos = []
    proms_todos = []
    porcents_todos = []

    for i, lines in enumerate(gaps_parte,0):
        gaps_parte[i] = gaps_parte[i].split()

    for i in range(2*(num_bandas-1)):
        contador = 0
        for j in range ( int(len(gaps_parte)) ):
            if ( int(gaps_parte[j][3]) == (i+1)):
                gaps_todos.append( float(gaps_parte[j][8].split("(")[1].split(")")[0]) - float(gaps_parte[j][4].split("(")[1].split(")")[0]) )
                proms_todos.append( 0.5*(float(gaps_parte[j][8].split("(")[1].split(")")[0]) + float(gaps_parte[j][4].split("(")[1].split(")")[0]) ) )
                porcents_todos.append( float(gaps_parte[j][9].split("%")[0]) )
                contador = contador + 1

        if (contador == 0):
            gaps_todos.append(0.0)
            proms_todos.append(0.0)
            porcents_todos.append(0.0)
            gaps_todos.append(0.0)
            proms_todos.append(0.0)
            porcents_todos.append(0.0)

        # no distingue entre te y tm
        # esto no es relevante en 1d
        if (contador == 1):
            gaps_todos.append(0.0)
            proms_todos.append(0.0)
            porcents_todos.append(0.0)

    gaps_te = [gaps_todos[2*i] for i in range(num_bandas-1)]
    proms_te = [proms_todos[2*i] for i in range(num_bandas-1)]
    porcents_te = [porcents_todos[2*i] for i in range(num_bandas-1)]
    gaps_tm = [gaps_todos[2*i+1] for i in range(num_bandas-1)]
    proms_tm = [proms_todos[2*i+1] for i in range(num_bandas-1)]
    porcents_tm = [porcents_todos[2*i+1] for i in range(num_bandas-1)]
    
    return [gaps_te, proms_te, porcents_te, gaps_tm, proms_tm, porcents_tm]

def mover_punto(parametros, directorio):
    identidad = str(parametros[0])
    for i in range(len(parametros)-1):
        identidad = identidad + '-' + str(parametros[i+1])

    try:
        print("Guardando punto: ")
        print("mv cypris-" + identidad  + "x.ctl " + directorio + "/")
        os.system("mv cypris-" + identidad  + "x.ctl " + directorio + "/")

        print("mv cypris-" + identidad  + "x-epsilon.h5 " + directorio + "/")
        os.system("mv cypris-" + identidad  + "x-epsilon.h5 " + directorio + "/")

        print("mv cypris-" + identidad + ".out " + directorio + "/")
        os.system("mv cypris-" + identidad + ".out " + directorio + "/")
    
        print("mv cypris-" + identidad + ".te.dat " + directorio + "/")
        os.system("mv cypris-" + identidad + ".te.dat " + directorio + "/")
    
        print("mv cypris-" + identidad + ".tevel.dat " + directorio + "/")
        os.system("mv cypris-" + identidad + ".tevel.dat " + directorio + "/")

        print("mv cypris-" + identidad + ".tm.dat " + directorio + "/")
        os.system("mv cypris-" + identidad + ".tm.dat " + directorio + "/")
    
        print("mv cypris-" + identidad + ".tmvel.dat " + directorio + "/")
        os.system("mv cypris-" + identidad + ".tmvel.dat " + directorio + "/")
    
        print("mv cypris-" + identidad + ".gap.dat " + directorio + "/")
        os.system("mv cypris-" + identidad + ".gap.dat " + directorio + "/")
        print()
        print()
    except:
        print("Error moviendo archivos a " + str(directorio) + ": ")
        print("Id: " + identidad)


def balance_proporcional3(matriz,puntos,material,cifras):
    material = material - 1
    cont_dim = matriz[0][((material+1)%3)+3] / matriz[0][((material+2)%3)+3]
    for i in range(len(matriz)):
        matriz[i][((material+2)%3)+3] = round(( (1-puntos[i])/(1+cont_dim) ),cifras)
        matriz[i][((material+1)%3)+3] = round(cont_dim*matriz[i][((material+2)%3)+3],cifras)
    return matriz

def balance_proporcional2(matriz,puntos,material,cifras):
    for i in range(len(matriz)):
        matriz[i][((material+2)%2)+2] = round( (1.0-matriz[i][((material+1)%2)+2]) ,cifras)
    return matriz




def default(nada=0): return nada
def rutina(num_bandas=6,
           archivo_control='control-2mat.ctl',
           control=[2.35,1.0,0.81,0.19],
           puntos=[2.35],
           tipo=['2mat',0], # num, mat o lineal. indice (en control) para introduccion
                            # usar indice mayor a tamanho de control para omitir remplazo
           cifras=2, # solo se usa para el balance de proporciones
           nombre='rutina',
           funcion=default # obligatorio para balance dimensional
                           # hace posible lista de parametros mas exotica
          ):
    track = num_bandas - 1

    parametros = [[0 for column in range(len(control))] for fila in range(len(puntos))]
    for fila in range(len(puntos)):
        for colum in range(len(control)):
            parametros[fila][colum] = control[colum]
    
    try:    
        for i in range(len(puntos)):
            parametros[i][tipo[1]] = puntos[i]
    except:
        pass

    parametros = funcion(parametros)

    try:
        os.system("mkdir " + str(nombre))
    except:
        pass
    
    tefreqs = []
    tmfreqs = []
    tevels = []
    tmvels = []
    ancho_te = np.zeros(( track , len(puntos) ))
    prom_te = np.zeros(( track , len(puntos) ))
    porcent_te = np.zeros(( track , len(puntos) ))
    ancho_tm = np.zeros(( track , len(puntos) ))
    prom_tm = np.zeros(( track , len(puntos) ))
    porcent_tm = np.zeros(( track , len(puntos) ))    
    for i in range(len(puntos)):
        if (tipo[0] == 'num'):
            ctl_num(parametros[i], archivo_control)
        elif (tipo[0] == '2mat'):
            ctl_2mat(parametros[i], archivo_control, cifras=cifras+1)
        elif (tipo[0] == '3mat'):
            ctl_3mat(parametros[i], archivo_control, cifras=cifras+1)
        elif (tipo[0] == 'lineal'):
            ctl_lineal(parametros[i], archivo_control)       
        
#        run(parametros[i])
        run(parametros[i], nombre)
        mover_punto(parametros[i],  nombre)
        tefreqs.append(freqs(parametros[i], 'te', nombre))
        tmfreqs.append(freqs(parametros[i], 'tm', nombre))
        tevels.append(vels(parametros[i], 'te', nombre))
        tmvels.append(vels(parametros[i], 'tm', nombre))
        gaps_vector = gaps(parametros[i], num_bandas, nombre)
        
        for j in range(track):
            ancho_te[:,i][j] = gaps_vector[0][j]
            prom_te[:,i][j] = gaps_vector[1][j]
            porcent_te[:,i][j] = gaps_vector[2][j]
            ancho_tm[:,i][j] = gaps_vector[3][j]
            prom_tm[:,i][j] = gaps_vector[4][j]
            porcent_tm[:,i][j] = gaps_vector[5][j]
    
    resultados = {'puntos' : puntos,
                  'parametros' : parametros,
                  'tefreqs' : tefreqs,
                  'tmfreqs' : tmfreqs,
                  'tevels' : tevels,
                  'tmvels' : tmvels,
                  'gaps' : {'Ancho TE' : ancho_te,
                            'Promedio TE' : prom_te,
                            'Porcentaje TE' : porcent_te,
                            'Ancho TM' : ancho_tm,
                            'Promedio TM' : prom_tm,
                            'Porcentaje TM' : porcent_tm
                           }
                 }

    with open('resultados-' + str(nombre) + '.pkl', 'wb') as f:
        pickle.dump(resultados, f)
    #os.system('mv ' + 'resultados-' + str(nombre) + '.pkl ' +  str(nombre))

    return resultados
    
def rutina_doble(num_bandas=6,
           archivo_control='control-2mat.ctl',
           control=[2.35,1.0,0.81,0.19], 
           puntos1=[2.35],
           puntos2=[0.81],
           tipo=['2mat',0,2], # num, mat o lineal. indice (en control) para introduccion   
           cifras=2, # solo se usa para el balance de proporciones
           nombre='rutina',
           funcion=default
          ):
    track = num_bandas - 1

    grilla1 , grilla2 = np.meshgrid(puntos1, puntos2)

    lista = []
    for i in range(len(puntos2)):
        for j in range(len(puntos1)):
            lista.append([grilla1[i][j], grilla2[i][j]])

    parametros = [[0 for column in range(len(control))] for fila in range(len(lista))]    
    for fila in range(len(lista)):
        for colum in range(len(control)):
            parametros[fila][colum] = control[colum]

    try: 
        for i in range(len(lista)):
            parametros[i][tipo[1]] = lista[i][0]
        for i in range(len(lista)):
            parametros[i][tipo[2]] = lista[i][1]
    except:
        pass
  
    parametros = funcion(parametros)

    try:
        os.system("mkdir " + str(nombre))
    except:
        pass
    
    tefreqs = []
    tmfreqs = []
    tevels = []
    tmvels = []
    ancho_te = np.zeros(( track , len(lista) ))
    prom_te = np.zeros(( track , len(lista) ))
    porcent_te = np.zeros(( track , len(lista) ))
    ancho_tm = np.zeros(( track , len(lista) ))
    prom_tm = np.zeros(( track , len(lista) ))
    porcent_tm = np.zeros(( track , len(lista) ))    
    for i in range(len(lista)):
        if (tipo[0] == 'num'):
            ctl_num(parametros[i], archivo_control)
        elif (tipo[0] == '2mat'):
            ctl_2mat(parametros[i], archivo_control, cifras=cifras)
        elif (tipo[0] == '3mat'):
            ctl_3mat(parametros[i], archivo_control, cifras=cifras)
        elif (tipo[0] == 'lineal'):
            ctl_lineal(parametros[i], archivo_control)       
        
#        run(parametros[i])
        run(parametros[i], nombre)
        mover_punto(parametros[i],  nombre)
        tefreqs.append(freqs(parametros[i], 'te', nombre))
        tmfreqs.append(freqs(parametros[i], 'tm', nombre))
        tevels.append(vels(parametros[i], 'te', nombre))
        tmvels.append(vels(parametros[i], 'tm', nombre))
        gaps_vector = gaps(parametros[i], num_bandas, nombre)
        
        for j in range(track):
            ancho_te[:,i][j] = gaps_vector[0][j]
            prom_te[:,i][j] = gaps_vector[1][j]
            porcent_te[:,i][j] = gaps_vector[2][j]
            ancho_tm[:,i][j] = gaps_vector[3][j]
            prom_tm[:,i][j] = gaps_vector[4][j]
            porcent_tm[:,i][j] = gaps_vector[5][j]
    
    resultados = {'puntos' : [puntos1,puntos2],
                  'lista' : lista,
                  'parametros' : parametros,
                  'tefreqs' : tefreqs,
                  'tmfreqs' : tmfreqs,
                  'tevels' : tevels,
                  'tmvels' : tmvels,
                  'gaps' : {'Ancho TE' : ancho_te,
                            'Promedio TE' : prom_te,
                            'Porcentaje TE' : porcent_te,
                            'Ancho TM' : ancho_tm,
                            'Promedio TM' : prom_tm,
                            'Porcentaje TM' : porcent_tm
                           }
                 }

    with open('resultados-' + str(nombre) + '.pkl', 'wb') as f:
        pickle.dump(resultados, f)
    #os.system('mv ' + 'resultados-' + str(nombre) + '.pkl ' +  str(nombre))

    return resultados
    



