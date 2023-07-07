# ================================================================================
# ANIMACION ISING
#
# Genera una animación a partir de un fichero de datos con la configuración
# del retículo en cada instante de tiempo
# 
# El fichero debe estructurarse de la siguiente forma:
# 
#   t_1
#   s(1,1)_1, s(1,2)_1, ..., s(1,M)_1
#   s(2,1)_1, s(2,2)_1, ..., s(2,M)_1
#   (...)
#   s(N,1)_1, s(N,2)_1, ..., s(N,M)_1
#
#   t_2   
#   s(1,1)_2, s(1,2)_2, ..., s(1,M)_2
#   s(2,1)_2, s(2,2)_2, ..., s(2,M)_2
#   (...)
#   s(N,1)_2, s(N,2)_2, ..., s(N,M)_2
#
#   t_3
#   s(1,1)_3, s(1,2)_3, ..., s(1,M)_3
#   s(2,1)_3, s(2,2)_3, ..., s(2,M)_3
#   (...)
#   s(N,1)_3, s(N,2)_3, ..., s(N,M)_3
#   
#   (...)
#
# donde s(i,j)_k es el valor del spin en la fila i-ésima y la columna
# j-ésima en el instante k. M es el número de columnas y N el número
# de filas en el retículo. Los valores del spin deben ser +1 ó -1.
# El programa asume que las dimensiones del retículo no cambian a lo
# largo del tiempo.
# 
# Si solo se especifica un instante de tiempo, se genera una imagen en pdf
# en lugar de una animación
#
# Se puede configurar la animación cambiando el valor de las variables
# de la sección "Parámetros"
#
# ================================================================================

# Importa los módulos necesarios
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import io

# Parámetros
# ========================================
file_in = "output_hopefield_gsl.txt" # Nombre del fichero de datos
file_out = "hopefield" # Nombre del fichero de salida (sin extensión)
interval = 30 # Tiempo entre fotogramas en milisegundos
save_to_file = False # False: muestra la animación por pantalla,
                     # True: la guarda en un fichero
dpi = 150 # Calidad del vídeo de salida (dots per inch)


# Lectura del fichero de datos
# ========================================
# Lee el fichero a una cadena de texto
with open(file_in, "r") as f:
    data_str = f.read()

# Inicializa la lista con los datos de cada fotograma.
# frames_data[j] contiene los datos del fotograma j-ésimo
# Read the data file
with open(file_in, "r") as f:
    data_str = f.read()

# Initialize the list to store the data for each frame
frames_data = []

# Split the text into data blocks
data_blocks = data_str.strip().split("\n\n")

# Iterate over the data blocks
for data_block in data_blocks:
    # Split the block into lines
    lines = data_block.strip().split("\n")

    # Get the time value from the first line
    t_line = lines[0].strip()
    if not t_line:
        continue  # Ignore empty lines

    t = float(t_line)  # Convert the time value to float

    # Convert the remaining lines into a matrix
    frame_data = np.loadtxt(io.StringIO("\n".join(lines[1:])), delimiter=",")
    frames_data.append((frame_data, t))  # Add the frame data and time as a tuple

# Create the animation/plot
fig, ax = plt.subplots()

# Set the axis range
ax.axis("off")  # Hide the axes

# Display the first frame
im = ax.imshow(frames_data[0][0], cmap="binary", vmin=0, vmax=+1)
time_text = ax.text(0.07, 0.90, '', transform=ax.transAxes, fontsize=15)

# Function to update the system configuration in the animation
def update(j_frame, frames_data, im):
    frame_data, t = frames_data[j_frame]
    # Update the plot with the system configuration
    im.set_array(frame_data)

    time_text.set_text(' '.format(t))

    return im, time_text

# Calculate the number of frames or time steps
nframes = len(frames_data)

# If there is more than one time step, generate the animation
if nframes > 1:
    animation = FuncAnimation(
        fig, update,
        fargs=(frames_data, im), frames=len(frames_data), blit=True, interval=interval)

    # Show on screen or save according to parameters
    if save_to_file:
        animation.save("{}.mp4".format(file_out), dpi=dpi)
    else:
        plt.show()
# Otherwise, show or save an image
else:
    # Show on screen or save according to parameters
    if save_to_file:
        fig.savefig("{}.pdf".format(file_out))
    else:
        plt.show()