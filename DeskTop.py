import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import re

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

import numpy as np
import matplotlib.pyplot as plt

from scipy.fft import rfft, rfftfreq
from scipy.fft import irfft
from scipy.io.wavfile import write
from scipy.fft import fft, fftfreq

from scipy.io import wavfile
import winsound


class FourieMethod():

    def get_magnitude_spectrum(self, signal, sr, f_ratio=1):
        yf = rfft(signal)
        xf = rfftfreq(len(signal), 1 / sr)
        return xf, yf

    def get_magnitude_spectrum1(self, signal, sr, f_ratio=1):
        X = np.fft.rfft(signal)
        X_mag = np.absolute(X)
        f = np.linspace(0, sr, len(X_mag))
        f_bins = int(len(X_mag) * f_ratio)
        return f[:f_bins], X_mag[:f_bins]

    def filtr(self, data, sr):
        y_mas = np.array(data)
        n = len(y_mas)
        yf = rfft(y_mas)
        xf = fftfreq(n, 1 / sr)
        new_sig = irfft(yf)

        # self.dif = data[0]
        return new_sig


class WizardLikeApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        container = tk.Frame(self)
        container.grid(row=0, column=0, sticky='nsew')
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            # frame.pack()
        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text='Главная страница')
        label.grid(column=0, row=0, sticky=NSEW, padx=10)
        open_button = tk.Button(self, text="Открыть",
                                 command=lambda: controller.show_frame(PageOne))
        # open_button1.grid(column=0, row=0, sticky=NSEW, padx=10)
        open_button.grid(column=0, row=1, sticky=NSEW, padx=10)
        create_button = tk.Button(self, text="Создать",
                                 command=lambda: controller.show_frame(PageTwo))
        # open_button2.grid(column=0, row=1, sticky=NSEW, padx=10)
        create_button.grid(column=1, row=1, sticky=NSEW, padx=10)


"""class PageThree(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text='Page Three')
        label.pack(pady=10, padx=10)
        self.choose_file()
        button1 = tk.Button(self, text='Back to Home',
                            command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = tk.Button(self, text='Page Two',
                            command=lambda: controller.show_frame(PageTwo))
        button2.pack()

    def choose_file(self):
        self.filepath = filedialog.askopenfilename()
        if self.filepath != "":
            samplerate, data = wavfile.read(self.filepath)
            self.show_graphics1(samplerate, data)
            save_button = tk.Button(self, text="Сохранить", command=self.save_sound)
            # save_button.grid(column=2, row=0, sticky=NSEW, padx=10)
            save_button.pack()
            play_before_button1 = tk.Button(self, text="Play original", command=self.play_sound1)
            # play_before_button1.grid(column=0, row=1, sticky=NSEW, padx=10)
            play_before_button1.pack()
            play_before_button2 = tk.Button(self, text="Play Fourie", command=self.play_sound2)
            # play_before_button2.grid(column=1, row=1, sticky=NSEW, padx=10)
            play_before_button2.pack()

    def show_graphics1(self, sr, data):
        fm = FourieMethod()
        fig, ax = plt.subplots(4, 1, figsize=(10, 7))
        filtr_data = fm.filtr(data, sr)
        ax[0].plot(data)

        ax[1].plot(filtr_data)

        x, y = fm.get_magnitude_spectrum1(data, sr)

        self.filtr_data = filtr_data
        self.sr = sr
        self.data = data
        ax[2].plot(x[x > 0], y[x > 0])
        # ax[3].plot(x[x > 0], 1/y[x > 0])
        ax[3].plot(1 / x[x > 0], y[x > 0])
        # ax[2].plot(x, abs(y))
        if 'self.canvas' in globals():
            print(123)

        self.canvas = FigureCanvasTkAgg(fig)
        self.canvas.draw()
        # self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        # self.canvas.get_tk_widget().grid(column=0, row=2, columnspan=3, sticky=NSEW, padx=10)
        self.canvas.get_tk_widget().pack()
        self.toolbar = NavigationToolbar2Tk(self.canvas, pack_toolbar=False)
        self.toolbar.update()
        self.toolbar.pack()
        # self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        # self.toolbar.grid(column=0, row=3, columnspan=2, sticky=NSEW, padx=10)

    def play_sound1(self):
        winsound.PlaySound(self.filepath, winsound.SND_FILENAME)

    def play_sound2(self):
        norm_new_sig = np.byte(self.filtr_data * (256 / self.filtr_data.max()))
        write("clean.wav", self.sr, norm_new_sig)
        winsound.PlaySound("clean.wav", winsound.SND_FILENAME)

    def save_sound(self):

        norm_new_sig = np.byte(self.filtr_data * (256 / self.filtr_data.max()))
        dif = norm_new_sig[0] - self.data[0]
        print(dif)
        for i in range(0, len(norm_new_sig)):
            norm_new_sig[0] -= dif
        write("clean.wav", self.sr, norm_new_sig)"""


