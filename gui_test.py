import customtkinter
from customtkinter import *

class SoundboardApp:

    customtkinter.set_appearance_mode("system")
    customtkinter.set_default_color_theme("dark-blue")

    acc_colour1 =  "#FFE637"
    acc_colour2 =  "#527FE6"

    def __init__(self, master, sounds, hotkeys_by_sound, play_func, stop_func):
        """
        Inicjalizacja GUI aplikacji.

        Args:
            master: Główny obiekt CustomTkinter.
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

        # --- 1. KONFIGURACJA SEKCJI ---
        frame_sounds = CTkFrame(self.master, border_width=2)
        frame_sounds.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        frame_player_s = CTkFrame(self.master, border_width=2)
        frame_player_s.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        # --- 2. ZAPEŁNIANIE SEKCJI ---

        # Nagłówek
        label = CTkLabel(master=frame_sounds, text="Soundboard", font=('Arial', 14, 'bold'))
        label.grid(row=0, column=0, columnspan=3, pady=5)

        # Ramka na listę dźwięków
        sound_list_frame = CTkFrame(master=frame_sounds)
        sound_list_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

        label = CTkLabel(master=sound_list_frame, text="Dźwięki / Skróty (config.ini):", font=('Arial', 10, 'bold'))
        label.grid(row=0, column=0, sticky="W")

        # Tabela (Grid) na dźwięki
        row_counter = 1

        for name_id in sounds.keys():
            hotkey = hotkeys_by_sound.get(name_id, 'BRAK')

            # Kolumna 1: Nazwa Dźwięku
            label = CTkLabel(master=sound_list_frame, text=name_id, anchor="w")
            label.grid(row=row_counter, column=0, sticky=W, padx=5, pady=2)

            # Kolumna 2: Przypisany Skrót
            label = CTkLabel(master=sound_list_frame, text=f"[{hotkey}]", anchor="w")
            label.grid(row=row_counter, column=1, sticky="w", padx=5, pady=2)

            # Kolumna 3: Przycisk Odtwórz (Ręczne uruchomienie)
            play_btn = CTkButton(master=sound_list_frame, text="▶ Odtwórz", command=lambda id_name=name_id: self.play_func(id_name))
            play_btn.grid(row=row_counter, column=2, sticky="e", padx=5, pady=2)

            row_counter += 1

        # Przycisk STOP
        stop_button = CTkButton(master=frame_player_s, text="STOP", command=self.stop_func, font=('Arial', 14, 'bold'))
        stop_button.grid(row=0, column=0, columnspan=3, pady=5)