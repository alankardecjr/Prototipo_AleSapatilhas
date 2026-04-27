import tkinter as tk
from tkinter import messagebox
import database 

class JanelaCadastroProdutos(tk.Toplevel):
    def __init__(self, master, dados_produto=None):
        super().__init__(master)
        self.title("Alê Sapatilhas - Painel de Produtos")
        self.geometry("450x650") 
        self.resizable(False, False)
        
        # Paleta de Cores (Padrão Alê Sapatilhas)
        self.bg_fundo = "#f4f5f9"
        self.bg_card = "#ffffff"
        self.cor_borda = "#d1d5db"
        self.cor_texto = "#1f2937"
        self.cor_lbl = "#4b5563"
        self.cor_btn_1 = "#4b5563"   
        self.cor_btn_sair = "#1f2937" 
        self.cor_hover_field = "#3b82f6"   
        self.cor_hover_btn = "#6b7280" 

        self.configure(bg=self.bg_fundo)
        self.produto_id = None

        self.criar_widgets()
        
        if dados_produto:
            self.preencher_dados(dados_produto)            
     
        self.grab_set()

    def criar_widgets(self):
        main_frame = tk.Frame(self, bg=self.bg_fundo, padx=20, pady=10)
        main_frame.pack(fill="both", expand=True)

        def ao_entrar_botao(e, cor_destaque):
            e.widget.config(bg=cor_destaque)

        def ao_sair_botao(e, cor_original):
            e.widget.config(bg=cor_original)

        def criar_campo(parent, texto, row, col=0, colspan=2, width=None):
            tk.Label(parent, text=texto, bg=self.bg_fundo, fg=self.cor_lbl, 
                     font=("Segoe UI", 8, "bold")).grid(row=row, column=col, sticky="w", pady=(6, 0))
            
            ent = tk.Entry(parent, font=("Segoe UI", 10), bg=self.bg_card, fg=self.cor_texto,
                            relief="flat", highlightbackground=self.cor_borda, highlightthickness=1)
            
            if width: ent.config(width=width)
            ent.grid(row=row+1, column=col, columnspan=colspan, sticky="ew", ipady=3, padx=(0, 5) if colspan==1 else 0)
            
            # --- EFEITO HOVER E FOCUS ---
            ent.bind("<Enter>", lambda e: e.widget.config(highlightbackground="#9ca3af") if e.widget != self.focus_get() else None)
            ent.bind("<Leave>", lambda e: e.widget.config(highlightbackground=self.cor_borda) if e.widget != self.focus_get() else None)
            ent.bind("<FocusIn>", lambda e: e.widget.config(highlightbackground=self.cor_hover_field, highlightthickness=2))
            ent.bind("<FocusOut>", lambda e: e.widget.config(highlightbackground=self.cor_borda, highlightthickness=1))
            
            return ent

        # --- HEADER ---
        lbl_header = tk.Label(main_frame, text="Gerenciar Produto", bg=self.bg_fundo, 
                               fg=self.cor_texto, font=("Segoe UI", 14, "bold"))
        lbl_header.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

        # --- CAMPOS ---
        self.ent_produto = criar_campo(main_frame, "MODELO / DESCRIÇÃO*", 1)
        
        # Linha: Cor e Tamanho
        self.ent_cor = criar_campo(main_frame, "COR*", 3, col=0, colspan=1)
        self.ent_tam = criar_campo(main_frame, "TAMANHO*", 3, col=1, colspan=1)
        
        # Linha: Preços
        self.ent_custo = criar_campo(main_frame, "PREÇO CUSTO (R$)", 5, col=0, colspan=1)
        self.ent_venda = criar_campo(main_frame, "PREÇO VENDA* (R$)", 5, col=1, colspan=1)
        
        # Linha: Estoque e Categoria
        self.ent_qtd = criar_campo(main_frame, "QUANTIDADE*", 7, col=0, colspan=1)
        self.ent_cat = criar_campo(main_frame, "CATEGORIA", 7, col=1, colspan=1)
        
        self.ent_fornecedor = criar_campo(main_frame, "FORNECEDOR", 9)

        # --- STATUS ---
        tk.Label(main_frame, text="DISPONIBILIDADE", bg=self.bg_fundo, fg=self.cor_lbl, 
                 font=("Segoe UI", 8, "bold")).grid(row=11, column=0, sticky="w", pady=(8, 0))
        
        self.var_status = tk.StringVar(value="Disponível")
        self.opt_status = tk.OptionMenu(main_frame, self.var_status, "Disponível", "Indisponível", "Esgotado", "Promoção")
        self.opt_status.config(bg=self.bg_card, fg=self.cor_texto, relief="flat", highlightthickness=1, 
                                highlightbackground=self.cor_borda, font=("Segoe UI", 9), cursor="hand2")
        self.opt_status.grid(row=12, column=0, columnspan=2, sticky="ew", pady=(2, 0))

        # --- BOTÕES ---
        btn_frame = tk.Frame(main_frame, bg=self.bg_fundo)
        btn_frame.grid(row=13, column=0, columnspan=2, pady=(30, 5))

        self.btn_salvar = tk.Button(btn_frame, text="SALVAR", bg=self.cor_btn_1, fg="white", 
                                    font=("Segoe UI", 9, "bold"), width=30, relief="flat", cursor="hand2", 
                                    command=self.validar_e_salvar)
        self.btn_salvar.pack(pady=5, ipady=8)
        self.btn_salvar.bind("<Enter>", lambda e: ao_entrar_botao(e, self.cor_hover_btn))
        self.btn_salvar.bind("<Leave>", lambda e: ao_sair_botao(e, self.cor_btn_1))

        self.btn_sair = tk.Button(main_frame, text="SAIR", bg=self.cor_btn_sair, fg="white", 
                                        font=("Segoe UI", 9, "bold"), width=30, relief="flat", cursor="hand2", 
                                        command=self.fechar)
        self.btn_sair.grid(row=14, column=0, columnspan=2, pady=(10, 0), ipady=8)
        self.btn_sair.bind("<Enter>", lambda e: ao_entrar_botao(e, "#374151"))
        self.btn_sair.bind("<Leave>", lambda e: ao_sair_botao(e, self.cor_btn_sair))

        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def fechar(self):
        self.grab_release()
        self.destroy()

    def coletar_dados(self):
        return {
            "produto": self.ent_produto.get().strip(),
            "cor": self.ent_cor.get().strip(),
            "tam": self.ent_tam.get().strip(),
            "custo": self.ent_custo.get().replace(",", "."),
            "venda": self.ent_venda.get().replace(",", "."),
            "qtd": self.ent_qtd.get().strip(),
            "cat": self.ent_cat.get().strip(),
            "forn": self.ent_fornecedor.get().strip(),
            "status": self.var_status.get()
        }

    def validar_e_salvar(self):
        d = self.coletar_dados()
        
        if not d["produto"] or not d["cor"] or not d["venda"] or not d["tam"] or not d["qtd"]:
            messagebox.showwarning("Atenção", "Todos os campos obrigatórios devem ser preenchidos.")
            return

        try:
            if self.produto_id:
                # Lógica de atualização
                database.atualizar_status_item(self.produto_id, d["status"])
                messagebox.showinfo("Sucesso", "Status atualizado!")
            else:
                # Novo cadastro
                database.salvar_item(
                    d["produto"], d["cor"], d["tam"], d["custo"], 
                    d["venda"], d["qtd"], d["cat"], d["forn"], d["status"]
                )
                messagebox.showinfo("Sucesso", "Produto cadastrado!")
            self.fechar()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar: {e}")

    def preencher_dados(self, d):
        self.produto_id = d[0]
        self.ent_produto.insert(0, d[1])
        self.ent_cor.insert(0, d[2])
        self.ent_tam.insert(0, d[3])
        self.ent_custo.insert(0, d[4])
        self.ent_venda.insert(0, d[5])
        self.ent_qtd.insert(0, d[6])
        self.ent_cat.insert(0, d[7])
        self.ent_fornecedor.insert(0, d[8])
        self.var_status.set(d[9])
        self.btn_salvar.config(text="ATUALIZAR")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() 
    JanelaCadastroProdutos(root)
    root.mainloop()