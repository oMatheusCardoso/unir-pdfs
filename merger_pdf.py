import PyPDF2
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

lista_arquivos = []

def atualizar_lista():
    global lista_arquivos
    pasta = pasta_selecionada.cget("text").replace("Pasta selecionada: ", "").replace('...', '')
    if not pasta:
        return

    if opcoes_ordem.get() == "Nome":
        lista_arquivos = sorted([f for f in os.listdir(pasta) if f.endswith(".pdf")])
    else:  # Ordenação por data de modificação
        lista_arquivos = sorted(
            [f for f in os.listdir(pasta) if f.endswith(".pdf")],
            key=lambda x: os.path.getmtime(os.path.join(pasta, x))
        )

    # Atualiza a Listbox com a nova ordem
    lista_arquivos_pdf.delete(0, tk.END)  # Limpa a Listbox anterior
    for arquivo in lista_arquivos:
        lista_arquivos_pdf.insert(tk.END, arquivo)
def selecionar_pasta():
    pasta = filedialog.askdirectory(title="Selecione a pasta com os arquivos de .pdf para união.")
    if pasta:
        lista_pdfs = [f for f in os.listdir(pasta) if f.endswith(".pdf")]
        if lista_pdfs:
            pasta_selecionada.config(text=f"Pasta selecionada: {pasta}")
            botao_unir.config(state=tk.NORMAL)
            atualizar_lista()
        else:
            messagebox. showwarning(
                'Aviso',
                'A pasta selecionada não contém arquivos de PDFs.\nColoque os arquivos que deseja juntar em uma pasta e selecione a pasta.'
            )

def unir_pdfs():
    global lista_arquivos
    pasta = pasta_selecionada.cget("text").replace("Pasta selecionada: ", "")
    if not pasta:
        messagebox.showerror("Erro", "Nenhuma pasta selecionada.")
        return

    nome_arquivo_saida = entrada_nome_arquivo.get().strip()
    if not nome_arquivo_saida:
        messagebox.showerror("Erro", "Nome do arquivo de saída não pode ser vazio.")
        return

    if not nome_arquivo_saida.endswith(".pdf"):
        nome_arquivo_saida += ".pdf"

    if not lista_arquivos:
        messagebox.showerror("Erro", "Nenhum arquivo PDF encontrado na pasta selecionada.")
        return
    
    merger = PyPDF2.PdfMerger()
    barra_progresso['maximum'] = len(lista_arquivos)
    for i, arquivo in enumerate(lista_arquivos, start=1):
            caminho_arquivo = os.path.join(pasta, arquivo)
            merger.append(caminho_arquivo)
            barra_progresso['value'] = i
            janela.update_idletasks()

    caminho_saida = os.path.join(pasta, nome_arquivo_saida)
    with open(caminho_saida, "wb") as f_out:
        merger.write(f_out)
    
    merger.close()
    messagebox.showinfo("Sucesso", f"PDFs unidos com sucesso em: {caminho_saida}")

# Configuração da janela Tkinter
janela = tk.Tk()
janela.title("Unir PDFs")
janela.geometry("600x700")


texto_orientacao = tk.Label(janela, text="Selecione a pasta com os arquivos .pdf para união.")
texto_orientacao.grid(column=0, row=0, padx=10, pady=10, sticky='ew')


botao_selecionar = tk.Button(janela, text="Selecionar Pasta", command=selecionar_pasta)
botao_selecionar.grid(column=0, row=1, padx=10, pady=10)

pasta_selecionada = tk.Label(janela, text="")
pasta_selecionada.grid(column=0, row=2, padx=10, pady=10, sticky='ew')

texto_ordem = tk.Label(janela, text="Selecione a ordem de união dos PDFs")
texto_ordem.grid(column=0, row=3, padx=10, pady=10, sticky='ew')

opcoes_ordem = tk.StringVar(value="Nome")
menu_ordem = tk.OptionMenu(janela, opcoes_ordem, 'Nome', 'Data de Modificação', command=lambda _: atualizar_lista())
menu_ordem.grid(column=0, row=4, padx=10, pady=10)

texto_nome_arquivo = tk.Label(janela, text="Digite o nome do arquivo final:")
texto_nome_arquivo.grid(column=0, row=5, padx=10, pady=10, sticky='ew')

entrada_nome_arquivo = tk.Entry(janela, width=50)
entrada_nome_arquivo.grid(column=0, row=6, padx=10, pady=10)

botao_unir = tk.Button(janela, text="Unir PDFs", command=unir_pdfs)
botao_unir.grid(column=0, row=7, padx=10, pady=10)

lista_arquivos_pdf = tk.Listbox(janela, height=10, selectmode=tk.SINGLE)
lista_arquivos_pdf.grid(column=0, row=8, padx=10, pady=5, sticky='ew')

barra_progresso = ttk.Progressbar(janela, orient='horizontal', length=400, mode='determinate')
barra_progresso.grid(column=0, row=9, padx=10, pady=10, sticky="ew")

janela.columnconfigure(0, weight=1)
janela.mainloop()
