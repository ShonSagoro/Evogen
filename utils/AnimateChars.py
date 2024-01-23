import os
import time

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation


class AnimarChars:
    math_function = {
        'sin': np.sin,
        'cos': np.cos,
        'tan': np.tan,
        'pi': np.pi,
        'log': np.log,
        'e': np.e,
        'ln': lambda x: np.log(x + 1e-7),
        'x': None,
        'abs': np.abs
    }

    def __init__(self, generations, parameter, expression):
        self.parameter = parameter
        self.generations = generations
        self.expression = expression
        self.animation_list = []
        self.videos_list = []

    def init_animation(self):
        start = time.time()
        total_generations = len(self.generations)
        max_extra_images = min(10, total_generations - 2)
        for i, gen in enumerate(self.generations):
            if i == 0 or i == total_generations - 1 or (i % ((total_generations - 2) // max_extra_images) == 0):
                self.animate(gen)
        self.join_videos()
        end = time.time()
        total_time = end - start
        print(f"Tiempo de ejecución: {total_time} segundos")

    def animate(self, gen):
        x_values = np.array([chromosome.x for chromosome in gen.chromosomas])
        fx_values = np.array([chromosome.fx for chromosome in gen.chromosomas])
        self.animation_list.append(self.animate_plot(x_values, fx_values, gen.id, gen.better, gen.worst))
        video_name = f"public/video{self.generations[1].id + 1}.mp4"
        self.videos_list.append(video_name)

    def animate_plot(self, x, y, id, better, worst):
        fig, ax = plt.subplots()
        x_data = np.linspace(self.parameter.min_limit, self.parameter.max_limit, 1000)
        self.math_function['x'] = x_data
        y_data = eval(self.expression, self.math_function)

        def update_plot(i):
            ax.clear()
            ax.scatter(x[:i], y[:i])
            ax.set_xlim(self.parameter.min_limit, self.parameter.max_limit)
            ax.set_ylim([1.1 * np.min(y), 1.1 * np.max(y)])
            if better:
                ax.scatter(better.x, better.fx, color='red', label='Mejor Cromosoma')

            if worst:
                ax.scatter(worst.x, worst.fx, color='blue', label='Peor Cromosoma')
            ax.legend()
            ax.set_xlabel('x')
            ax.set_ylabel('fx')
            ax.set_title(f'Dispersión de fx - Generación {id}')
            fig.suptitle(f"Expresión: {self.expression}", fontsize=16)

            ax.plot(x_data, y_data, '--', label='Expresión')

        animate = FuncAnimation(fig, update_plot, range(len(x)), interval=0, cache_frame_data=False, repeat=False)
        return fig, animate

    def grabarVideo(self, animacion, nombre_video):
        fig, animar = animacion

        ancho, alto = fig.get_size_inches() * fig.get_dpi()
        fourcc = cv.VideoWriter_fourcc(*'mp4v')
        video_out = cv.VideoWriter(nombre_video, fourcc, 60, (int(ancho), int(alto)))
        len_x = animar._stop
        for i in range(len_x):
            animar(i)
            fig.canvas.draw()
            image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8').reshape(int(alto), int(ancho), 3)
            video_out.write(image)

        video_out.release()

        plt.close(fig)

    def join_videos(self):
        videos = []
        for i in range(len(self.animation_list)):
            print(f"Generando video {i + 1}")
            fig, animar = self.animation_list[i]
            animar.save(self.videos_list[i], writer='ffmpeg', fps=60, dpi=72)
            plt.close(fig)
            videos.append(cv.VideoCapture(self.videos_list[i]))

        ancho = int(videos[0].get(cv.CAP_PROP_FRAME_WIDTH))
        alto = int(videos[0].get(cv.CAP_PROP_FRAME_HEIGHT))
        fps = int(videos[0].get(cv.CAP_PROP_FPS))
        fourcc = cv.VideoWriter_fourcc(*'mp4v')
        video_combinado = cv.VideoWriter('public/video_final.mp4', fourcc, fps, (ancho, alto))
        for video in videos:
            print(f"Haciendo videos {video}")
            while True:
                ret, frame = video.read()
                if not ret:
                    break
                video_combinado.write(frame)
        for video in videos:
            video.release()
        video_combinado.release()
        for i in range(len(self.videos_list)):
            if os.path.exists(self.videos_list[i]):
                os.remove(self.videos_list[i])
            else:
                print(f"El archivo {self.videos_list[i]} no se pudo encontrar")

    def reproducirVideo(self, nombre_video):
        video = cv.VideoCapture(nombre_video)
        while True:
            ret, frame = video.read()
            if not ret:
                break
            cv.imshow('public/output_multimedia', frame)
            if cv.waitKey(25) & 0xFF == ord('q'):
                break
        video.release()
        cv.destroyAllWindows()