class PageOne(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text='Фурье преобразование звукового сигнала')
        label.grid(column=0, row=0, columnspan=2, sticky=NSEW, padx=10)

        # save_button = tk.Button(self, text="Выбрать файл", command=self.choose_file)
        save_button = tk.Button(self, text="Выбрать файл", command=self.choose_file)
        # save_button.grid(column=2, row=0, sticky=NSEW, padx=10)
        save_button.grid(column=0, row=1, sticky=NSEW, padx=10)
        save_button = tk.Button(self, text="Сохранить", command=lambda: self.save_sound)
        # save_button.grid(column=2, row=0, sticky=NSEW, padx=10)
        save_button.grid(column=1, row=1, sticky=NSEW, padx=10)
        play_before_button1 = tk.Button(self, text="Включить оригинал", command=self.play_sound1)
        # play_before_button1.grid(column=0, row=1, sticky=NSEW, padx=10)
        play_before_button1.grid(column=0, row=2, sticky=NSEW, padx=10)
        play_before_button2 = tk.Button(self, text="Включить восстановленный", command=self.play_sound2)
        # play_before_button2.grid(column=1, row=1, sticky=NSEW, padx=10)
        play_before_button2.grid(column=1, row=2, sticky=NSEW, padx=10)
        button1 = tk.Button(self, text='Вернуться на главный',
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(column=0, row=3, sticky=NSEW, padx=10)

        button2 = tk.Button(self, text='Создать',
                            command=lambda: controller.show_frame(PageTwo))
        button2.grid(column=1, row=3, sticky=NSEW, padx=10)

    def choose_file(self):
        #self._clear()
        self.filepath = ""
        self.filepath = filedialog.askopenfilename()
        if self.filepath != "":
            samplerate, data = wavfile.read(self.filepath)
            self.show_graphics1(samplerate, data)


    def _clear(self):
        for item in self.canvas.get_tk_widget().find_all():
            self.canvas.get_tk_widget().delete(item)

    def show_graphics1(self, sr, data):
        fm = FourieMethod()
        fig, ax = plt.subplots(2, 2, figsize=(20, 10))
        filtr_data = fm.filtr(data, sr)
        ax[0][0].set_title('звуковая запись')
        ax[0][0].set_xlabel("время")
        ax[0][0].set_ylabel("амплитуда")
        ax[0][0].plot(data)

        ax[0][1].set_title('восстановленные данные')
        ax[0][1].set_xlabel("время")
        ax[0][1].set_ylabel("амплитуда")
        ax[0][1].plot(filtr_data)

        x, y = fm.get_magnitude_spectrum1(data, sr)

        filtr_data = filtr_data
        sr = sr
        data = data
        ax[1][0].set_title('спектр частот')
        ax[1][0].set_xlabel("частота(Гц)")
        ax[1][0].set_ylabel("амплитуда")
        ax[1][0].plot(x[x > 0], y[x > 0])



        ax[1][1].set_title('спектр длин волн')
        ax[1][1].set_xlabel("длина волны")
        ax[1][1].set_ylabel("амплитуда")
        ax[1][1].plot(1 / x[x > 0], y[x > 0])
        # ax[2].plot(x, abs(y))
        if 'self.canvas' in locals():
            print(123)

        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        # self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        # self.canvas.get_tk_widget().grid(column=0, row=2, columnspan=3, sticky=NSEW, padx=10)
        canvas.get_tk_widget().grid(column=0, row=0,columnspan=2, sticky=NSEW, padx=10)
        toolbar = NavigationToolbar2Tk(canvas, self, pack_toolbar=False)
        toolbar.update()
        #toolbar.grid(column=1, row=2, sticky=NSEW, padx=10)
        # self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.toolbar.grid(column=1, row=0, columnspan=2, sticky=NSEW, padx=10)
        clear_btn = tk.Button(self, text="Очистить", command=self._clear)
        # save_button.grid(column=2, row=0, sticky=NSEW, padx=10)
        clear_btn.grid(column=1, row=1, sticky=NSEW, padx=10)


    def play_sound1(self):
        winsound.PlaySound(self.filepath, winsound.SND_FILENAME)

    def play_sound2(self):
        norm_new_sig = np.byte(self.filtr_data * (256 / self.filtr_data.max()))
        write("clean.wav", self.sr, norm_new_sig)
        winsound.PlaySound("clean.wav", winsound.SND_FILENAME)

    def save_sound(self):

        norm_new_sig = np.byte(self.filtr_data * (256 / self.filtr_data.max()))
        dif = norm_new_sig[0] - self.data[0]
        print(dif)
        for i in range(0, len(norm_new_sig)):
            norm_new_sig[0] -= dif
        write("clean.wav", self.sr, norm_new_sig)


class PageTwo(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        label = tk.Label(self, text='Создание волны')
        label.grid(column=0, row=0, sticky=NSEW, padx=10)

        sr_label = Label(self, text="Выберите частоту дискретизации (Гц): ")
        sr_label.grid(column=0, row=2, sticky=NSEW, padx=10)
        chose_sr = ["11025", "22050", "44100"]
        self.sr_input = ttk.Combobox(self, values=chose_sr)
        self.sr_input.grid(column=1, row=2, sticky=NSEW, padx=10)

        time_label = Label(self, text="Выберите время (с): ")
        time_label.grid(column=0, row=3, sticky=NSEW, padx=10)
        chose_time = ["1", "2", "3"]
        self.time_input = ttk.Combobox(self, values=chose_time)
        self.time_input.grid(column=1, row=3, sticky=NSEW, padx=10)

        count_label = Label(self, text="Выберите количество гармоник: ")
        count_label.grid(column=0, row=4, sticky=NSEW, padx=10)
        chose_count = ["1", "2", "3", "4", "5"]
        self.count_input = ttk.Combobox(self, values=chose_count)
        self.count_input.grid(column=1, row=4, sticky=NSEW, padx=10)
        self.k = 0

        self.mas_phase = []
        self.mas_freq = []
        self.mas_ampl = []

        button1 = tk.Button(self, text='Вернуться на главный',
                            command=lambda: controller.show_frame(StartPage))
        button1.grid(column=0, row=5, sticky=NSEW, padx=10)

        play_before_button = ttk.Button(self, text="Подтвердить", command=self.insert_wave)
        play_before_button.grid(column=1, row=5, sticky=NSEW, padx=10)

    def insert_wave(self):

        phase_label = Label(self, text="Выберите фазу: ")
        phase_label.grid(column=0, row=2, sticky=NSEW, padx=10)
        chose_phase = ["0", "pi/2", "pi", "3pi/2"]
        self.phase_input = ttk.Combobox(self, values=chose_phase)
        self.phase_input.grid(column=1, row=2, sticky=NSEW, padx=10)

        freq_label = Label(self, text="Введите частоту (Гц): ")
        freq_label.grid(column=0, row=3, sticky=NSEW, padx=10)
        self.freq_input = ttk.Entry(self, validate="key")
        self.freq_input.grid(column=1, row=3, sticky=NSEW, padx=10)

        ampl_label = Label(self, text="Введите амплитуду: ")
        ampl_label.grid(column=0, row=4, sticky=NSEW, padx=10)
        self.ampl_input = ttk.Entry(self, validate="key")
        self.ampl_input.grid(column=1, row=4, sticky=NSEW, padx=10)
        self.k += 1

        if int(self.count_input.get()) > self.k:
            play_before_button = ttk.Button(self, text="Далее", command=self.create_mas)
            play_before_button.grid(column=1, row=5, sticky=NSEW, padx=10)
        else:
            play_before_button = ttk.Button(self, text="Подтвердить", command=self.create_mas)
            play_before_button.grid(column=1, row=5, sticky=NSEW, padx=10)

    def create_mas(self):
        self.mas_phase.append(self.phase_input.get())
        self.mas_freq.append(int(self.freq_input.get()))
        self.mas_ampl.append(self.ampl_input.get())
        if int(self.count_input.get()) > self.k:
            self.insert_wave()
        else:
            self.show_wave()

    def generate_sine_wave(self, freq, phase, sample_rate, duration):
        x = np.linspace(0, duration, sample_rate * duration, endpoint=False)
        frequencies = x * freq
        # 2pi для преобразования в радианы
        y = np.sin((np.pi) * frequencies + phase)
        return x, y

    def show_wave(self):
        fm = FourieMethod()
        fig, ax = plt.subplots(2, 1, figsize=(10, 8))
        sum_wave = np.zeros(int(self.sr_input.get())*int(self.time_input.get()))
        formula = 'f(x)='
        for i in range(int(self.count_input.get())):
            dur_phase = 0
            if self.mas_phase[i] == "0":
                dur_phase = 0
            elif self.mas_phase[i] == "pi/2":
                dur_phase = np.pi/2
            elif self.mas_phase[i] == "pi":
                dur_phase = np.pi
            elif self.mas_phase[i] == "3pi/2":
                dur_phase = 1.5*np.pi
            x, y = self.generate_sine_wave(int(self.mas_freq[i]), dur_phase, int(self.sr_input.get()), int(self.time_input.get()))
            sum_wave = sum_wave + y
            formula = formula + '+sin(' + str(self.mas_freq[i]) + 't + ' + self.mas_phase[i] + ')'

        x, y = fm.get_magnitude_spectrum1(sum_wave, int(self.sr_input.get()))
        ax[0].set_title(formula)
        ax[0].set_xlabel("время")
        ax[0].set_ylabel("колебание")
        #ax[0].label('Звуковые колебания')
        ax[0].plot(x[:500], sum_wave[:500])
        ax[1].set_title('амплитудно-частотная характеристика')
        ax[1].set_xlabel("частота (Гц)")
        ax[1].set_ylabel("амплитуда")
        #ax[1].label('Амплитудно-частотная характеристика')
        ax[1].plot(x[x>0], y[x>0])
        print(x[y>10])

        canvas = FigureCanvasTkAgg(fig)
        canvas.draw()
        canvas.get_tk_widget().grid(column=0, row=0, columnspan=3, sticky=NSEW, padx=10)

        toolbar = NavigationToolbar2Tk(canvas, pack_toolbar=False)
        toolbar.update()
        toolbar.grid(column=0, row=1, columnspan=2, sticky=NSEW, padx=10)


"""root = Tk()
root.title("METANIT.COM")
root.geometry("250x200")"""
app = WizardLikeApp()
app.mainloop()
