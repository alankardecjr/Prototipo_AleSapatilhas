import tkinter as tk
from tkinter import messagebox
import database

class JanelaCadastroPedidos(tk.Toplevel):
    def __init__(self, master, dados_venda):
        super().__init__(master)
        self.title("Alê Sapatilhas - Painel de Pedidos")
        self.geometry("450x550")
        self.configure(bg="#f4f5f9")
        
        self.venda_id = dados_venda[0]
        self.criar_widgets(dados_venda)
        self.grab_set()

    def criar_widgets(self, d):
        main_frame = tk.Frame(self, bg="#f4f5f9", padx=25, pady=20)
        main_frame.pack(fill="both", expand=True)

        # Info Cliente
        tk.Label(main_frame, text=f"PEDIDO: #{self.venda_id}", bg="#f4f5f9", font=("Segoe UI", 14, "bold")).pack(anchor="w")
        tk.Label(main_frame, text=f"Cliente: {d[1]}", bg="#f4f5f9", font=("Segoe UI", 11)).pack(anchor="w")
        tk.Label(main_frame, text=f"Valor Total: R$ {d[2]:.2f}", bg="#f4f5f9", fg="#3b82f6", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=10)

        # --- MENUS DE STATUS ---
        # 1. Status Financeiro
        tk.Label(main_frame, text="STATUS DA VENDA (PAGAMENTO)", bg="#f4f5f9", font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(10,0))
        self.var_venda = tk.StringVar(value=d[3])
        opt_venda = tk.OptionMenu(main_frame, self.var_venda, "Pendente", "Confirmada", "Cancelada")
        self.estilizar_opt(opt_venda)
        opt_venda.pack(fill="x", pady=5)

        # 2. Status Entrega
        tk.Label(main_frame, text="STATUS DO PEDIDO (LOGÍSTICA)", bg="#f4f5f9", font=("Segoe UI", 8, "bold")).pack(anchor="w", pady=(10,0))
        self.var_entrega = tk.StringVar(value=d[4])
        opt_entrega = tk.OptionMenu(main_frame, self.var_entrega, "À Entregar", "Em Trânsito", "Entregue")
        self.estilizar_opt(opt_entrega)
        opt_entrega.pack(fill="x", pady=5)

        # Botões
        tk.Button(main_frame, text="ATUALIZAR", bg="#4b5563", fg="white", font=("Segoe UI", 10, "bold"),
                  relief="flat", command=self.atualizar).pack(fill="x", pady=(30, 5), ipady=8)
        
        tk.Button(main_frame, text="FECHAR", bg="#1f2937", fg="white", relief="flat", 
                  command=self.destroy).pack(fill="x", ipady=5)

    def estilizar_opt(self, opt):
        opt.config(bg="white", relief="flat", highlightthickness=1, highlightbackground="#d1d5db")

    def atualizar(self):
        database.atualizar_status_venda_financeiro(self.venda_id, self.var_venda.get())
        database.atualizar_status_entrega(self.venda_id, self.var_entrega.get())
        messagebox.showinfo("Sucesso", "Status atualizados com sucesso!")
        self.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    # Exemplo para teste rápido
    JanelaCadastroPedidos(root, (1, "Exemplo Alê", 120.0, "Pendente", "À Entregar", "2023-01-01"))
    root.mainloop()