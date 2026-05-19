# -*- coding: utf-8 -*-
"""
Interface Gráfica - Marcatili Kawano Analyzer (5 regiões)

Data: 19/05/2026
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import os

from controllers.marcatili_controller import MarcatiliController


class MarcatiliKawanoGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Marcatili-Kawano Analyzer (5 regiões)")
        self.root.geometry("1450x950")
        self.root.minsize(1100, 750)
        self.root.configure(bg='#f0f0f0')

        self.controller = MarcatiliController()
        self.controller.add_observer(self.on_data_updated)

        self._setup_variables()
        self._setup_styles()
        self._create_widgets()
        self._calculation_done = False

    def _setup_variables(self):
        # Dimensões
        self.width_var = tk.StringVar(value="4.0")
        self.height_var = tk.StringVar(value="4.0")
        self.lambda_var = tk.StringVar(value="1.55")
        # Índices das 5 regiões
        self.n1_var = tk.StringVar(value="1.5")
        self.n2_var = tk.StringVar(value="1.0")   # cover (ar)
        self.n3_var = tk.StringVar(value="1.45")  # direita
        self.n4_var = tk.StringVar(value="1.45")  # inferior
        self.n5_var = tk.StringVar(value="1.45")  # esquerda
        self.mode_x_var = tk.StringVar(value="0")
        self.mode_y_var = tk.StringVar(value="0")
        self.polarization_var = tk.IntVar(value=1)
        self.resolution_var = tk.StringVar(value="301")
        self.extension_var = tk.StringVar(value="2.5")

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 9))
        style.configure('TLabelframe', background='#f0f0f0')
        style.configure('TLabelframe.Label', font=('Segoe UI', 9, 'bold'))

    def _create_widgets(self):
        main = ttk.Frame(self.root)
        main.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left = self._create_left_panel(main)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        right = self._create_right_panel(main)
        right.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def _create_left_panel(self, parent):
        panel = ttk.Frame(parent, width=420)
        panel.pack_propagate(False)

        canvas = tk.Canvas(panel, bg='#f0f0f0', highlightthickness=0)
        scroll = ttk.Scrollbar(panel, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)

        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scroll.set)

        canvas.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")

        tk.Label(scrollable, text="MARCATILI-KAWANO ANALYZER", font=('Segoe UI', 12, 'bold'),
                 bg='#f0f0f0', fg='#2c3e50').pack(pady=10)

        # Geometria
        gframe = ttk.LabelFrame(scrollable, text="Geometria (µm)", padding=8)
        gframe.pack(fill=tk.X, pady=5)
        self._add_entry(gframe, "Largura (2a):", self.width_var, 0)
        self._add_entry(gframe, "Altura (2b):", self.height_var, 1)

        # Ópticos
        oframe = ttk.LabelFrame(scrollable, text="Comprimento de onda", padding=8)
        oframe.pack(fill=tk.X, pady=5)
        self._add_entry(oframe, "λ (µm):", self.lambda_var, 0)

        # Índices das 5 regiões
        nframe = ttk.LabelFrame(scrollable, text="Índices de refração (5 regiões)", padding=8)
        nframe.pack(fill=tk.X, pady=5)
        self._add_entry(nframe, "n₁ (núcleo):", self.n1_var, 0)
        self._add_entry(nframe, "n₂ (superior):", self.n2_var, 1)
        self._add_entry(nframe, "n₃ (direito):", self.n3_var, 2)
        self._add_entry(nframe, "n₄ (inferior):", self.n4_var, 3)
        self._add_entry(nframe, "n₅ (esquerdo):", self.n5_var, 4)

        # Modos
        mframe = ttk.LabelFrame(scrollable, text="Modo", padding=8)
        mframe.pack(fill=tk.X, pady=5)
        self._add_entry(mframe, "p (modo em x):", self.mode_x_var, 0)
        self._add_entry(mframe, "q (modo em y):", self.mode_y_var, 1)

        pol_frame = ttk.Frame(mframe)
        pol_frame.grid(row=2, column=0, columnspan=2, pady=5, sticky='w')
        ttk.Radiobutton(pol_frame, text="TE (E_x)", variable=self.polarization_var, value=1).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(pol_frame, text="TM (E_y)", variable=self.polarization_var, value=2).pack(side=tk.LEFT, padx=5)

        # Malha
        rframe = ttk.LabelFrame(scrollable, text="Malha", padding=8)
        rframe.pack(fill=tk.X, pady=5)
        self._add_entry(rframe, "Resolução (pts):", self.resolution_var, 0)
        self._add_entry(rframe, "Extensão (fator):", self.extension_var, 1)

        # Botões
        btn_frame = ttk.Frame(scrollable)
        btn_frame.pack(fill=tk.X, pady=15)
        self.calc_btn = ttk.Button(btn_frame, text="CALCULAR", command=self._on_calculate)
        self.calc_btn.pack(fill=tk.X, pady=3)
        self.clear_btn = ttk.Button(btn_frame, text="🗑 LIMPAR TUDO", command=self._on_clear)
        self.clear_btn.pack(fill=tk.X, pady=3)
        self.save_btn = ttk.Button(btn_frame, text="SALVAR GRÁFICOS", command=self._on_save, state='disabled')
        self.save_btn.pack(fill=tk.X, pady=3)
        self.export_btn = ttk.Button(btn_frame, text="EXPORTAR DADOS", command=self._on_export, state='disabled')
        self.export_btn.pack(fill=tk.X, pady=3)

        # Resultados textuais
        res_frame = ttk.LabelFrame(scrollable, text="Resultados", padding=5)
        res_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.result_text = tk.Text(res_frame, height=18, width=50, font=('Consolas', 9))
        sc = ttk.Scrollbar(res_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=sc.set)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        sc.pack(side=tk.RIGHT, fill=tk.Y)
        self.result_text.insert(tk.END, "Aguardando cálculo...")

        return panel

    def _add_entry(self, parent, label, var, row):
        ttk.Label(parent, text=label).grid(row=row, column=0, sticky='w', padx=5, pady=2)
        ttk.Entry(parent, textvariable=var, width=12).grid(row=row, column=1, padx=5, pady=2)

    def _create_right_panel(self, parent):
        panel = ttk.Frame(parent)
        self.figure = Figure(figsize=(11, 8), dpi=100, facecolor='white')
        self.figure.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08, hspace=0.35, wspace=0.35)
        self.ax1 = self.figure.add_subplot(2, 2, 1)
        self.ax2 = self.figure.add_subplot(2, 2, 2)
        self.ax3 = self.figure.add_subplot(2, 2, 3)
        self.ax4 = self.figure.add_subplot(2, 2, 4, projection='3d')
        self._clear_plots()  # texto inicial

        self.canvas = FigureCanvasTkAgg(self.figure, master=panel)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        toolbar_frame = ttk.Frame(panel)
        toolbar_frame.pack(fill=tk.X)
        NavigationToolbar2Tk(self.canvas, toolbar_frame).update()
        return panel

    def _clear_plots(self):
        for ax in [self.ax1, self.ax2, self.ax3, self.ax4]:
            ax.clear()
        self.ax1.text(0.5, 0.5, 'Clique em CALCULAR', transform=self.ax1.transAxes, ha='center', va='center', fontsize=12, color='gray')
        self.ax1.set_title('Distribuição do Campo')
        self.ax2.text(0.5, 0.5, 'Aguardando', transform=self.ax2.transAxes, ha='center', va='center')
        self.ax2.set_title('Corte y=0')
        self.ax3.text(0.5, 0.5, 'Aguardando', transform=self.ax3.transAxes, ha='center', va='center')
        self.ax3.set_title('Corte x=0')
        self.ax4.text(0.5, 0.5, 'Aguardando', transform=self.ax4.transAxes, ha='center', va='center')
        self.ax4.set_title('3D')
        self.canvas.draw()

    def _validate_inputs(self):
        try:
            float(self.width_var.get()); float(self.height_var.get()); float(self.lambda_var.get())
            float(self.n1_var.get()); float(self.n2_var.get()); float(self.n3_var.get())
            float(self.n4_var.get()); float(self.n5_var.get())
            int(self.mode_x_var.get()); int(self.mode_y_var.get())
            res = int(self.resolution_var.get())
            if res < 50: self.resolution_var.set("50")
            ext = float(self.extension_var.get())
            if ext < 1.2: self.extension_var.set("1.2")
            if ext > 4.0: self.extension_var.set("4.0")
            return True
        except:
            messagebox.showerror("Erro", "Verifique os valores numéricos")
            return False

    def _on_calculate(self):
        if not self._validate_inputs():
            return
        self._clear_plots()   # limpa gráficos antigos
        try:
            self.controller.set_parameters(
                width_um=float(self.width_var.get()),
                height_um=float(self.height_var.get()),
                wavelength_um=float(self.lambda_var.get()),
                n1=float(self.n1_var.get()), n2=float(self.n2_var.get()),
                n3=float(self.n3_var.get()), n4=float(self.n4_var.get()), n5=float(self.n5_var.get()),
                mode_x=int(self.mode_x_var.get()), mode_y=int(self.mode_y_var.get()),
                polarization=self.polarization_var.get(),
                resolution=int(self.resolution_var.get()),
                extension=float(self.extension_var.get())
            )
            self.controller.calculate()
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, self.controller.get_summary())
            self.save_btn.config(state='normal')
            self.export_btn.config(state='normal')
            self._calculation_done = True
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def on_data_updated(self):
        self._update_plots()

    def _update_plots(self):
        res = self.controller.results
        if res is None or res.field is None:
            return
        params = self.controller.params
        if params is None:
            return

        x_um = res.x_grid * 1e6
        y_um = res.y_grid * 1e6
        field = res.field
        a_um = params.half_width * 1e6
        b_um = params.half_height * 1e6
        tipo = 'E_x' if params.polarization.value == 1 else 'E_y'

        self.ax1.clear()
        im = self.ax1.imshow(field.T, origin='lower', extent=[x_um[0], x_um[-1], y_um[0], y_um[-1]],
                             cmap='jet', aspect='auto')
        self.ax1.set_xlabel('x (μm)'); self.ax1.set_ylabel('y (μm)')
        self.ax1.set_title(f'Distribuição de {tipo}')
        rect = plt.Rectangle((-a_um, -b_um), 2*a_um, 2*b_um, fill=False, edgecolor='white', linewidth=1.5, linestyle='--')
        self.ax1.add_patch(rect)
        self.figure.colorbar(im, ax=self.ax1, label='Campo (u.a.)')

        idx_y = np.argmin(np.abs(res.y_grid))
        self.ax2.clear()
        self.ax2.plot(x_um, field[:, idx_y], 'b-', linewidth=2)
        self.ax2.grid(True, alpha=0.3)
        self.ax2.set_xlabel('x (μm)'); self.ax2.set_ylabel(f'{tipo} (u.a.)')
        self.ax2.set_title('Corte em y = 0')
        self.ax2.axvline(-a_um, color='r', linestyle='--'); self.ax2.axvline(a_um, color='r', linestyle='--')
        self.ax2.set_ylim(-1.1, 1.1)

        idx_x = np.argmin(np.abs(res.x_grid))
        self.ax3.clear()
        self.ax3.plot(y_um, field[idx_x, :], 'r-', linewidth=2)
        self.ax3.grid(True, alpha=0.3)
        self.ax3.set_xlabel('y (μm)'); self.ax3.set_ylabel(f'{tipo} (u.a.)')
        self.ax3.set_title('Corte em x = 0')
        self.ax3.axvline(-b_um, color='b', linestyle='--'); self.ax3.axvline(b_um, color='b', linestyle='--')
        self.ax3.set_ylim(-1.1, 1.1)

        Xm, Ym = np.meshgrid(x_um, y_um)
        self.ax4.clear()
        self.ax4.plot_surface(Xm, Ym, field.T, cmap='jet', edgecolor='none', alpha=0.9)
        self.ax4.set_xlabel('x (μm)'); self.ax4.set_ylabel('y (μm)'); self.ax4.set_zlabel('Campo (u.a.)')
        self.ax4.set_title('Visualização 3D')
        self.ax4.view_init(elev=30, azim=45)

        tipo_pol = "TE" if params.polarization.value == 1 else "TM"
        self.figure.suptitle(f'Marcatili-Kawano - Modo {tipo_pol}_{{{params.mode_x}{params.mode_y}}}', fontsize=14)
        self.canvas.draw()

    def _on_clear(self):
        if messagebox.askyesno("Limpar tudo", "Resetar todos os parâmetros e gráficos?"):
            # reset campos
            self.width_var.set("4.0"); self.height_var.set("4.0"); self.lambda_var.set("1.55")
            self.n1_var.set("1.5"); self.n2_var.set("1.0"); self.n3_var.set("1.45")
            self.n4_var.set("1.45"); self.n5_var.set("1.45")
            self.mode_x_var.set("0"); self.mode_y_var.set("0")
            self.polarization_var.set(1)
            self.resolution_var.set("301"); self.extension_var.set("2.5")
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Aguardando cálculo...")
            self._clear_plots()
            self.save_btn.config(state='disabled')
            self.export_btn.config(state='disabled')
            self._calculation_done = False
            self.controller.reset()

    def _on_save(self):
        if not self._calculation_done:
            messagebox.showwarning("Aviso", "Nenhum dado para salvar.")
            return
        dirname = filedialog.askdirectory()
        if dirname:
            fname = f"MarcatiliKawano_{self.controller.params.mode_x}{self.controller.params.mode_y}.png"
            self.figure.savefig(os.path.join(dirname, fname), dpi=300)
            messagebox.showinfo("Sucesso", f"Salvo em {dirname}")

    def _on_export(self):
        if not self._calculation_done:
            messagebox.showwarning("Aviso", "Nenhum dado para exportar.")
            return
        fpath = filedialog.asksaveasfilename(defaultextension=".npz")
        if fpath:
            res = self.controller.results
            par = self.controller.params
            np.savez_compressed(fpath, x_grid=res.x_grid, y_grid=res.y_grid,
                                field=res.field, intensity=res.intensity,
                                kx=res.kx, ky=res.ky, beta=res.beta, n_eff=res.n_eff,
                                n1=par.n1, n2=par.n2, n3=par.n3, n4=par.n4, n5=par.n5)
            messagebox.showinfo("Sucesso", "Dados exportados.")

    def run(self):
        self.root.mainloop()