import tkinter as tk

# from tkinter import ttk
import ttkbootstrap as ttk
from tkinter import messagebox
from RCC_Beam import RCCBeam  # Assuming your module is named rcc_beam_module.py


class RCCBeamApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RCC Beam Design App")

        self.fck_label = ttk.Label(root, text="Concrete Grade (fck) (MPa):")
        self.fck_entry = ttk.Entry(root)
        self.fck_label.grid(row=0, column=0, sticky=tk.W)
        self.fck_entry.grid(row=0, column=1)

        self.fy_label = ttk.Label(root, text="Steel Grade (fy) (MPa):")
        self.fy_entry = ttk.Entry(root)
        self.fy_label.grid(row=1, column=0, sticky=tk.W)
        self.fy_entry.grid(row=1, column=1)

        self.b_label = ttk.Label(root, text="Width of Beam (mm):")
        self.b_entry = ttk.Entry(root)
        self.b_label.grid(row=2, column=0, sticky=tk.W)
        self.b_entry.grid(row=2, column=1)

        self.h_label = ttk.Label(root, text="Depth of Beam (mm):")
        self.h_entry = ttk.Entry(root)
        self.h_label.grid(row=3, column=0, sticky=tk.W)
        self.h_entry.grid(row=3, column=1)

        self.Mu_label = ttk.Label(root, text="Design Moment (kNm):")
        self.Mu_entry = ttk.Entry(root)
        self.Mu_label.grid(row=4, column=0, sticky=tk.W)
        self.Mu_entry.grid(row=4, column=1)

        self.calculate_button = ttk.Button(
            root, text="Calculate", command=self.calculate_beam
        )
        self.calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

    def calculate_beam(self):
        try:
            fck = float(self.fck_entry.get())
            fy = float(self.fy_entry.get())
            b = float(self.b_entry.get())
            h = float(self.h_entry.get())
            Mu = float(self.Mu_entry.get())

            beam = RCCBeam(fck, fy, b, h, Mu)
            result = f"Required Area of Steel (mm^2): {beam.calculate_Ast_req()}\n"
            result += f"Design Moment Limit (kNm): {beam.Mu_lim}\n"
            messagebox.showinfo("Results", result)
        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers.")


if __name__ == "__main__":
    root = tk.Tk()
    app = RCCBeamApp(root)
    root.mainloop()
