#Descripcion general del análisis de MEG/EEG con MNE-Python
#Importación de modulos necesarios
import mne
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

#Cargamos el archivo EDF
file_path = "files/S001/S001R03.edf"
raw = mne.io.read_raw_edf(file_path)

#Imprimos informacion basica sobre el archivo EDF
print("Informacion 'raw'\n")
print(raw)
#Imprimos informacion sobre los datos, ubicaciones de los canales, filtros, proyecciones, etc.
print("Informacion 'raw.info'\n")
print(raw.info)

#Imprimimos la densidad de potencia espectral (PSD) de los datos, "fmax" es la frecuencia máxima a la que se calcula el PSD
raw.compute_psd(fmax=80).plot(picks="data", exclude="bads", amplitude=False)
#Imprimimos el grafico de los datos en bruto, este es un grafico interactivo, escalar, marcado de canales defectuosos y anotaciones.
raw.plot(duration=5, n_channels=30)

# Detectamos eventos en los datos crudos, el canal de estímulo es "STI 014"
events, event_dict = mne.events_from_annotations(raw, event_id={'T0': 1, 'T1': 2, 'T2': 3})

# Filtrar eventos para incluir solo los eventos T1
specific_event = events[events[:, 2] == event_dict['T0']]

# Detectamos qué evento sigue después de cada evento sleccionado
next_events = []
# Iteramos sobre los "specific_event"
for event in specific_event:
    # Buscamos el "event" en la lista de eventos original "events" y retornamos el siguiente evento
    for i, e in enumerate(events):
        if np.array_equal(e, event):
            # Si existe un evento en seguida de "event", lo agregamos a la lista "next_events" y si no agregamos "None"
            next_events.append(events[i + 1] if i + 1 < len(events) else None)
            break

# Crear una lista para almacenar los objetos Raw correspondientes a cada segmento de la tarea especifica
raw_T1_segments = []
# Creamos una lista con la duracion de cada evento
raw_T1_times = []

for i in range(len(specific_event)):
    start_time = specific_event[i][0] / raw.info['sfreq']  # Tiempo de inicio del segmento
    end_time = 0.0  # Tiempo de finalización del segmento

    # Determinar el tiempo de finalización del segmento
    if next_events[i] is None:
        # Si no existe otro evento despues del evento final en la lista el tiempo de finalizacion sera el tiempo final de la señal
        end_time = raw.times[-1]
    else:
        # De lo contrario, el tiempo de finalización es el tiempo de inicio de la próxima tarea
        next_event_time = next_events[i][0] / raw.info['sfreq']
        end_time = next_event_time

    # Segmentar la señal
    raw_segment = raw.copy().crop(tmin=start_time, tmax=end_time)
    raw_T1_segments.append(raw_segment)

    # Almacenar la duración del segmento
    raw_T1_times.append(end_time - start_time)

# Imprimir el gráfico de cada segmento de la señal correspondiente a las tareas T1
for i, raw_segment in enumerate(raw_T1_segments):
    # Extraemos la duracion de la lista raw_T1_times
    raw_segment.plot(duration=raw_T1_times[i], n_channels=15)

plt.show()