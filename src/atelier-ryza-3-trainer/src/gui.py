import tkinter as tk
from tkinter import ttk
from src.trainer_core import AtelierRyza3Trainer

class TrainerGUI:
    """
    Simple Tkinter GUI for controlling the Atelier Ryza 3 trainer.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Atelier Ryza 3 Trainer")
        self.root.geometry("300x250")
        self.root.resizable(False, False)

        self.trainer = AtelierRyza3Trainer()
        self.attached = False

        # Status label
        self.status_label = ttk.Label(root, text="Not attached to game", foreground="red")
        self.status_label.pack(pady=10)

        # Attach button
        self.attach_btn = ttk.Button(root, text="Attach to Game", command=self.attach_game)
        self.attach_btn.pack(pady=5)

        # Infinite HP checkbox
        self.hp_var = tk.BooleanVar()
        self.hp_check = ttk.Checkbutton(root, text="Infinite HP", variable=self.hp_var, command=self.toggle_hp)
        self.hp_check.pack(pady=5)

        # Infinite MP checkbox
        self.mp_var = tk.BooleanVar()
        self.mp_check = ttk.Checkbutton(root, text="Infinite MP", variable=self.mp_var, command=self.toggle_mp)
        self.mp_check.pack(pady=5)

        # Infinite AP checkbox
        self.ap_var = tk.BooleanVar()
        self.ap_check = ttk.Checkbutton(root, text="Infinite AP", variable=self.ap_var, command=self.toggle_ap)
        self.ap_check.pack(pady=5)

        # Infinite Items checkbox
        self.items_var = tk.BooleanVar()
        self.items_check = ttk.Checkbutton(root, text="Infinite Items", variable=self.items_var, command=self.toggle_items)
        self.items_check.pack(pady=5)

        # Exit button
        self.exit_btn = ttk.Button(root, text="Exit", command=self.on_exit)
        self.exit_btn.pack(pady=10)

    def attach_game(self) -> None:
        """Attach to the game process."""
        if self.trainer.attach():
            self.attached = True
            self.status_label.config(text="Attached to game", foreground="green")
            self.attach_btn.config(state=tk.DISABLED)
        else:
            self.status_label.config(text="Failed to attach", foreground="red")

    def toggle_hp(self) -> None:
        """Toggle infinite HP."""
        if self.attached:
            self.trainer.set_infinite_hp(self.hp_var.get())

    def toggle_mp(self) -> None:
        """Toggle infinite MP."""
        if self.attached:
            self.trainer.set_infinite_mp(self.mp_var.get())

    def toggle_ap(self) -> None:
        """Toggle infinite AP."""
        if self.attached:
            self.trainer.set_infinite_ap(self.ap_var.get())

    def toggle_items(self) -> None:
        """Toggle infinite items."""
        if self.attached:
            self.trainer.set_infinite_items(self.items_var.get())

    def on_exit(self) -> None:
        """Clean up and exit."""
        if self.attached:
            self.trainer.detach()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainerGUI(root)
    root.mainloop()
