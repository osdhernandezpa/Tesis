from funciones import *

puntos_lineal = np.round(np.arange(1.1,15.1,0.1),2)
rutina(num_bandas=20,
       archivo_control=ctl_num([20,512,50,500], 'control-2mat.ctl'),
       control=[2.35,1.0,0.5,0.5],
       puntos=puntos_lineal,
       tipo=['2mat',0], # num, mat o lineal. indice (en control) para introduccion
                        # usar indice mayor a tamanho de control para omitir remplazo
       cifras=2, # solo se usa para el balance de proporciones
       nombre='lineal-2mat',
       funcion=default # obligatorio para balance dimensional
                       # hace posible lista de parametros mas exotica
      )

resultados = rutina_doble(num_bandas=8,
           archivo_control=ctl_num([20,512,50,500], 'control-2mat.ctl'),
           control=[2.35,1.0,0.81,0.19], #e1,e2,e3,a1,a2,a3
           puntos1=[1.5,2.5,3.5],
           puntos2=[0.4,0.6,0.8],
           tipo=['2mat',0,2], # num, mat o lineal. indice (en control) para introduccion   
           cifras=2, # solo se usa para el balance de proporciones
           nombre='rutina-doble',
           funcion=partial(balance_proporcional2,
                           puntos=[0.4,0.6,0.8],
                           material=1,
                           cifras=2
                          )
          )




