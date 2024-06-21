import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import winsound

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        self.work_time = 25 * 60  # 25 minutes in seconds
        self.short_break = 5 * 60  # 5 minutes in seconds
        self.long_break = 15 * 60  # 15 minutes in seconds
        self.current_time = self.work_time
        self.is_running = False
        self.sessions = 4

        self.create_widgets()
        self.update_timer()

    def create_widgets(self):
        self.timer_frame = tk.Frame(self.root)
        self.timer_frame.pack(pady=20)

        self.timer_label = tk.Label(self.timer_frame, text="Pomodoro Timer", font=("Helvetica", 24))
        self.timer_label.pack(pady=10)

        self.time_display = tk.Label(self.timer_frame, text=self.format_time(self.current_time), font=("Helvetica", 48))
        self.time_display.pack(pady=10)

        self.progress = ttk.Progressbar(self.timer_frame, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        self.buttons_frame = tk.Frame(self.timer_frame)
        self.buttons_frame.pack(pady=10)

        self.start_button = tk.Button(self.buttons_frame, text="Start", command=self.start_timer, font=("Helvetica", 14))
        self.start_button.grid(row=0, column=0, padx=10)

        self.pause_button = tk.Button(self.buttons_frame, text="Pause", command=self.pause_timer, font=("Helvetica", 14))
        self.pause_button.grid(row=0, column=1, padx=10)

        self.reset_button = tk.Button(self.buttons_frame, text="Reset", command=self.reset_timer, font=("Helvetica", 14))
        self.reset_button.grid(row=0, column=2, padx=10)

        self.settings_button = tk.Button(self.buttons_frame, text="Settings", command=self.open_settings, font=("Helvetica", 14))
        self.settings_button.grid(row=0, column=3, padx=10)

        self.about_button = tk.Button(self.buttons_frame, text="About", command=self.show_about, font=("Helvetica", 14))
        self.about_button.grid(row=0, column=4, padx=10)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(pady=10)

        self.notes_frame = tk.Frame(self.notebook, width=400, height=200)
        self.notes_frame.pack(fill="both", expand=True)
        self.notebook.add(self.notes_frame, text="Notes")

        self.notes_text = tk.Text(self.notes_frame, wrap="word")
        self.notes_text.pack(expand=True, fill="both")

        self.postit_frame = tk.Frame(self.notebook, width=400, height=200)
        self.postit_frame.pack(fill="both", expand=True)
        self.notebook.add(self.postit_frame, text="Post-it")

        self.postit_text = tk.Text(self.postit_frame, wrap="word", bg="yellow")
        self.postit_text.pack(expand=True, fill="both")

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.countdown()

    def pause_timer(self):
        if self.is_running:
            self.is_running = False

    def reset_timer(self):
        self.is_running = False
        self.sessions = 0
        self.current_time = self.work_time
        self.update_timer()
        self.progress['value'] = 0

    def countdown(self):
        if self.is_running:
            if self.current_time > 0:
                self.current_time -= 1
                self.update_timer()
                self.progress['value'] = 100 - (self.current_time / self.work_time * 100)
                self.root.after(1000, self.countdown)
            else:
                self.is_running = False
                self.sessions += 1
                winsound.Beep(1000, 1000)  # Beep sound when time is up

                if self.sessions % 4 == 0:
                    self.current_time = self.long_break
                    messagebox.showinfo("Long Break", "Time for a long break!")
                elif self.sessions % 2 == 0:
                    self.current_time = self.work_time
                    messagebox.showinfo("Work Time", "Time to get back to work!")
                else:
                    self.current_time = self.short_break
                    messagebox.showinfo("Short Break", "Time for a short break!")

                self.start_timer()

    def update_timer(self):
        self.time_display.config(text=self.format_time(self.current_time))

    def format_time(self, seconds):
        minutes = seconds // 60
        seconds = seconds % 60
        return f"{minutes:02d}:{seconds:02d}"

    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x200")

        tk.Label(settings_window, text="Work Time (minutes):").pack(pady=10)
        work_time_entry = tk.Entry(settings_window)
        work_time_entry.insert(0, str(self.work_time // 60))
        work_time_entry.pack(pady=5)

        tk.Label(settings_window, text="Short Break (minutes):").pack(pady=10)
        short_break_entry = tk.Entry(settings_window)
        short_break_entry.insert(0, str(self.short_break // 60))
        short_break_entry.pack(pady=5)

        tk.Label(settings_window, text="Long Break (minutes):").pack(pady=10)
        long_break_entry = tk.Entry(settings_window)
        long_break_entry.insert(0, str(self.long_break // 60))
        long_break_entry.pack(pady=5)

        def save_settings():
            self.work_time = int(work_time_entry.get()) * 60
            self.short_break = int(short_break_entry.get()) * 60
            self.long_break = int(long_break_entry.get()) * 60
            self.current_time = self.work_time
            self.update_timer()
            settings_window.destroy()

        save_button = tk.Button(settings_window, text="Save", command=save_settings)
        save_button.pack(pady=20)

    def show_about(self):
        about_message = (
            "Pomodoro Timer\n\n"
            "Version 1.0\n"
            "Développé par [Dimonapatrick243]\n\n"
            "Cette application utilise la technique Pomodoro pour améliorer "
            "la gestion du temps et la productivité. Vous pouvez personnaliser "
            "les durées de travail et de pause, et prendre des notes dans les "
            "sections Notes et Post-it.\n\n"
            "Merci d'utiliser notre application!"
        )
        messagebox.showinfo("About", about_message)

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
