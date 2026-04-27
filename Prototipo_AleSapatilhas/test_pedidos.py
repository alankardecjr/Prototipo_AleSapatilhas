import tkinter as tk
from tkinter import messagebox
import database

class JanelaCadastroPedidos(tk.Toplevel):
    def __init__(self, master, dados_venda):
        """
        dados_venda deve conter: (id, nome_cliente, valor_total, status_venda, status_entrega, data)
        """
        super().__init__(master)
        self.title(f"Alê Sapatilhas - Detalhes da Venda #{dados_venda[0]}")
        self.geometry("480x650")
        self.resizable(False, False)
        
        # Paleta de Cores Padrão
        self.bg_fundo = "#f4f5f9"
        self.bg_card = "#ffffff"
        self.cor_borda = "#d1d5db"
        self.cor_texto = "#1f2937"
        self.cor_lbl = "#4b5563"
        self.cor_destaque = "#3b82f6" # Azul para informações importantes
        self.cor_btn_sair = "#1f2937"

        self.configure(bg=self.bg_fundo)
        self.venda_id = dados_venda[0]
        self.dados_venda = dados_venda

        self.criar_widgets()
        self.grab_set()

    def criar_widgets(self):
        main_frame = tk.Frame(self, bg=self.bg_fundo, padx=25, pady=20)
        main_frame.pack(fill="both", expand=True)

        # --- CABEÇALHO ---
        header_frame = tk.Frame(main_frame, bg=self.bg_fundo)
        header_frame.pack(fill="x", pady=(0, 15))

        tk.Label(header_frame, text=f"VENDA #{self.venda_id}", bg=self.bg_fundo, 
                 fg=self.cor_texto, font=("Segoe UI", 16, "bold")).pack(side="left")
        
        tk.Label(header_frame, text=self.dados_venda[5], bg=self.bg_fundo, 
                 fg=self.cor_lbl, font=("Segoe UI", 9)).pack(side="right", pady=5)

        # --- CARD DO CLIENTE ---
        cliente_frame = tk.LabelFrame(main_frame, text=" Dados da Cliente ", bg=self.bg_card, 
                                      fg=self.cor_lbl, font=("Segoe UI", 9, "bold"), 
                                      padx=15, pady=10, relief="flat", highlightbackground=self.cor_borda, highlightthickness=1)
        cliente_frame.pack(fill="x", pady=5)

        tk.Label(cliente_frame, text="NOME:", bg=self.bg_card, fg=self.cor_lbl, font=("Segoe UI", 8)).grid(row=0, column=0, sticky="w")
        tk.Label(cliente_frame, text=self.dados_venda[1], bg=self.bg_card, fg=self.cor_texto, font=("Segoe UI", 11, "bold")).grid(row=1, column=0, sticky="w")

        # --- RESUMO FINANCEIRO ---
        financeiro_frame = tk.Frame(main_frame, bg=self.bg_fundo)
        financeiro_frame.pack(fill="x", pady=15)

        tk.Label(financeiro_frame, text="VALOR TOTAL DA VENDA", bg=self.bg_fundo, fg=self.cor_lbl, font=("Segoe UI", 8, "bold")).pack()
        tk.Label(financeiro_frame, text=f"R$ {self.dados_venda[2]:.2f}", bg=self.bg_fundo, fg=self.cor_destaque, font=("Segoe UI", 22, "bold")).pack()

        # --- SEÇÃO DE STATUS (GESTÃO) ---
        status_frame = tk.Frame(main_frame, bg=self.bg_fundo)
        status_frame.pack(fill="x", pady=10)

        # Status da Venda (Financeiro)
        tk.Label(status_frame, text="STATUS FINANCEIRO", bg=self.bg_fundo, fg=self.cor_lbl, font=("Segoe UI", 8, "bold")).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.var_venda = tk.StringVar(value=self.dados_venda[3])
        self.opt_venda = tk.OptionMenu(status_frame, self.var_venda, "Pendente", "Confirmada", "Cancelada")
        self.estilizar_option(self.opt_venda)
        self.opt_venda.grid(row=1, column=0, sticky="ew", padx=(0, 5))

        # Status do Pedido (Entrega)
        tk.Label(status_frame, text="STATUS DA ENTREGA", bg=self.bg_fundo, fg=self.cor_lbl, font=("Segoe UI", 8, "bold")).grid(row=0, column=1, sticky="w", pady=(0, 5))
        self.var_entrega = tk.StringVar(value=self.dados_venda[4])
        self.opt_entrega = tk.OptionMenu(status_frame, self.var_entrega, "À Entregar", "Em Trânsito", "Entregue")
        self.estilizar_option(self.opt_entrega)
        self.opt_entrega.grid(row=1, column=1, sticky="ew", padx=(5, 0))

        status_frame.columnconfigure(0, weight=1)
        status_frame.columnconfigure(1, weight=1)

        # --- BOTÕES DE AÇÃO ---
        btn_frame = tk.Frame(main_frame, bg=self.bg_fundo)
        btn_frame.pack(fill="x", pady=(30, 0))

        self.btn_salvar = tk.Button(btn_frame, text="ATUALIZAR STATUS", bg=self.cor_lbl, fg="white", 
                                    font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", 
                                    command=self.salvar_status)
        self.btn_salvar.pack(fill="x", ipady=10, pady=5)
        
        self.btn_sair = tk.Button(btn_frame, text="FECHAR", bg=self.cor_btn_sair, fg="white", 
                                 font=("Segoe UI", 10, "bold"), relief="flat", cursor="hand2", 
                                 command=self.destroy)
        self.btn_sair.pack(fill="x", ipady=8, pady=5)

    def estilizar_option(self, menu):
        menu.config(bg=self.bg_card, fg=self.cor_texto, relief="flat", highlightthickness=1, 
                    highlightbackground=self.cor_borda, font=("Segoe UI", 10), cursor="hand2")

    def salvar_status(self):
        try:
            # Chama as funções que criamos no database.py
            database.atualizar_status_venda_financeiro(self.venda_id, self.var_venda.get())
            database.atualizar_status_entrega(self.venda_id, self.var_entrega.get())
            
            messagebox.showinfo("Sucesso", f"Status da Venda #{self.venda_id} atualizados!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    # Exemplo de dados para teste: (id, nome, valor, status_v, status_e, data)
    exemplo = (1, "Maria Silva", 159.90, "Pendente", "À Entregar", "2023-10-27 14:30")
    JanelaCadastroPedidos(root, exemplo)
    root.mainloop()