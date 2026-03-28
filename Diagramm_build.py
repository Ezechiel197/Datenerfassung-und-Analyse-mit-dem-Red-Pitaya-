import pandas as pd
import matplotlib.pyplot as plt

# Schritt 1: CSV-Datei einlesen
file_path = 'hist_Na_22.csv'  # Name oder Pfad Ihrer CSV-Datei

try:
    # Versuchen, die CSV-Datei mit Komma-Trennzeichen zu lesen
    data = pd.read_csv(file_path, sep=';', na_values=['', 'NaN'])

    # Falls das Trennzeichen Semikolon ist, ändern Sie die Zeile wie folgt:
    # data = pd.read_csv(file_path, sep=';', na_values=['', 'NaN'])

except pd.errors.ParserError:
    print("Fehler beim Lesen der CSV-Datei. Bitte überprüfen Sie das Trennzeichen und die Struktur der Datei.")
    exit()

# Extrahieren der Daten
try:
    spannung = data['Spannung'].values  # Werte für die erste X-Achse (Spannung)
    energie = data['Energie(KeV)'].values  # Werte für die zweite X-Achse (Energie)
    y_werte = data['Count'].values  # Y-Werte
except KeyError as e:
    print(f"Fehler: Die Spalte '{e.args[0]}' existiert nicht in der CSV-Datei. Bitte überprüfen Sie die Header-Namen.")
    exit()

# Schritt 2: Diagramm erstellen
fig, ax1 = plt.subplots()

# Erste X-Achse (Spannung)
ax1.plot(spannung, y_werte, 'b-', label='Count über Spannung')  # Blaue Linie für Spannung
ax1.set_xlabel('Spannung (V)', color='b')
ax1.set_ylabel('Count')
ax1.tick_params(axis='x', colors='b')  # Farbe der X-Achse-Spannung auf blau setzen
ax1.legend(loc='upper left')

# Zweite X-Achse (Energie)
ax2 = ax1.twiny()  # Eine neue Achse über der ersten Achse erstellen
ax2.plot(energie, y_werte, 'r--', label='Count über Energie')  # Rote gestrichelte Linie für Energie
ax2.set_xlabel('Energie (KeV)', color='r')
ax2.tick_params(axis='x', colors='r')  # Farbe der zweiten X-Achse auf rot setzen
ax2.legend(loc='upper right')

# Layout anpassen, damit die Achsenbeschriftungen nicht übereinanderliegen
fig.tight_layout()

# Titel hinzufügen
plt.title('Diagramm mit zwei X-Achsen: Spannung und Energie')

# Diagramm anzeigen
plt.show()