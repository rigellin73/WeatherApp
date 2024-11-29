import tkinter as tk
from tkinter import ttk


def create_weather_entries(content_frame, weather_info_dict):
    # create result as a table
    for index, key in enumerate(weather_info_dict):
        key_entry = tk.Entry(content_frame, width=20, fg='blue', font=('Arial', 16, 'bold'))
        value_entry = tk.Entry(content_frame, width=20, fg='blue', font=('Arial', 16, 'bold'))
        key_entry.grid(row=index, column=0)
        value_entry.grid(row=index, column=1)
        key_entry.insert(tk.END, key)
        value_entry.insert(tk.END, weather_info_dict[key])


def create_window_content(window, api_response):

    # Step 3: Create a Frame for Grid Layout
    frame = ttk.Frame(window)
    frame.grid(row=0, column=0, sticky="nsew")

    # Step 4: Create a Canvas and Scrollbar
    canvas = tk.Canvas(frame)
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Step 5: Create a Frame for Scrollable Content
    content_frame = ttk.Frame(canvas)

    # Step 6: Configure the Canvas and Scrollable Content Frame
    content_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    create_weather_entries(content_frame, api_response)

    # Step 8: Create Window Resizing Configuration
    window.columnconfigure(0, weight=1)
    window.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    # Step 9: Pack Widgets onto the Window
    canvas.create_window((0, 0), window=content_frame, anchor="nw")
    canvas.grid(row=0, column=0, sticky="nsew")
    scrollbar.grid(row=0, column=1, sticky="ns")

    # Step 10: Bind the Canvas to Mousewheel Events
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)