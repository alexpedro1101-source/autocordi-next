import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from procesador import procesar_registro


# ================= CONFIG =================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("AutoCoordi NEXT A")
app.geometry("850x520")

contador = 0
historial = []


# ================= CONTAINER =================
container = ctk.CTkFrame(app, fg_color="#0f172a")
container.pack(fill="both", expand=True, padx=10, pady=10)


# ================= HEADER =================
header = ctk.CTkFrame(container, fg_color="#111c2e", corner_radius=12)
header.pack(fill="x", padx=10, pady=10)

ctk.CTkLabel(
    header,
    text="⚡Coordi NEXT A ",
    font=("Arial", 20, "bold")
).pack(side="left", padx=15, pady=10)


# ================= KPI =================
kpi = ctk.CTkFrame(container, fg_color="#111c2e", corner_radius=12)
kpi.pack(fill="x", padx=10)

lbl_kpi = ctk.CTkLabel(kpi, text="📊 Registros: 0 | ⚡ Procesados: 0")
lbl_kpi.pack(padx=10, pady=8)


# ================= INPUT =================
input_card = ctk.CTkFrame(container, fg_color="#111c2e", corner_radius=12)
input_card.pack(fill="x", padx=10, pady=10)

ctk.CTkLabel(
    input_card,
    text="📝 Entrada de registro",
    font=("Arial", 13, "bold")
).pack(anchor="w", padx=10)

txt_input = ctk.CTkTextbox(input_card, height=90, fg_color="#0b1220")
txt_input.pack(fill="x", padx=10, pady=8)


# ================= BOTONES =================
btn_frame = ctk.CTkFrame(container, fg_color="#111c2e", corner_radius=12)
btn_frame.pack(fill="x", padx=10, pady=5)


# ================= FUNCION =================
def procesar():
    global contador, historial

    texto = txt_input.get("1.0", "end").strip()

    if not texto:
        messagebox.showwarning("Aviso", "Ingrese registro")
        return

    salida1, salida2 = procesar_registro(texto)

    txt_out1.delete("1.0", "end")
    txt_out1.insert("1.0", salida1)

    txt_out2.delete("1.0", "end")
    txt_out2.insert("1.0", salida2)

    contador += 1
    lbl_kpi.configure(text=f"📊 Registros: {contador} | ⚡ Procesados: {contador}")

    historial.append(f"{datetime.now().strftime('%H:%M:%S')} | {salida1}")

    txt_hist.delete("1.0", "end")
    for h in historial[-5:]:
        txt_hist.insert("end", h + "\n")


ctk.CTkButton(
    btn_frame,
    text="⚙️ Procesar",
    command=procesar,
    width=180,
    height=35
).pack(side="left", padx=10, pady=10)

ctk.CTkButton(
    btn_frame,
    text="🧹 Limpiar",
    command=lambda: txt_input.delete("1.0", "end"),
    width=180,
    height=35
).pack(side="left", padx=10, pady=10)


# ================= SALIDA TÉCNICA =================
card1 = ctk.CTkFrame(container, fg_color="#111c2e", corner_radius=12)
card1.pack(fill="x", padx=10, pady=5)

ctk.CTkLabel(
    card1,
    text="📌 Salida Técnica",
    font=("Arial", 13, "bold")
).pack(anchor="w", padx=10)

txt_out1 = ctk.CTkTextbox(card1, height=80, fg_color="#0b1220")
txt_out1.pack(fill="x", padx=10, pady=8)


# ================= SALIDA CORREO =================
card2 = ctk.CTkFrame(container, fg_color="#111c2e", corner_radius=12)
card2.pack(fill="x", padx=10, pady=5)

ctk.CTkLabel(
    card2,
    text="✉️ Correo Automático",
    font=("Arial", 13, "bold")
).pack(anchor="w", padx=10)

txt_out2 = ctk.CTkTextbox(card2, height=90, fg_color="#0b1220")
txt_out2.pack(fill="x", padx=10, pady=8)


# ================= HISTORIAL =================
card3 = ctk.CTkFrame(container, fg_color="#111c2e", corner_radius=12)
card3.pack(fill="x", padx=10, pady=5)

ctk.CTkLabel(
    card3,
    text="📜 Historial",
    font=("Arial", 13, "bold")
).pack(anchor="w", padx=10)

txt_hist = ctk.CTkTextbox(card3, height=80, fg_color="#0b1220")
txt_hist.pack(fill="x", padx=10, pady=8)


# ================= RUN =================
app.mainloop()