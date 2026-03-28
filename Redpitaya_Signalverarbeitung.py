


import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import find_peaks
import redpitaya_scpi as scpi
import csv

# Red Pitaya Konfiguration
IP = 'rp-f068ca.local' # IP-Adresse deines Red Pitaya Geräts
rp_s = scpi.scpi(IP)

# zurücksetzen und Konfiguration der Red Pitaya
rp_s.tx_txt('ACQ:RST')  # Erfassung zurücksetzen
rp_s.tx_txt('ACQ:DATA:FORMAT ASCII')  # Setze Datenformat auf ASCII
rp_s.tx_txt('ACQ:DATA:UNITS VOLTS')  # Setze Einheiten auf Volt
rp_s.tx_txt('ACQ:DEC 256')  # Setze Decimation (3.9 MS/s)
rp_s.tx_txt('ACQ:TRIG:LEV 0.01')  # Setze Trigger-Level auf +0.6 V (für positives Signal)
rp_s.tx_txt('ACQ:TRIG CH1_PE')  # Trigger auf steigende Flanke von CH1 (positives Signal)
rp_s.tx_txt('ACQ:TRIG:DLY 1000')  # Trigger-Verzögerung
rp_s.tx_txt('ACQ:MODE CONT')  # Kontinuierlicher Modus
rp_s.tx_txt('ACQ:SOUR1:GAIN HV')  # Hochspannungsmode
rp_s.tx_txt('ACQ:START')  # Starte die Datenerfassung

# Initialisiere Plots
plt.ion()  # Interaktiver Modus aktivieren
fig, (ax_raw, ax_hist) = plt.subplots(2, 1, figsize=(10, 8), sharex=False)

# Rohsignal-Plot initialisieren
line_raw, = ax_raw.plot([], [], label="Signal", color='blue', lw=0.8)
ax_raw.set_xlim(0, 16384)  # X-Achse-Bereich (Buffergröße)
ax_raw.set_ylim(-1, 5)  # X-Achse-Bereich (Buffergröße)
ax_raw.set_title('Kontinuierliches Signal vom Red Pitaya')
ax_raw.set_xlabel('Sample')
ax_raw.set_ylabel('Amplitude (V)')
ax_raw.legend()
ax_raw.grid(True, which='major', linestyle='--', linewidth=0.5)

# Peak-Marker für lokale Maxima
line_peaks, = ax_raw.plot([], [], 'ro', markersize=4, label="Maxima")  # Rote Punkte für Maxima
ax_raw.legend()

# Histogramm-Plot initialisieren
bins = np.linspace(0, 5, 1001)  # Bins von 0 bis 1 V mit 1000 Intervallen
hist_peaks = np.zeros(len(bins) - 1)  # Speicher für kumulative Frequenzen der Maxima
bar_container = ax_hist.bar(bins[:-1], hist_peaks, width=np.diff(bins), color='green', alpha=0.7)
ax_hist.set_title('Kumulatives Histogramm der lokalen Maxima')
ax_hist.set_xlabel('Amplitude (V)')
ax_hist.set_ylabel('Count')
#ax_hist.set_ylim(0.1,None)
ax_hist.set_yscale('log')  # Logarithmische Skalierungax_hist
ax_hist.grid(True, which='major', linestyle='--', linewidth=0.5)

try:
    while True:
        # Warte auf Trigger-Ereignis
        rp_s.tx_txt('ACQ:TRIG:STAT?')  # Abfrage des Trigger-Status
        if rp_s.rx_txt().strip() != 'TD':  # Warte, bis der Trigger ausgelöst wird
            continue
        
        # Hole Daten
        rp_s.tx_txt('ACQ:SOUR1:DATA?')  # Anfrage der Daten
        buff_string = rp_s.rx_txt().strip('{}\n\r').split(',')
        try:
            buff = np.array([float(val) for val in buff_string])  # Konvertiere Daten in Floats
        except ValueError:
            print("Ungültige Daten empfangen. Überspringe diese Iteration.")
            continue
        if len(buff) == 0:
            print("Keine gültigen Daten empfangen. Überspringe diese Iteration.")
            continue
        offset = np. median(buff)
        
        buff = buff-offset
        # Positive Peaks (lokale Maxima) finden
        peaks_max, _ = find_peaks(buff, height=0.02, width=(3,None),distance=40)  # Finde lokale Maxima im positiven Signal
        peak_values_max = buff[peaks_max]  # Amplituden der lokalen Maxima

        # Aktualisiere Rohsignal-Plot
        line_raw.set_ydata(buff)  # Aktualisiere Y-Daten
        line_raw.set_xdata(np.arange(len(buff)))  # Aktualisiere X-Daten

        # Zeichne Maxima als rote Punkte
        line_peaks.set_data(peaks_max, peak_values_max)  # Markiere Maxima im originalen Signal

        # Histogramm aktualisieren
        new_hist, bin_edges = np.histogram(peak_values_max, bins=bins)  # Positive Werte für Histogramm
        hist_peaks += new_hist
        for count, rect in zip(hist_peaks, bar_container.patches):
            rect.set_height(count)  # Aktualisiere Höhe der Balken

        # Automatische Anpassung der Y-Achse für das Histogramm
        ax_hist.set_ylim(0.1, max(1, np.max(hist_peaks) * 1.2))
        
        # Zeichne Plots
        fig.canvas.draw_idle()  # Aktualisiere nur geänderte Teile
        fig.canvas.flush_events()

        # Kurze Pause zwischen Iterationen
        time.sleep(0.1)

except KeyboardInterrupt:
    with open("histogram_Cobel_60.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Bin_Start", "Bin_End", "Frequency"])  # Header
        for i in range(len(hist_peaks)-1):
            writer.writerow([bin_edges[i], bin_edges[i+1], hist_peaks[i]])

    print("Histogramm-Daten wurden in 'histogram.csv' gespeichert.")
    print("Datenübertragung gestoppt.")
    rp_s.tx_txt('ACQ:STOP')  # Stoppe die Datenerfassung
    plt.ioff()
    plt.show()
