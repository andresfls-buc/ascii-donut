import os
import time
import math

def render_donut():
    # Ángulos de rotación iniciales
    A = 0  
    B = 0  
    
    # Caracteres de densidad de luz (Luminance)
    chars = ".,-~:;=!*#$@"
    
    # Limpiamos la pantalla antes de iniciar
    os.system('clear') 

    try:
        while True:
            # Buffer de salida y Buffer de profundidad (z-buffer)
            output = [' '] * 1760 
            z_buffer = [0] * 1760

            # Cálculos matemáticos del Toroide (3D)
            j = 0
            while j < 6.28: # Círculo de la sección transversal
                j += 0.07
                i = 0
                while i < 6.28: # Círculo de la revolución
                    i += 0.02

                    # Optimizamos pre-calculando valores trigonométricos
                    sin_i, cos_i = math.sin(i), math.cos(i)
                    sin_j, cos_j = math.sin(j), math.cos(j)
                    sin_A, cos_A = math.sin(A), math.cos(A)
                    sin_B, cos_B = math.sin(B), math.cos(B)

                    # Ecuación de la dona antes de proyectar
                    h = cos_j + 2 
                    D = 1 / (sin_i * h * sin_A + sin_j * cos_A + 5) 
                    t = sin_i * h * cos_A - sin_j * sin_A

                    # Proyección 2D a coordenadas de consola (x, y)
                    x = int(40 + 30 * D * (cos_i * h * cos_B - t * sin_B))
                    y = int(12 + 15 * D * (cos_i * h * sin_B + t * cos_B))
                    
                    idx = x + 80 * y

                    # Cálculo de iluminación basado en el vector normal
                    N = int(8 * ((sin_j * sin_A - sin_i * cos_j * cos_A) * cos_B - sin_i * cos_j * sin_A - sin_j * cos_A - cos_i * cos_j * sin_B))

                    # Si el punto está en pantalla y es el más cercano al frente (Z-buffering)
                    if 22 > y > 0 and 80 > x > 0 and D > z_buffer[idx]:
                        z_buffer[idx] = D
                        output[idx] = chars[N if N > 0 else 0]

            # \033[H mueve el cursor arriba. \033[96m cambia el color a cian brillante.
            print("\033[H\033[96m", end="")
            
            # Dibujamos el buffer completo
            for k in range(1760):
                print(output[k] if k % 80 != 79 else output[k] + '\n', end="")
            
            # Incremento de rotación
            A += 0.08
            B += 0.04
            
            # Pausa para frames
            time.sleep(0.01)

    except KeyboardInterrupt:
        # Restauramos el color original de la terminal (\033[0m)
        print("\033[0m\n\n[INFO] El renderizado ha finalizado.")

# Ejecución del script
if __name__ == "__main__":
    render_donut()