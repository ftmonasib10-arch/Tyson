import tkinter as tk
from tkinter import ttk
import math
from fractions import Fraction

# ---------- ANIQ QIYMATLAR (ILDIZLIK) ----------
ANIQ = {
    0:   {"sin": "0", "cos": "1", "tg": "0", "ctg": "aniqlanmagan"},
    15:  {"sin": "(√6 - √2)/4", "cos": "(√6 + √2)/4", "tg": "2 - √3", "ctg": "2 + √3"},
    30:  {"sin": "1/2", "cos": "√3/2", "tg": "√3/3", "ctg": "√3"},
    45:  {"sin": "√2/2", "cos": "√2/2", "tg": "1", "ctg": "1"},
    60:  {"sin": "√3/2", "cos": "1/2", "tg": "√3", "ctg": "√3/3"},
    75:  {"sin": "(√6 + √2)/4", "cos": "(√6 - √2)/4", "tg": "2 + √3", "ctg": "2 - √3"},
    90:  {"sin": "1", "cos": "0", "tg": "aniqlanmagan", "ctg": "0"},
    120: {"sin": "√3/2", "cos": "-1/2", "tg": "-√3", "ctg": "-√3/3"},
    135: {"sin": "√2/2", "cos": "-√2/2", "tg": "-1", "ctg": "-1"},
    150: {"sin": "1/2", "cos": "-√3/2", "tg": "-√3/3", "ctg": "-√3"},
    180: {"sin": "0", "cos": "-1", "tg": "0", "ctg": "aniqlanmagan"},
    210: {"sin": "-1/2", "cos": "-√3/2", "tg": "√3/3", "ctg": "√3"},
    225: {"sin": "-√2/2", "cos": "-√2/2", "tg": "1", "ctg": "1"},
    240: {"sin": "-√3/2", "cos": "-1/2", "tg": "√3", "ctg": "√3/3"},
    270: {"sin": "-1", "cos": "0", "tg": "aniqlanmagan", "ctg": "0"},
    300: {"sin": "-√3/2", "cos": "1/2", "tg": "-√3", "ctg": "-√3/3"},
    315: {"sin": "-√2/2", "cos": "√2/2", "tg": "-1", "ctg": "-1"},
    330: {"sin": "-1/2", "cos": "√3/2", "tg": "-√3/3", "ctg": "-√3"},
    360: {"sin": "0", "cos": "1", "tg": "0", "ctg": "aniqlanmagan"},
}

def kasrga(q):
    if q is None: return "—"
    if abs(q) < 1e-12: return "0"
    if abs(q) > 1e9: return "aniqlanmagan"
    try:
        f = Fraction(q).limit_denominator(1000)
        return f"{f.numerator}/{f.denominator}" if f.denominator != 1 else str(f.numerator)
    except:
        return "—"

