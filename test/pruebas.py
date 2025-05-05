#Descripcion general del análisis de MEG/EEG con MNE-Python
#Importación de modulos necesarios
import mne
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

#Carga de datos (Datos de ejemplo proporcionados por MNE-Python)
sample_data_folder = mne.datasets.sample.data_path()
#Carga de datos MEG
sample_data_raw_file = (
    sample_data_folder / "MEG" / "sample" / "sample_audvis_filt-0-40_raw.fif"
)

#Mostramos la informacion sobre el archivo que acabamos de cargar
raw = mne.io.read_raw_fif(sample_data_raw_file)
#Informacion de la carga de datos
print("Informacion 'raw'\n")
print(raw)
#Informacion de los datos ubicaciones de los canales, filtros, pryeciones, etc.
print("Informacion 'raw.info'\n")
print(raw.info)

#Imprimimos la desnidad de potencia espectral (PSD) de los datos, "fmax" es la frecuencia máxima a la que se calcula el PSD
raw.compute_psd(fmax=50).plot(picks="data", exclude="bads", amplitude=False)
#Imprimimos el grafico de los datos en bruto, este es un grafico interactivo, escalar, marcado de canales defectuosos y anotaciones.
raw.plot(duration=5, n_channels=30)

ica = mne.preprocessing.ICA(n_components=20, random_state=97, max_iter=800)
ica.fit(raw)
ica.exclude = [1, 2]  # details on how we picked these are omitted here
ica.plot_properties(raw, picks=ica.exclude)

orig_raw = raw.copy()
raw.load_data()
ica.apply(raw)

# show some frontal channels to clearly illustrate the artifact removal
chs = [
    "EEG 001",
    "EEG 002",
    "EEG 003",
    "EEG 004",
    "EEG 005",
    "EEG 006",
    "EEG 007",
    "EEG 008",
]
chan_idxs = [raw.ch_names.index(ch) for ch in chs]
orig_raw.plot(order=chan_idxs, start=12, duration=4)
raw.plot(order=chan_idxs, start=12, duration=4)

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

plt.show()