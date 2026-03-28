# Funktion zum Konvertieren einer Komma-getrennten Datei in eine Semikolon-getrennte CSV-Datei
def convert_to_csv(input_file, output_file):
    try:
        # Öffne die Eingabedatei im Lesemodus
        with open(input_file, 'r', encoding='utf-8') as infile:
            data = infile.readlines()  # Lies alle Zeilen aus der Datei

        # Erstelle eine neue Liste, um die konvertierten Zeilen zu speichern
        converted_data = []

        # Gehe durch jede Zeile in der Datei
        for line in data:
            # Ersetze Kommas durch Semikolons und entferne Leerzeichen am Anfang/Ende
            converted_line = line.strip().replace(',', ';') + '\n'
            converted_data.append(converted_line)

        # Schreibe die konvertierten Daten in die Ausgabedatei
        with open(output_file, 'w', encoding='utf-8') as outfile:
            outfile.writelines(converted_data)

        print(f"Die Datei wurde erfolgreich konvertiert: {output_file}")

    except FileNotFoundError:
        print(f"Fehler: Die Datei '{input_file}' wurde nicht gefunden.")
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")


# Beispielaufruf des Programms
if __name__ == "__main__":
    # Pfade zur Eingabe- und Ausgabedatei
    input_file_path = "histogram_Cs_137.csv"  # Name der Eingabetextdatei
    output_file_path = "hist_Cs_137.csv"  # Name der Ausgabecsv-Datei

    # Konvertierung starten
    convert_to_csv(input_file_path, output_file_path)