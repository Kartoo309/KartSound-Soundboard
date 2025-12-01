import pygame
import configparser
from customtkinter import *
from pynput import keyboard
import keyboard

#from SoundboardGUIc import SoundboardApp
from gui_test import SoundboardApp

# --- 1. KONFIGURACJA ŚCIEŻEK ---
# Folder na pliki dźwiękowe (musi istnieć!)
SOUND_DIR = 'dzwieki'
CONFIG_FILE = 'config.ini'

# --- 2. INICJALIZACJA I WCZYTYWANIE ---
try:
    # Inicjalizacja miksera Pygame (do odtwarzania dźwięku)
    # Zwróć uwagę: Pygame nie ma wbudowanej możliwości wyboru urządzenia audio,
    # dlatego musimy ustawić CABLE Input jako domyślne urządzenie systemowe!
    pygame.mixer.init()
except pygame.error as e:
    print(f"Błąd inicjalizacji Pygame: {e}")
    print("Upewnij się, że biblioteka 'pygame' jest poprawnie zainstalowana.")
    exit()

# Słowniki do przechowywania danych
SOUNDS = {}  # {nazwa_pliku: obiekt_pygame_sound}
HOTKEYS = {}  # {skrót_pynput: nazwa_pliku_lub_funkcja}
HOTKEYS_BY_SOUND = {} # {nazwa_pliku: skrót_pynput}


def load_sounds():
    """Automatyczne wczytywanie plików dźwiękowych z folderu."""
    if not os.path.exists(SOUND_DIR):
        print(f"Błąd: Nie znaleziono folderu '{SOUND_DIR}'. Utwórz ten folder i umieść w nim pliki audio.")
        return False

    print(f" ")
    print(f"=================================================================")
    print(f"Wczytywanie plików z: {SOUND_DIR}...")
    for filename in os.listdir(SOUND_DIR):
        if filename.endswith(('.wav', '.mp3', '.ogg')):
            name_id = os.path.splitext(filename)[0]  # Nazwa bez rozszerzenia
            full_path = os.path.join(SOUND_DIR, filename)
            try:
                SOUNDS[name_id] = pygame.mixer.Sound(full_path)
                print(f"Wczytano: {name_id}")
            except pygame.error as err:
                print(f"Błąd wczytywania pliku {filename}: {err}")
    return True


def load_config():
    """Wczytywanie skrótów klawiszowych z pliku INI."""
    config = configparser.ConfigParser()
    if not os.path.exists(CONFIG_FILE):
        print(f"Błąd: Nie znaleziono pliku '{CONFIG_FILE}'. Utwórz go zgodnie z instrukcjami.")
        return False

    config.read(CONFIG_FILE)

    if 'HOTKEYS' not in config:
        print("Błąd: Brak sekcji [HOTKEYS] w pliku config.ini.")
        return False

    print(f" ")
    print(f"=================================================================")
    for name_id, hotkey_str in config.items('HOTKEYS'):
        # Normalizacja nazw dla porównań
        name_id = name_id.strip()
        hotkey_str = hotkey_str.strip()

        # Jeśli klucz odpowiada wczytanemu plikowi lub jest globalnym stopem
        if name_id in SOUNDS or name_id == 'stop_all':
            formatted_hotkey = hotkey_str.replace('<', '').replace('>', '')
            HOTKEYS[hotkey_str] = name_id
            if name_id != 'stop_all':
                HOTKEYS_BY_SOUND[name_id] = formatted_hotkey
            print(f"Skrót przypisany: {hotkey_str} -> {name_id}")

    return True

# Spróbuj wczytać dźwięki i konfigurację
if not (load_sounds() and load_config()):
    print("Błąd konfiguracji. Zamykanie programu.")
    exit()


# --- 3. FUNKCJE ODTWARZANIA ---

def play_sound(name_id):
    """Odtwarza dźwięk i zatrzymuje poprzednie odtwarzanie (jeśli jest)."""
    if name_id in SOUNDS:
        pygame.mixer.stop()  # Zatrzymuje wszystkie aktualnie odtwarzane dźwięki
        SOUNDS[name_id].play()
        print(f"Odtwarzam: {name_id}")
    else:
        print(f"Błąd: Dźwięk '{name_id}' nie został wczytany.")


def stop_all_sounds():
    """Zatrzymuje wszystkie odtwarzane dźwięki."""
    pygame.mixer.stop()
    print("Zatrzymano wszystkie dźwięki.")


# --- 4. OBSŁUGA GLOBALNYCH SKRÓTÓW KLAWISZOWYCH (pynput) ---

def on_hotkey_triggered(target):
    """Główna funkcja wywoływana po aktywacji skrótu przez bibliotekę keyboard."""
    print(f"--- SKRÓT ZŁAPANY: {target} ---")
    if target == 'stop_all':
        stop_all_sounds()
    else:
        play_sound(target)


def setup_hotkeys():
    """
    Konfiguruje skróty klawiszowe używając keyboard.add_hotkey().
    Biblioteka 'keyboard' obsługuje nasłuchiwanie w tle.
    """
    for hotkey_str, target in HOTKEYS.items():
        try:
            # Rejestrujemy skrót klawiszowy.
            # keyword.add_hotkey przyjmuje argumenty jako (skrót, callback, lista_argumentów)
            keyboard.add_hotkey(hotkey_str, on_hotkey_triggered, args=(target,))
        except ValueError:
            print(f"Błąd formatu skrótu w config.ini: '{hotkey_str}' jest niepoprawny dla biblioteki keyboard.")

    print(f" ")
    print("✅ Globalne skróty klawiszowe zostały aktywowane za pomocą biblioteki 'keyboard'.")


def main():

    setup_hotkeys()

    root = CTk()
    app = SoundboardApp(
        master=root,
        sounds=SOUNDS,
        hotkeys_by_sound=HOTKEYS_BY_SOUND,
        play_func=play_sound,
        stop_func=stop_all_sounds
    )
    root.mainloop()

if __name__ == "__main__":
    main()

