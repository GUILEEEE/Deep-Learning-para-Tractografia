import numpy as np
import nibabel as nib
from dipy.io.streamline import load_tractogram
import os

def extract_cubic_neighborhood(x, y, z, peaks_data, n):
    """Extrae una vecindad cúbica del volumen de peaks"""
    offset = n // 2
    shape = peaks_data.shape
    
    # Verificar bordes
    if (x - offset < 0) or (x + offset + 1 > shape[0]):
        return None
    if (y - offset < 0) or (y + offset + 1 > shape[1]):
        return None
    if (z - offset < 0) or (z + offset + 1 > shape[2]):
        return None
    
    # Extraer vecindad
    return peaks_data[x-offset:x+offset+1, 
                     y-offset:y+offset+1, 
                     z-offset:z+offset+1, :]

def generate_training_data(peaks_path, trk_path, output_dir, n=3, k=1, num_samples=1000):
    # Cargar datos de peaks
    peaks_img = nib.load(peaks_path)
    peaks_data = peaks_img.get_fdata()
    affine = peaks_img.affine
    
    # Cargar tractograma
    tractogram = load_tractogram(trk_path, reference=peaks_img)
    streamlines = tractogram.streamlines

    # Almacenamiento de datos
    inputs = []
    outputs = []
    
    # Procesar cada streamline
    for streamline in streamlines:
        if len(inputs) >= num_samples:
            break
            
        # Convertir coordenadas a espacio voxel
        voxel_coords = [np.round(nib.affines.apply_affine(
            np.linalg.inv(affine), point)).astype(int) 
            for point in streamline]
        
        # Calcular direcciones normalizadas
        directions = []
        for i in range(len(streamline)-1):
            dir_vec = np.array(streamline[i+1]) - np.array(streamline[i])
            norm = np.linalg.norm(dir_vec)
            if norm == 0:
                continue
            directions.append(dir_vec / norm)
        
        # Generar muestras para este streamline
        for i in range(k, len(directions)):
            if len(inputs) >= num_samples:
                break
                
            # Extraer vecindad
            x, y, z = voxel_coords[i]
            neighborhood = extract_cubic_neighborhood(x, y, z, peaks_data, n)
            
            if neighborhood is None:
                continue
                
            # Obtener direcciones anteriores
            prev_dirs = directions[i-k:i]
            
            # Crear muestra de entrada
            input_neigh = neighborhood.flatten()
            input_prev = np.array(prev_dirs).flatten()
            input_sample = np.concatenate([input_neigh, input_prev])
            
            # Crear muestra de salida
            output_sample = directions[i]
            
            inputs.append(input_sample)
            outputs.append(output_sample)
    
    # Guardar datos en formato .npz
    os.makedirs(output_dir, exist_ok=True)
    np.savez_compressed(
        os.path.join(output_dir, f'data_{num_samples}_k{n}.npz'),
        inputs=np.array(inputs),
        outputs=np.array(outputs)
    )
    print(f"Datos generados: {len(inputs)} muestras con vecindad de tamano {k} y {k} direcciones.")
    print()

if __name__ == "__main__":
    generate_training_data(
        peaks_path='ismrm2015_withReversed__peaks.nii.gz',
        trk_path='2_filtered_loops.trk',
        output_dir='datos_train',
        n=5,
        k=1,
        num_samples=100000
    )