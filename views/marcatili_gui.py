# -*- coding: utf-8 -*-
"""
====================================================================================================
View - Interface gráfica do usuário
Implementa o padrão Observer para atualização automática

Data: 13/04/2026
====================================================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import numpy as np
import os

from controllers.marcatili_controller import MarcatiliController


class MarcatiliGUI:
    """
    Classe da interface gráfica
    Implementa o padrão MVC como View
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Método de Marcatili - Análise de Guias de Onda Ópticos")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        self.root.configure(bg='#f0f0f0')
        
        # Controller
        self.controller = MarcatiliController()
        self.controller.add_observer(self.on_data_updated)
        
        # Variáveis de interface
        self._setup_variables()
        
        # Configurar estilo
        self._setup_styles()
        
        # Criar interface
        self._create_widgets()
        
        # Estado
        self._calculation_done = False
    
    def _setup_variables(self):
        """Configura as variáveis de interface"""
        self.width_var = tk.StringVar(value="4.0")
        self.height_var = tk.StringVar(value="4.0")
        self.lambda_var = tk.StringVar(value="1.55")
        self.n1_var = tk.StringVar(value="1.5")
        self.n2_var = tk.StringVar(value="1.4")
        self.mode_x_var = tk.StringVar(value="0")
        self.mode_y_var = tk.StringVar(value="0")
        self.polarization_var = tk.IntVar(value=1)
        self.resolution_var = tk.StringVar(value="301")
        self.extension_var = tk.StringVar(value="2.5")
    
    def _setup_styles(self):
        """Configura estilos da interface"""
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure('Title.TLabel', font=('Segoe UI', 14, 'bold'), 
                       foreground='#2c3e50', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0', font=('Segoe UI', 10))
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabelframe', background='#f0f0f0', font=('Segoe UI', 10, 'bold'))
        style.configure('TLabelframe.Label', background='#f0f0f0', font=('Segoe UI', 10, 'bold'))
        style.configure('TButton', font=('Segoe UI', 10))
        style.configure('TEntry', font=('Segoe UI', 10))
    
    def _create_widgets(self):
        """Cria todos os widgets da interface"""
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Painel esquerdo (parâmetros)
        left_panel = self._create_left_panel(main_frame)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        
        # Painel direito (gráficos)
        right_panel = self._create_right_panel(main_frame)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    def _create_left_panel(self, parent):
        """Cria o painel esquerdo com parâmetros"""
        panel = ttk.Frame(parent, width=380)
        panel.pack_propagate(False)
        
        # Canvas com scroll
        canvas = tk.Canvas(panel, bg='#f0f0f0', highlightthickness=0)
        scrollbar = ttk.Scrollbar(panel, orient="vertical", command=canvas.yview)
        scrollable = ttk.Frame(canvas)
        
        scrollable.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollable, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Título
        tk.Label(scrollable, text="MÉTODO DE MARCATILI", 
                font=('Segoe UI', 14, 'bold'), bg='#f0f0f0', fg='#2c3e50').pack(pady=(0, 15))
        
        # Parâmetros geométricos
        self._create_geometry_frame(scrollable)
        
        # Parâmetros ópticos
        self._create_optical_frame(scrollable)
        
        # Parâmetros do modo
        self._create_mode_frame(scrollable)
        
        # Configurações da malha
        self._create_mesh_frame(scrollable)
        
        # Botões
        self._create_buttons_frame(scrollable)
        
        # Resultados textuais
        self._create_results_frame(scrollable)
        
        return panel
    
    def _create_geometry_frame(self, parent):
        """Cria frame de parâmetros geométricos"""
        frame = ttk.LabelFrame(parent, text="Parâmetros Geométricos", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Largura do núcleo (2a):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=self.width_var, width=15).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(frame, text="μm").grid(row=0, column=2, sticky=tk.W)
        
        ttk.Label(frame, text="Altura do núcleo (2b):").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=self.height_var, width=15).grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(frame, text="μm").grid(row=1, column=2, sticky=tk.W)
    
    def _create_optical_frame(self, parent):
        """Cria frame de parâmetros ópticos"""
        frame = ttk.LabelFrame(parent, text="Parâmetros Ópticos", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Comprimento de onda:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=self.lambda_var, width=15).grid(row=0, column=1, padx=10, pady=5)
        ttk.Label(frame, text="μm").grid(row=0, column=2, sticky=tk.W)
        
        ttk.Label(frame, text="Índice do núcleo (n₁):").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=self.n1_var, width=15).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="Índice do revestimento (n₂):").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=self.n2_var, width=15).grid(row=2, column=1, padx=10, pady=5)
    
    def _create_mode_frame(self, parent):
        """Cria frame de parâmetros do modo"""
        frame = ttk.LabelFrame(parent, text="Parâmetros do Modo", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Número do modo em x (p):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=self.mode_x_var, width=15).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="Número do modo em y (q):").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=self.mode_y_var, width=15).grid(row=1, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="Polarização:").grid(row=2, column=0, sticky=tk.W, pady=5)
        pol_frame = ttk.Frame(frame)
        pol_frame.grid(row=2, column=1, columnspan=2, sticky=tk.W)
        ttk.Radiobutton(pol_frame, text="TE (E_x)", variable=self.polarization_var, value=1).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(pol_frame, text="TM (E_y)", variable=self.polarization_var, value=2).pack(side=tk.LEFT, padx=5)
    
    def _create_mesh_frame(self, parent):
        """Cria frame de configurações da malha"""
        frame = ttk.LabelFrame(parent, text="Configurações da Malha", padding=10)
        frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text="Resolução (pontos/eixo):").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=self.resolution_var, width=15).grid(row=0, column=1, padx=10, pady=5)
        
        ttk.Label(frame, text="Extensão da janela (fator):").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(frame, textvariable=self.extension_var, width=15).grid(row=1, column=1, padx=10, pady=5)
        ttk.Label(frame, text="(1.2-4.0)").grid(row=1, column=2, sticky=tk.W)
    
    def _create_buttons_frame(self, parent):
        """Cria frame com botões"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=15)
        
        self.calc_btn = ttk.Button(frame, text="CALCULAR", command=self._on_calculate)
        self.calc_btn.pack(fill=tk.X, pady=5)
        
        self.save_btn = ttk.Button(frame, text="SALVAR GRÁFICOS", command=self._on_save, state='disabled')
        self.save_btn.pack(fill=tk.X, pady=5)
        
        self.export_btn = ttk.Button(frame, text="EXPORTAR DADOS", command=self._on_export, state='disabled')
        self.export_btn.pack(fill=tk.X, pady=5)

        self.export_btn = ttk.Button(frame, text="LIMPAR TUDO", command=exit)
        self.export_btn.pack(fill=tk.X, pady=5)
    
    def _create_results_frame(self, parent):
        """Cria frame para exibição de resultados"""
        frame = ttk.LabelFrame(parent, text="Resultados", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.result_text = tk.Text(frame, height=20, width=45, font=('Consolas', 9), wrap=tk.WORD)
        scroll = ttk.Scrollbar(frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scroll.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _create_right_panel(self, parent):
        """Cria o painel direito com gráficos"""
        panel = ttk.Frame(parent)
        
        # Figura com subplots
        self.figure = Figure(figsize=(10, 8), dpi=100, facecolor='white')
        self.figure.subplots_adjust(left=0.08, right=0.92, top=0.92, bottom=0.08, 
                                    hspace=0.35, wspace=0.35)
        
        self.ax1 = self.figure.add_subplot(2, 2, 1)
        self.ax2 = self.figure.add_subplot(2, 2, 2)
        self.ax3 = self.figure.add_subplot(2, 2, 3)
        self.ax4 = self.figure.add_subplot(2, 2, 4, projection='3d')
        
        # Canvas
        self.canvas = FigureCanvasTkAgg(self.figure, master=panel)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Toolbar
        toolbar_frame = ttk.Frame(panel)
        toolbar_frame.pack(fill=tk.X)
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
        
        return panel
    
    def _validate_inputs(self) -> bool:
        """Valida as entradas do usuário"""
        try:
            width = float(self.width_var.get())
            if width <= 0:
                raise ValueError("Largura deve ser positiva")
            
            height = float(self.height_var.get())
            if height <= 0:
                raise ValueError("Altura deve ser positiva")
            
            wavelength = float(self.lambda_var.get())
            if wavelength <= 0:
                raise ValueError("Comprimento de onda deve ser positivo")
            
            n1 = float(self.n1_var.get())
            if n1 <= 0:
                raise ValueError("Índice do núcleo deve ser positivo")
            
            n2 = float(self.n2_var.get())
            if n2 <= 0:
                raise ValueError("Índice do revestimento deve ser positivo")
            if n2 >= n1:
                raise ValueError("n₂ deve ser menor que n₁")
            
            mode_x = int(self.mode_x_var.get())
            if mode_x < 0:
                raise ValueError("Número do modo deve ser ≥ 0")
            
            mode_y = int(self.mode_y_var.get())
            if mode_y < 0:
                raise ValueError("Número do modo deve ser ≥ 0")
            
            resolution = int(self.resolution_var.get())
            if resolution < 50:
                self.resolution_var.set("50")
                resolution = 50
            
            extension = float(self.extension_var.get())
            if extension < 1.2:
                self.extension_var.set("1.2")
                extension = 1.2
            if extension > 4.0:
                self.extension_var.set("4.0")
                extension = 4.0
            
            return True
            
        except ValueError as e:
            messagebox.showerror("Erro de Entrada", str(e))
            return False 
            
    def _on_calculate(self):
        """Callback do botão calcular"""
        if not self._validate_inputs():
            return
        
        try:
            # Atualiza parâmetros no controller
            self.controller.set_parameters(
                width_um=float(self.width_var.get()),
                height_um=float(self.height_var.get()),
                wavelength_um=float(self.lambda_var.get()),
                n_core=float(self.n1_var.get()),
                n_cladding=float(self.n2_var.get()),
                mode_x=int(self.mode_x_var.get()),
                mode_y=int(self.mode_y_var.get()),
                polarization=self.polarization_var.get(),
                resolution=int(self.resolution_var.get()),
                extension=float(self.extension_var.get())
            )
            
            # Executa cálculo
            self.controller.calculate()
            
            # Atualiza texto de resultados
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, self.controller.get_summary())
            
            # Habilita botões
            self.save_btn.config(state='normal')
            self.export_btn.config(state='normal')
            self._calculation_done = True
            
        except Exception as e:
            messagebox.showerror("Erro no Cálculo", str(e))
    
    def on_data_updated(self):
        """Callback chamado quando os dados são atualizados"""
        self._update_plots()
    
    def _update_plots(self):
        """Atualiza os gráficos"""
        results = self.controller.results
        if results is None or results.field is None:
            return
        
        params = self.controller.params
        if params is None:
            return
        
        x_um = results.x_grid * 1e6
        y_um = results.y_grid * 1e6
        field = results.field
        a_um = params.half_width * 1e6
        b_um = params.half_height * 1e6
        tipo_campo = 'E_x' if params.polarization.value == 1 else 'E_y'
        
        # Limpar axes
        self.ax1.clear()
        self.ax2.clear()
        self.ax3.clear()
        self.ax4.clear()
        
        # Gráfico 1: Distribuição 2D
        im = self.ax1.imshow(field.T, origin='lower', 
                            extent=[x_um[0], x_um[-1], y_um[0], y_um[-1]],
                            cmap='jet', aspect='auto')
        self.ax1.set_xlabel('x (μm)')
        self.ax1.set_ylabel('y (μm)')
        self.ax1.set_title(f'Distribuição de {tipo_campo}')
        
        # Contorno do núcleo
        rect = plt.Rectangle((-a_um, -b_um), 2*a_um, 2*b_um, 
                            fill=False, edgecolor='white', linewidth=2, linestyle='--')
        self.ax1.add_patch(rect)
        self.figure.colorbar(im, ax=self.ax1, label='Campo (u.a.)')
        
        # Gráfico 2: Corte em y=0
        idx_y0 = np.argmin(np.abs(results.y_grid))
        self.ax2.plot(x_um, field[:, idx_y0], 'b-', linewidth=2)
        self.ax2.grid(True, alpha=0.3)
        self.ax2.set_xlabel('x (μm)')
        self.ax2.set_ylabel(f'{tipo_campo} (u.a.)')
        self.ax2.set_title('Corte em y = 0')
        self.ax2.axvline(x=-a_um, color='r', linestyle='--', alpha=0.7)
        self.ax2.axvline(x=a_um, color='r', linestyle='--', alpha=0.7)
        self.ax2.set_ylim(-1.1, 1.1)
        
        # Gráfico 3: Corte em x=0
        idx_x0 = np.argmin(np.abs(results.x_grid))
        self.ax3.plot(y_um, field[idx_x0, :], 'r-', linewidth=2)
        self.ax3.grid(True, alpha=0.3)
        self.ax3.set_xlabel('y (μm)')
        self.ax3.set_ylabel(f'{tipo_campo} (u.a.)')
        self.ax3.set_title('Corte em x = 0')
        self.ax3.axvline(x=-b_um, color='b', linestyle='--', alpha=0.7)
        self.ax3.axvline(x=b_um, color='b', linestyle='--', alpha=0.7)
        self.ax3.set_ylim(-1.1, 1.1)
        
        # Gráfico 4: Visualização 3D
        X_um, Y_um = np.meshgrid(x_um, y_um)
        self.ax4.plot_surface(X_um, Y_um, field.T, cmap='jet', edgecolor='none', alpha=0.9)
        self.ax4.set_xlabel('x (μm)')
        self.ax4.set_ylabel('y (μm)')
        self.ax4.set_zlabel('Campo (u.a.)')
        self.ax4.set_title('Visualização 3D')
        self.ax4.view_init(elev=30, azim=45)
        
        # Título geral
        tipo = "TE" if params.polarization.value == 1 else "TM"
        self.figure.suptitle(f'Método de Marcatili - Modo {tipo}_{{{params.mode_x}{params.mode_y}}}', 
                            fontsize=14, fontweight='bold')
        
        self.canvas.draw()
    
    def _on_save(self):
        """Salva os gráficos em arquivos"""
        if not self._calculation_done:
            messagebox.showwarning("Aviso", "Nenhum dado para salvar. Execute o cálculo primeiro.")
            return
        
        params = self.controller.params
        if params is None:
            return
        
        directory = filedialog.askdirectory(title="Selecione o diretório para salvar")
        if not directory:
            return
        
        try:
            base_name = f"Marcatili_TE{params.mode_x}{params.mode_y}_lambda{params.wavelength*1e6:.2f}"
            
            # Salvar figura principal
            fig_path = os.path.join(directory, f"{base_name}_campos.png")
            self.figure.savefig(fig_path, dpi=300, bbox_inches='tight')
            
            # Criar figura de intensidade
            self._save_intensity_figure(directory, base_name)
            
            messagebox.showinfo("Sucesso", f"Gráficos salvos em:\n{directory}")
            
        except Exception as e:
            messagebox.showerror("Erro ao Salvar", str(e))
    
    def _save_intensity_figure(self, directory: str, base_name: str):
        """Salva figura de intensidade"""
        results = self.controller.results
        params = self.controller.params
        
        if results is None or params is None:
            return
        
        fig_int = Figure(figsize=(12, 10), dpi=100, facecolor='white')
        
        ax1 = fig_int.add_subplot(2, 2, 1)
        ax2 = fig_int.add_subplot(2, 2, 2)
        ax3 = fig_int.add_subplot(2, 2, 3)
        ax4 = fig_int.add_subplot(2, 2, 4)
        
        x_um = results.x_grid * 1e6
        y_um = results.y_grid * 1e6
        a_um = params.half_width * 1e6
        b_um = params.half_height * 1e6
        
        # Intensidade 2D
        im = ax1.imshow(results.intensity.T, origin='lower',
                       extent=[x_um[0], x_um[-1], y_um[0], y_um[-1]],
                       cmap='hot', aspect='auto')
        ax1.set_xlabel('x (μm)')
        ax1.set_ylabel('y (μm)')
        ax1.set_title('Distribuição de Intensidade')
        rect = plt.Rectangle((-a_um, -b_um), 2*a_um, 2*b_um, 
                            fill=False, edgecolor='cyan', linewidth=2, linestyle='--')
        ax1.add_patch(rect)
        fig_int.colorbar(im, ax=ax1, label='Intensidade (u.a.)')
        
        # Cortes de intensidade
        idx_y0 = np.argmin(np.abs(results.y_grid))
        ax2.plot(x_um, results.intensity[:, idx_y0], 'b-', linewidth=2)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlabel('x (μm)')
        ax2.set_ylabel('Intensidade (u.a.)')
        ax2.set_title('Intensidade - Corte em y = 0')
        ax2.axvline(x=-a_um, color='r', linestyle='--')
        ax2.axvline(x=a_um, color='r', linestyle='--')
        
        idx_x0 = np.argmin(np.abs(results.x_grid))
        ax3.plot(y_um, results.intensity[idx_x0, :], 'r-', linewidth=2)
        ax3.grid(True, alpha=0.3)
        ax3.set_xlabel('y (μm)')
        ax3.set_ylabel('Intensidade (u.a.)')
        ax3.set_title('Intensidade - Corte em x = 0')
        ax3.axvline(x=-b_um, color='b', linestyle='--')
        ax3.axvline(x=b_um, color='b', linestyle='--')
        
        # Curvas de nível
        ax4.contour(x_um, y_um, results.intensity.T, 20, cmap='viridis')
        ax4.set_xlabel('x (μm)')
        ax4.set_ylabel('y (μm)')
        ax4.set_title('Curvas de Nível da Intensidade')
        ax4.set_aspect('equal')
        rect = plt.Rectangle((-a_um, -b_um), 2*a_um, 2*b_um, 
                            fill=False, edgecolor='red', linewidth=2, linestyle='--')
        ax4.add_patch(rect)
        
        fig_int.suptitle(f'Perfil de Intensidade - λ = {params.wavelength*1e6:.2f} μm', 
                        fontsize=14, fontweight='bold')
        
        fig_int.savefig(os.path.join(directory, f"{base_name}_intensidade.png"), 
                       dpi=300, bbox_inches='tight')
        plt.close(fig_int)
    
    def _on_export(self):
        """Exporta dados numéricos para arquivo"""
        if not self._calculation_done:
            messagebox.showwarning("Aviso", "Nenhum dado para exportar. Execute o cálculo primeiro.")
            return
        
        results = self.controller.results
        params = self.controller.params
        
        if results is None or params is None:
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".npz",
            filetypes=[("NumPy compressed", "*.npz"), ("All files", "*.*")],
            title="Salvar dados numéricos"
        )
        
        if not file_path:
            return
        
        try:
            # Salvar dados em formato comprimido
            np.savez_compressed(file_path,
                               x_grid=results.x_grid,
                               y_grid=results.y_grid,
                               field=results.field,
                               intensity=results.intensity,
                               k0=results.k0,
                               kx=results.kx,
                               ky=results.ky,
                               beta=results.beta,
                               n_eff=results.n_eff,
                               gamma_x=results.gamma_x,
                               gamma_y=results.gamma_y,
                               V=results.V,
                               half_width=params.half_width,
                               half_height=params.half_height,
                               wavelength=params.wavelength,
                               n_core=params.n_core,
                               n_cladding=params.n_cladding,
                               mode_x=params.mode_x,
                               mode_y=params.mode_y,
                               polarization=params.polarization.value)
            
            messagebox.showinfo("Sucesso", f"Dados exportados para:\n{file_path}")
            
        except Exception as e:
            messagebox.showerror("Erro ao Exportar", str(e))
    
    def run(self):
        """Inicia a aplicação"""
        self.root.mainloop()
