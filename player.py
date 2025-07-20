import customtkinter as ctk
from tkinter import filedialog
import pygame
import os
from mutagen.mp3 import MP3
import time
from threading import Thread

pygame.mixer.init()
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("🎵 Advanced Music Player")
app.geometry("600x500")

paused = False
music_list = []
current_index = -1
current_song_length = 0
music_playing = False

# -------- Functions --------

def load_songs():
    global music_list
    files = filedialog.askopenfilenames(title="Select Songs", filetypes=[("MP3 files", "*.mp3")])
    for file in files:
        music_list.append(file)
        playlist.insert("end", os.path.basename(file))

def play_selected():
    global current_index
    if playlist.curselection():
        current_index = playlist.curselection()[0]
        play_song()

def play_song():
    global paused, current_song_length, music_playing
    if current_index != -1:
        pygame.mixer.music.load(music_list[current_index])
        pygame.mixer.music.play()
        song = MP3(music_list[current_index])
        current_song_length = song.info.length
        song_label.configure(text=os.path.basename(music_list[current_index]))
        paused = False
        music_playing = True
        update_seekbar()

def pause_resume_song():
    global paused
    if music_playing:
        if not paused:
            pygame.mixer.music.pause()
            paused = True
        else:
            pygame.mixer.music.unpause()
            paused = False

def stop_song():
    global music_playing
    pygame.mixer.music.stop()
    song_label.configure(text="No song playing")
    music_playing = False

def set_volume(val):
    pygame.mixer.music.set_volume(float(val))

def update_seekbar():
    def run():
        while music_playing and not paused:
            if current_song_length > 0:
                try:
                    pos = pygame.mixer.music.get_pos() / 1000
                    seek_slider.set((pos / current_song_length) * 100)
                    time.sleep(1)
                except:
                    break
    Thread(target=run, daemon=True).start()

def seek_music(val):
    if current_song_length > 0:
        seek_sec = float(val) * current_song_length / 100
        pygame.mixer.music.play(start=seek_sec)

# -------- UI Elements --------

# Title
song_label = ctk.CTkLabel(app, text="No song playing", font=("Arial", 18))
song_label.pack(pady=15)

# Playlist Box
import tkinter as tk  # add this at the top with your imports if not already

# Create a CTk frame to hold the tk Listbox (for visual consistency)
playlist_frame = ctk.CTkFrame(app)
playlist_frame.pack(pady=10)

playlist = tk.Listbox(playlist_frame, width=60, height=7, bg="#2b2b2b", fg="white", selectbackground="#1f6aa5", selectforeground="white", highlightbackground="#444")
playlist.pack()

playlist.pack(pady=10)

# Load + Play Selected Buttons
button_frame = ctk.CTkFrame(app)
button_frame.pack(pady=10)

btn_load = ctk.CTkButton(button_frame, text="📁 Load Songs", command=load_songs, width=140)
btn_load.grid(row=0, column=0, padx=10)

btn_select = ctk.CTkButton(button_frame, text="▶️ Play Selected", command=play_selected, width=140)
btn_select.grid(row=0, column=1, padx=10)

# Control Buttons
control_frame = ctk.CTkFrame(app)
control_frame.pack(pady=15)

btn_play = ctk.CTkButton(control_frame, text="▶️ Play", command=play_song, width=100)
btn_play.grid(row=0, column=0, padx=5)

btn_pause = ctk.CTkButton(control_frame, text="⏸️ Pause/Resume", command=pause_resume_song, width=150)
btn_pause.grid(row=0, column=1, padx=5)

btn_stop = ctk.CTkButton(control_frame, text="⏹️ Stop", command=stop_song, width=100)
btn_stop.grid(row=0, column=2, padx=5)

# Volume Slider
volume_slider = ctk.CTkSlider(app, from_=0, to=1, command=set_volume)
volume_slider.set(0.5)
volume_slider.pack(pady=10)
ctk.CTkLabel(app, text="Volume").pack()

# Seek Slider
seek_slider = ctk.CTkSlider(app, from_=0, to=100, command=seek_music)
seek_slider.set(0)
seek_slider.pack(pady=10)
ctk.CTkLabel(app, text="Seek").pack()

# Run the app
app.mainloop()