class TrigApp:
    def __init__(self, root):
        self.root = root
        root.title("Trigonometrik Kalkulyator - Premium")
        root.geometry("1100x760")
        root.configure(bg="#0B0B14")
        
        # Styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container
        main = tk.Frame(root, bg="#0B0B14")
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header = tk.Frame(main, bg="#0B0B14")
        header.pack(fill="x", pady=(0,15))
        tk.Label(header, text="Trigonometrik Kalkulyator", font=("Manrope", 26, "bold"), bg="#0B0B14", fg="white").pack(side="left")
        tk.Label(header, text="  sin • cos • tg • ctg  —  ildiz / kasr / o'nlik", font=("Manrope", 11), bg="#0B0B14", fg="#8B8BA7").pack(side="left", padx=15, pady=8)

        content = tk.Frame(main, bg="#0B0B14")
        content.pack(fill="both", expand=True)

        # Left panel - controls + circle
        left = tk.Frame(content, bg="#151526", highlightbackground="#2A2A4A", highlightthickness=1)
        left.pack(side="left", fill="both", padx=(0,12), ipadx=15, ipady=15)
        left.configure(width=360)
        left.pack_propagate(False)

        tk.Label(left, text="Gradusni kiriting", font=("Manrope", 12, "bold"), bg="#151526", fg="#A5A5C0").pack(anchor="w")

        entry_frame = tk.Frame(left, bg="#1E1E36", highlightbackground="#3A3A6A", highlightthickness=1)
        entry_frame.pack(fill="x", pady=10)
        
        self.deg_var = tk.DoubleVar(value=45.0)
        self.entry = tk.Entry(entry_frame, textvariable=self.deg_var, font=("Manrope", 22, "bold"), bg="#1E1E36", fg="white", bd=0, insertbackground="white", justify="center")
        self.entry.pack(fill="x", padx=10, pady=12)
        self.entry.bind("<KeyRelease>", lambda e: self.update_calc())
        self.entry.bind("<Return>", lambda e: self.update_calc())

        # slider
        self.slider = tk.Scale(left, from_=-180, to=540, orient="horizontal", variable=self.deg_var, command=lambda v: self.update_calc(),
                               bg="#151526", fg="#7C5CFF", highlightthickness=0, troughcolor="#2A2A4A", activebackground="#7C5CFF", length=330)
        self.slider.pack(fill="x", pady=5)

        # quick buttons
        quick_frame = tk.Frame(left, bg="#151526")
        quick_frame.pack(fill="x", pady=12)
        tk.Label(quick_frame, text="Tez tanlash:", font=("Manrope", 10), bg="#151526", fg="#8B8BA7").pack(anchor="w", pady=(0,6))
        
        btns = [0,30,45,60,90,120,135,150,180,210,270,360]
        grid = tk.Frame(quick_frame, bg="#151526")
        grid.pack(fill="x")
        for i, b in enumerate(btns):
            r, c = divmod(i, 4)
            tk.Button(grid, text=f"{b}°", font=("Manrope", 10, "bold"), bg="#252542", fg="white", bd=0, padx=12, pady=8,
                      activebackground="#7C5CFF", activeforeground="white",
                      command=lambda v=b: self.set_deg(v)).grid(row=r, column=c, padx=4, pady=4, sticky="ew")
        for c in range(4): grid.columnconfigure(c, weight=1)

        # Unit circle canvas
        tk.Label(left, text="Birlik aylana", font=("Manrope", 12, "bold"), bg="#151526", fg="#A5A5C0").pack(anchor="w", pady=(20,10))
        self.canvas = tk.Canvas(left, width=330, height=330, bg="#101022", highlightthickness=0)
        self.canvas.pack()

        # Right panel - results
        right = tk.Frame(content, bg="#0B0B14")
        right.pack(side="right", fill="both", expand=True)

        self.cards = {}
        for name in ["sin", "cos", "tg", "ctg"]:
            card = tk.Frame(right, bg="#151526", highlightbackground="#2A2A4A", highlightthickness=1)
            card.pack(fill="x", pady=6, ipadx=12, ipady=12)
            
            top = tk.Frame(card, bg="#151526")
            top.pack(fill="x")
            color = {"sin":"#7C5CFF","cos":"#00D9FF","tg":"#FF6B9D","ctg":"#FFD93D"}[name]
            tk.Label(top, text=name, font=("Manrope", 18, "bold"), bg="#151526", fg=color, width=4).pack(side="left")
            tk.Label(top, text=f"{name}(θ)", font=("Manrope", 10), bg="#151526", fg="#6B6B8A").pack(side="left")
            
            body = tk.Frame(card, bg="#151526")
            body.pack(fill="x", pady=(8,0))
            
            labels = {}
            for idx, (lbl_text, key) in enumerate([("Ildizlik ko'rinish","ildiz"), ("Kasrlik ko'rinish","kasr"), ("O'nlik ko'rinish","onlik")]):
                row = tk.Frame(body, bg="#151526")
                row.pack(fill="x", pady=3)
                tk.Label(row, text=lbl_text+":", font=("Manrope", 9), bg="#151526", fg="#8B8BA7", width=18, anchor="w").pack(side="left")
                val_lbl = tk.Label(row, text="—", font=("Consolas", 11, "bold"), bg="#151526", fg="white", anchor="w")
                val_lbl.pack(side="left", fill="x", expand=True)
                labels[key] = val_lbl
            
            self.cards[name] = labels

        self.update_calc()

    def set_deg(self, v):
        self.deg_var.set(float(v))
        self.update_calc()

    def get_ildiz(self, norm_deg, func):
        # eng yaqin aniq burchakni topish
        nd = norm_deg % 360
        # 0.5 gradus tolerant
        for k in ANIQ:
            if abs(nd - k) < 0.51 or abs(nd - 360 - k) < 0.51 or (k==0 and nd>359.5):
                return ANIQ[k][func]
        return "aniq ildiz yo'q"

    def update_calc(self):
        try:
            deg = float(self.deg_var.get())
        except:
            return
        
        rad = math.radians(deg)
        sin_v = math.sin(rad)
        cos_v = math.cos(rad)
        
        tg_v = None if abs(cos_v) < 1e-12 else math.tan(rad)
        ctg_v = None if abs(sin_v) < 1e-12 else cos_v / sin_v

        norm = deg % 360

        vals = {"sin": sin_v, "cos": cos_v, "tg": tg_v, "ctg": ctg_v}
        
        for name in ["sin","cos","tg","ctg"]:
            v = vals[name]
            card = self.cards[name]
            if v is None:
                card["ildiz"].config(text="aniqlanmagan", fg="#FF6B6B")
                card["kasr"].config(text="—")
                card["onlik"].config(text="—")
            else:
                ildiz = self.get_ildiz(norm, name)
                card["ildiz"].config(text=ildiz, fg="#C3B5FF" if "√" in ildiz else "white")
                card["kasr"].config(text=kasrga(v))
                card["onlik"].config(text=f"{v:.10f}".rstrip('0').rstrip('.') if abs(v)>=1e-9 else "0")

        self.draw_circle(deg, sin_v, cos_v)

    def draw_circle(self, deg, sin_v, cos_v):
        c = self.canvas
        c.delete("all")
        w = 330
        h = 330
        cx, cy = w//2, h//2
        R = 120

        # grid
        c.create_oval(cx-R, cy-R, cx+R, cy+R, outline="#2A2A4A", width=2)
        c.create_line(cx-R-10, cy, cx+R+10, cy, fill="#2A2A4A", dash=(3,3))
        c.create_line(cx, cy-R-10, cx, cy+R+10, fill="#2A2A4A", dash=(3,3))

        # angle
        rad = math.radians(deg)
        x = cx + R * math.cos(rad)
        y = cy - R * math.sin(rad)

        # lines
        c.create_line(cx, cy, x, y, fill="#7C5CFF", width=3)
        c.create_oval(x-6, y-6, x+6, y+6, fill="#7C5CFF", outline="")
        
        # sin cos projection
        proj_x = cx + R * math.cos(rad)
        proj_y = cy
        c.create_line(x, y, proj_x, proj_y, fill="#00D9FF", width=1, dash=(4,4))
        c.create_line(x, y, cx, y, fill="#FF6B9D", width=1, dash=(4,4))

        c.create_text(cx, 18, text=f"{deg:.1f}°", fill="white", font=("Manrope", 14, "bold"))

if __name__ == "__main__":
    root = tk.Tk()
    app = TrigApp(root)
    root.mainloop()