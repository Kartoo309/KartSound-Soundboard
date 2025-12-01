from tkinter import Tk, Label, Button, ttk, N, S, E, W

class SoundboardApp:
    """Klasa implementująca interfejs graficzny Soundboarda."""
    def __init__(self, master, sounds, hotkeys_by_sound, play_func, stop_func):
        """
        Inicjalizuje aplikację GUI.

        Args:
            master: Główny obiekt Tkinter.
            sounds (dict): Słownik wczytanych dźwięków {nazwa_id: obiekt_pygame}.
            hotkeys_by_sound (dict): Słownik {nazwa_id: skrót_klawiszowy}.
            play_func (function): Funkcja do odtwarzania dźwięku.
            stop_func (function): Funkcja do zatrzymywania dźwięków.
        """
        self.master = master
        master.title("KartSound")
        self.play_func = play_func
        self.stop_func = stop_func

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(2, weight=1)

        self._create_widgets(sounds, hotkeys_by_sound)

    def _create_widgets(self, sounds, hotkeys_by_sound):
        """Tworzy wszystkie elementy GUI."""

        # Ramka na kontrolki główne
        control_frame = ttk.Frame(self.master, padding="10 10 10 10")
        control_frame.grid(row=0, column=0, sticky=(N, W, E, S))
        control_frame.columnconfigure(0, weight=1)

        # Nagłówek
        Label(control_frame, text="Soundboard", font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=3, pady=5)

        # Przycisk STOP
        stop_button = Button(control_frame, text="ZATRZYMAJ WSZYSTKO", command=self.stop_func, bg='red', fg='white')
        stop_button.grid(row=1, column=0, columnspan=3, pady=10, sticky=(W, E))

        # Ramka na listę dźwięków
        sound_list_frame = ttk.Frame(self.master, padding="10 10 10 10")
        sound_list_frame.grid(row=2, column=0, sticky=(N, W, E, S))
        sound_list_frame.columnconfigure(0, weight=1)

        Label(sound_list_frame, text="Dźwięki / Skróty (config.ini):", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=W)

        # Tabela (Grid) na dźwięki
        row_counter = 1

        for name_id in sounds.keys():
            hotkey = hotkeys_by_sound.get(name_id, 'BRAK')

            # Kolumna 1: Nazwa Dźwięku
            Label(sound_list_frame, text=name_id, anchor=W).grid(row=row_counter, column=0, sticky=W, padx=5, pady=2)

            # Kolumna 2: Przypisany Skrót
            Label(sound_list_frame, text=f"[{hotkey}]", anchor=W, fg='blue').grid(row=row_counter, column=1, sticky=W, padx=5, pady=2)

            # Kolumna 3: Przycisk Odtwórz (Ręczne uruchomienie)
            play_btn = Button(sound_list_frame, text="▶ Odtwórz", command=lambda id=name_id: self.play_func(id))
            play_btn.grid(row=row_counter, column=2, sticky=E, padx=5, pady=2)

            row_counter += 1