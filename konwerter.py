import tkinter as tk
from tkinter import filedialog, messagebox
import xmltodict
import json
import yaml
import os


def convert_file(input_path, input_format, output_path, output_format):
    with open(input_path, 'r', encoding='utf-8') as file:
        if input_format == 'XML':
            data = xmltodict.parse(file.read())
        elif input_format == 'JSON':
            data = json.load(file)
        elif input_format == 'YAML':
            data = yaml.safe_load(file)
        else:
            raise ValueError("Nieobsługiwany format pliku wejściowego")

    with open(output_path, 'w', encoding='utf-8') as file:
        if output_format == 'XML':
            xml_data = xmltodict.unparse(data, pretty=True)
            file.write(xml_data)
        elif output_format == 'JSON':
            json.dump(data, file, ensure_ascii=False, indent=4)
        elif output_format == 'YAML':
            yaml.dump(data, file, allow_unicode=True, default_flow_style=False)
        else:
            raise ValueError("Nieobsługiwany format pliku wyjściowego")


def browse_input_file():
    input_path = filedialog.askopenfilename(
        filetypes=[("Wszystkie Pliki", "*.*"), ("Pliki XML", "*.xml"), ("Pliki JSON", "*.json"),
                   ("Pliki YAML", "*.yaml *.yml")]
    )
    entry_input_path.delete(0, tk.END)
    entry_input_path.insert(0, input_path)


def browse_output_file():
    output_path = filedialog.asksaveasfilename(
        defaultextension=".xml",
        filetypes=[("Pliki XML", "*.xml"), ("Pliki JSON", "*.json"), ("Pliki YAML", "*.yaml *.yml")]
    )
    entry_output_path.delete(0, tk.END)
    entry_output_path.insert(0, output_path)


def convert():
    input_path = entry_input_path.get()
    output_path = entry_output_path.get()
    input_format = input_format_var.get()
    output_format = output_format_var.get()
    if not input_path or not output_path or not input_format or not output_format:
        messagebox.showerror("Błąd", "Wszystkie pola są wymagane!")
        return

    try:
        convert_file(input_path, input_format, output_path, output_format)
        messagebox.showinfo("Sukces", f"Plik został pomyślnie skonwertowany do {output_path}")
    except Exception as e:
        messagebox.showerror("Błąd", str(e))




# Ustawienia GUI
root = tk.Tk()
root.title("Konwerter Plików")

frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

label_input_format = tk.Label(frame, text="Format Wejściowy:")
label_input_format.grid(row=0, column=0, padx=5, pady=5, sticky="e")
input_format_var = tk.StringVar(value="XML")
input_format_menu = tk.OptionMenu(frame, input_format_var, "XML", "JSON", "YAML")
input_format_menu.grid(row=0, column=1, padx=5, pady=5)

label_input_path = tk.Label(frame, text="Plik Wejściowy:")
label_input_path.grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_input_path = tk.Entry(frame, width=50)
entry_input_path.grid(row=1, column=1, padx=5, pady=5)
button_browse_input = tk.Button(frame, text="Przeglądaj...", command=browse_input_file)
button_browse_input.grid(row=1, column=2, padx=5, pady=5)

label_output_format = tk.Label(frame, text="Format Wyjściowy:")
label_output_format.grid(row=2, column=0, padx=5, pady=5, sticky="e")
output_format_var = tk.StringVar(value="XML")
output_format_menu = tk.OptionMenu(frame, output_format_var, "XML", "JSON", "YAML")
output_format_menu.grid(row=2, column=1, padx=5, pady=5)

label_output_path = tk.Label(frame, text="Plik Wyjściowy:")
label_output_path.grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_output_path = tk.Entry(frame, width=50)
entry_output_path.grid(row=3, column=1, padx=5, pady=5)
button_browse_output = tk.Button(frame, text="Przeglądaj...", command=browse_output_file)
button_browse_output.grid(row=3, column=2, padx=5, pady=5)

button_convert = tk.Button(root, text="Konwertuj", command=convert)
button_convert.pack(pady=10)

root.mainloop()
