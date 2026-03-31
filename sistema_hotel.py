from tkinter import *
from tkinter import ttk
import sqlite3

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser


root = Tk()
root.iconbitmap("icone.ico")

class Relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")
    def geraRelatCliente(self):
        self.c = canvas.Canvas("cliente.pdf")

        self.codigoRel = self.codigo_entry.get()
        self.CPFRel = self.CPF_entry.get()
        self.nomeRel = self.nome_entry.get()
        self.data_nascimentoRel = self.data_nascimento_entry.get()
        self.sexoRel = self.sexo_entry.get()
        self.telefoneRel = self.telefone_entry.get()
        self.cepRel = self.cep_entry.get()
        self.ruaRel = self.rua_entry.get()
        self.numeroRel = self.numero_entry.get()
        self.complementoRel = self.complemento_entry.get()
        self.bairroRel = self.bairro_entry.get()
        self.cidadeRel = self.cidade_entry.get()
        self.estadoRel = self.estado_entry.get()
        self.observacoesRel = self.observacoes_entry.get()

        self.c.setFont("Courier-Bold", 20)
        self.c.drawString(200, 800, 'Ficha do Cliente')

        self.c.setFont("Courier-Bold", 14)
        self.c.drawString(50, 760, 'Código............:')
        self.c.drawString(50, 740, 'CPF...............:')
        self.c.drawString(50, 720, 'Nome..............:')
        self.c.drawString(50, 700, 'Data de Nascimento:')
        self.c.drawString(50, 680, 'Sexo..............:')
        self.c.drawString(50, 660, 'Telefone..........:')
        self.c.drawString(50, 640, 'CEP...............:')
        self.c.drawString(50, 620, 'Rua...............:')
        self.c.drawString(50, 600, 'Número............:')
        self.c.drawString(50, 580, 'Complemento.......:')
        self.c.drawString(50, 560, 'Bairro............:')
        self.c.drawString(50, 540, 'Cidade............:')
        self.c.drawString(50, 520, 'Estado............:')
        self.c.drawString(50, 500, 'Observações.......:')

        self.c.setFont("Courier", 14)
        self.c.drawString(220, 760, self.codigoRel)
        self.c.drawString(220, 740, self.CPFRel)
        self.c.drawString(220, 720, self.nomeRel)
        self.c.drawString(220, 700, self.data_nascimentoRel)
        self.c.drawString(220, 680, self.sexoRel)
        self.c.drawString(220, 660, self.telefoneRel)
        self.c.drawString(220, 640, self.cepRel)
        self.c.drawString(220, 620, self.ruaRel)
        self.c.drawString(220, 600, self.numeroRel)
        self.c.drawString(220, 580, self.complementoRel)
        self.c.drawString(220, 560, self.bairroRel)
        self.c.drawString(220, 540, self.cidadeRel)
        self.c.drawString(220, 520, self.estadoRel)
        self.c.drawString(220, 500, self.observacoesRel)

       # self.c.rect(20, 480, 550, 4, fill=True, stroke=False) -> linha ou borda

        self.c.showPage()
        self.c.save()
        self.printCliente()

class Funcs():
    def limpa_cliente(self):
        self.codigo_entry.delete(0, END)
        self.CPF_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.data_nascimento_entry.delete(0, END)
        self.sexo_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cep_entry.delete(0, END)
        self.rua_entry.delete(0, END)
        self.numero_entry.delete(0, END)
        self.complemento_entry.delete(0, END)
        self.bairro_entry.delete(0, END)
        self.cidade_entry.delete(0, END)
        self.estado_entry.delete(0, END)
        self.observacoes_entry.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.bd")
        self.cursor = self.conn.cursor(); print("Conectando ao banco de dados")
    def desconecta_bd(self):
        self.conn.close(); print("Desconectando ao banco de dados")
    def montaTabelas(self):
        self.conecta_bd()
        ###criar tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY AUTOINCREMENT,
                CPF TEXT UNIQUE NOT NULL,
                nome TEXT NOT NULL,
                data_nascimento TEXT,
                sexo TEXT,
                telefone TEXT,
                cep TEXT,
                rua TEXT,
                numero INTEGER,
                complemento TEXT,
                bairro TEXT,
                cidade TEXT,
                estado TEXT,
                observacoes TEXT
            );           
        """)
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd()
    def variaveis(self):
        self.codigo = self.codigo_entry.get()
        self.CPF = self.CPF_entry.get()
        self.nome = self.nome_entry.get()
        self.data_nascimento = self.data_nascimento_entry.get()
        self.sexo = self.sexo_entry.get()
        self.telefone = self.telefone_entry.get()
        self.cep = self.cep_entry.get()
        self.rua = self.rua_entry.get()
        self.numero = self.numero_entry.get()
        self.complemento = self.complemento_entry.get()
        self.bairro = self.bairro_entry.get()
        self.cidade = self.cidade_entry.get()
        self.estado = self.estado_entry.get()
        self.observacoes = self.observacoes_entry.get()
    def add_cliente(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute(""" INSERT INTO clientes (CPF, nome, data_nascimento, sexo, telefone, cep, rua, numero, complemento, bairro, cidade, estado, observacoes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (self.CPF, self.nome, self.data_nascimento, self.sexo, self.telefone, self.cep, self.rua, self.numero, self.complemento, self.bairro, self.cidade, self.estado, self.observacoes))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_cliente()
    def select_lista(self)    :
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, CPF, nome, data_nascimento, sexo, telefone, cep, rua, numero, complemento, bairro, cidade, estado, observacoes FROM clientes ORDER BY nome ASC; """)
        for i in lista:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()
    def OnDoubleClick(self, event):
        self.limpa_cliente()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14 = self.listaCli.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.CPF_entry.insert(END, col2)
            self.nome_entry.insert(END, col3)
            self.data_nascimento_entry.insert(END, col4)
            self.sexo_entry.insert(END, col5)
            self.telefone_entry.insert(END, col6)
            self.cep_entry.insert(END, col7)
            self.rua_entry.insert(END, col8)
            self.numero_entry.insert(END, col9)
            self.complemento_entry.insert(END, col10)
            self.bairro_entry.insert(END, col11)
            self.cidade_entry.insert(END, col12)
            self.estado_entry.insert(END, col13)
            self.observacoes_entry.insert(END, col14)
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ?""", (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_cliente()
        self.select_lista()
    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET CPF = ?, nome = ?, data_nascimento = ?, sexo = ?, telefone = ?, cep = ?, rua = ?, numero = ?, complemento = ?, bairro = ?, cidade = ?, estado = ?, observacoes = ? WHERE cod = ? """, (self.CPF, self.nome, self.data_nascimento, self.sexo, self.telefone, self.cep, self.rua, self.numero, self.complemento, self.bairro, self.cidade, self.estado, self.observacoes, self.codigo))
        self.conn.commit()

        self.desconecta_bd()
        self.select_lista()
        self.limpa_cliente()
    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())

        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.cursor.execute(
            """SELECT cod, CPF, nome, data_nascimento, sexo, telefone, cep, rua, numero, complemento, bairro, cidade, estado, observacoes FROM clientes WHERE nome LIKE '%s' ORDER BY nome ASC""" % nome)
        busca_nomeCli = self.cursor.fetchall()
        for i in busca_nomeCli:
            self.listaCli.insert("", END, values=i)
        self.limpa_cliente()
        self.desconecta_bd()


class Application(Funcs, Relatorios):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()
    def tela(self):
        self.root.title("Cadastro de Clientes")
        self.root.configure(background= "#CFE3BB")
        self.root.geometry("1920x1080")
        self.root.resizable(True, True)
        self.root.state("zoomed")
        self.root.maxsize(width=1920, height=1080)
        self.root.minsize(width=400, height=300)
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg= "#c0c3cc", highlightbackground='#8C8C8C', highlightthickness=3)
        self.frame_1.place(relx =0.02 , rely=0.02, relwidth=0.96, relheight=0.46)

        self.frame_2 = Frame(self.root, bd=4, bg= '#c0c3cc', highlightbackground='#8C8C8C', highlightthickness=3)
        self.frame_2.place(relx =0.02 , rely=0.5, relwidth=0.96, relheight=0.46)
    def widgets_frame1(self):
        # Botão Limpar alinhado à esquerda
        self.bt_limpar = Button(self.frame_1, text="Limpar", font=("DejaVu Sans Mono", 14, "bold"), bd=3, command=self.limpa_cliente)
        self.bt_limpar.place(relx=0.05, rely=0.05, relwidth=0.1, relheight=0.08)

        # Botão Buscar logo ao lado
        self.bt_buscar = Button(self.frame_1, text="Buscar", font=("DejaVu Sans Mono", 14, "bold"), bd=3, command=self.busca_cliente)
        self.bt_buscar.place(relx=0.17, rely=0.05, relwidth=0.1, relheight=0.08)

        # Os demais podem continuar mais à direita
        self.bt_novo = Button(self.frame_1, text="Novo", font=("DejaVu Sans Mono", 14, "bold"), bd=3, command=self.add_cliente)
        self.bt_novo.place(relx=0.6, rely=0.05, relwidth=0.1, relheight=0.08)

        self.bt_alterar = Button(self.frame_1, text="Alterar", font=("DejaVu Sans Mono", 14, "bold"), bd=3, command= self.altera_cliente)
        self.bt_alterar.place(relx=0.72, rely=0.05, relwidth=0.1, relheight=0.08)

        self.bt_apagar = Button(self.frame_1, text="Apagar", font=("DejaVu Sans Mono", 14, "bold"), bd=3, command=self.deleta_cliente)
        self.bt_apagar.place(relx=0.84, rely=0.05, relwidth=0.1, relheight=0.08)

        ### Linha 1: Código, CPF e Nome
        self.lb_codigo = Label(self.frame_1, text="Código", bg="#c0c3cc", font=("DejaVu Sans Mono", 12, "bold"))
        self.lb_codigo.place(relx=0.05, rely=0.20)
        self.codigo_entry = Entry(self.frame_1, width=5,font=("DejaVu Sans Mono", 14))
        self.codigo_entry.place(relx=0.05, rely=0.25, relwidth=0.07, relheight=0.05)

        self.lb_CPF = Label(self.frame_1, text="CPF", bg="#c0c3cc", font=("DejaVu Sans Mono", 12, "bold"))
        self.lb_CPF.place(relx=0.20, rely=0.20)
        self.CPF_entry = Entry(self.frame_1, width=12, font=("DejaVu Sans Mono", 14))
        self.CPF_entry.place(relx=0.20, rely=0.25, relwidth=0.15, relheight=0.05)

        self.lb_nome = Label(self.frame_1, text="Nome", bg="#c0c3cc", font=("DejaVu Sans Mono", 12, "bold"))
        self.lb_nome.place(relx=0.40, rely=0.20)
        self.nome_entry = Entry(self.frame_1, width=50, font=("DejaVu Sans Mono", 14))
        self.nome_entry.place(relx=0.40, rely=0.25, relwidth=0.50, relheight=0.05)

        ### Linha 2: Data de Nascimento, Sexo e Telefone
        self.lb_data_nascimento = Label(self.frame_1, text="Data de Nascimento", bg="#c0c3cc", font=("DejaVu Sans Mono", 12, "bold"))
        self.lb_data_nascimento.place(relx=0.05, rely=0.35)
        self.data_nascimento_entry = Entry(self.frame_1, width=10, font=("DejaVu Sans Mono", 14))
        self.data_nascimento_entry.place(relx=0.05, rely=0.40, relwidth=0.15, relheight=0.05)

        self.lb_sexo = Label(self.frame_1, text="Sexo", bg="#c0c3cc", font=("DejaVu Sans Mono", 12, "bold"))
        self.lb_sexo.place(relx=0.25, rely=0.35)
        self.sexo_entry = Entry(self.frame_1, width=10, font=("DejaVu Sans Mono", 14))
        self.sexo_entry.place(relx=0.25, rely=0.40, relwidth=0.10, relheight=0.05)

        self.lb_telefone = Label(self.frame_1, text="Telefone", bg="#c0c3cc", font=("DejaVu Sans Mono", 12, "bold"))
        self.lb_telefone.place(relx=0.40, rely=0.35)
        self.telefone_entry = Entry(self.frame_1, width=15, font=("DejaVu Sans Mono", 14))
        self.telefone_entry.place(relx=0.40, rely=0.40, relwidth=0.20, relheight=0.05)

        ### Linha 3: CEP, Rua, Número, Complemento, Bairro, Cidade e Estado
        self.lb_cep = Label(self.frame_1, text="CEP", bg="#c0c3cc", font=("DejaVu Sans Mono", 12, "bold"))
        self.lb_cep.place(relx=0.05, rely=0.50)
        self.cep_entry = Entry(self.frame_1, width=8, font=("DejaVu Sans Mono", 14))
        self.cep_entry.place(relx=0.05, rely=0.55, relwidth=0.12, relheight=0.05)

        self.lb_rua = Label(self.frame_1, text="Rua", bg="#c0c3cc", font=("DejaVu Sans Mono", 12, "bold"))
        self.lb_rua.place(relx=0.20, rely=0.50)
        self.rua_entry = Entry(self.frame_1, width=40, font=("DejaVu Sans Mono", 14))
        self.rua_entry.place(relx=0.20, rely=0.55, relwidth=0.30, relheight=0.05)

        self.lb_numero = Label(self.frame_1, text="Número", bg="#c0c3cc", font=("DejaVu Sans Mono", 12, "bold"))
        self.lb_numero.place(relx=0.52, rely=0.50)
        self.numero_entry = Entry(self.frame_1, width=6, font=("DejaVu Sans Mono", 14))
        self.numero_entry.place(relx=0.52, rely=0.55, relwidth=0.10, relheight=0.05)

        self.lb_complemento = Label(self.frame_1, text="Complemento", bg="#c0c3cc", font=("DejaVu Sans Mono", 12, "bold"))
        self.lb_complemento.place(relx=0.65, rely=0.50)
        self.complemento_entry = Entry(self.frame_1, width=20, font=("DejaVu Sans Mono", 14))
        self.complemento_entry.place(relx=0.65, rely=0.55, relwidth=0.20, relheight=0.05)

        self.lb_bairro = Label(self.frame_1, text="Bairro", bg="#c0c3cc", font=("DejaVu Sans Mono", 12, "bold"))
        self.lb_bairro.place(relx=0.05, rely=0.65)
        self.bairro_entry = Entry(self.frame_1, width=30, font=("DejaVu Sans Mono", 14))
        self.bairro_entry.place(relx=0.05, rely=0.70, relwidth=0.25, relheight=0.05)

        self.lb_cidade = Label(self.frame_1, text="Cidade", bg="#c0c3cc", font=("DejaVu Sans Mono", 12, "bold"))
        self.lb_cidade.place(relx=0.35, rely=0.65)
        self.cidade_entry = Entry(self.frame_1, width=30, font=("DejaVu Sans Mono", 14))
        self.cidade_entry.place(relx=0.35, rely=0.70, relwidth=0.25, relheight=0.05)

        self.lb_estado = Label(self.frame_1, text="Estado", bg="#c0c3cc", font=("DejaVu Sans Mono", 12, "bold"))
        self.lb_estado.place(relx=0.65, rely=0.65)
        self.estado_entry = Entry(self.frame_1, width=2, font=("DejaVu Sans Mono", 14))
        self.estado_entry.place(relx=0.65, rely=0.70, relwidth=0.10, relheight=0.05)

        ### Linha 4: Observações
        self.lb_observacoes = Label(self.frame_1, text="Observações", bg="#c0c3cc", font=("DejaVu Sans Mono", 12, "bold"))
        self.lb_observacoes.place(relx=0.05, rely=0.80)
        self.observacoes_entry = Entry(self.frame_1, width=80, font=("DejaVu Sans Mono", 14))
        self.observacoes_entry.place(relx=0.05, rely=0.85, relwidth=0.85, relheight=0.05)
    def lista_frame2(self):
        self.listaCli = ttk.Treeview(self.frame_2, height=3, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8", "col9", "col10", "col11", "col12", "col13","col14"))
        self.listaCli.heading("#0", text="")
        self.listaCli.heading("#1", text="Código")
        self.listaCli.heading("#2", text="CPF")
        self.listaCli.heading("#3", text="Nome")
        self.listaCli.heading("#4", text="Data de Nascimento")
        self.listaCli.heading("#5", text="Sexo")
        self.listaCli.heading("#6", text="Telefone")
        self.listaCli.heading("#7", text="CEP")
        self.listaCli.heading("#8", text="Rua")
        self.listaCli.heading("#9", text="Numero")
        self.listaCli.heading("#10", text="Complemento")
        self.listaCli.heading("#11", text="Bairro")
        self.listaCli.heading("#12", text="Cidade")
        self.listaCli.heading("#13", text="Estado")
        self.listaCli.heading("#14", text="Observacoes")

        self.listaCli.column("#0", width=1)
        self.listaCli.column("#1", width=5)
        self.listaCli.column("#2", width=10)
        self.listaCli.column("#3", width=100)
        self.listaCli.column("#4", width=8)
        self.listaCli.column("#5", width=1)
        self.listaCli.column("#6", width=7)
        self.listaCli.column("#7", width=6)
        self.listaCli.column("#8", width=100)
        self.listaCli.column("#9", width=4)
        self.listaCli.column("#10", width=30)
        self.listaCli.column("#11", width=15)
        self.listaCli.column("#12", width=40)
        self.listaCli.column("#13", width=1)
        self.listaCli.column("#14", width=80)
        self.listaCli.place(relx=0.01, rely=0.1, relwidth=0.95, relheight=0.85)

        self.scrollLista = Scrollbar(self.frame_2, orient="vertical")
        self.listaCli.configure(yscroll=self.scrollLista.set)
        self.scrollLista.place(relx=0.96, rely=0.1, relwidth=0.02, relheight=0.85)
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)       
    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar, tearoff=0)
        filemenu2 = Menu(menubar, tearoff=0)

        def Quit(): self.root.destroy()

        menubar.add_cascade(label= "Opções", menu= filemenu)
        menubar.add_cascade(label= "Relatórios", menu= filemenu2)

        filemenu.add_command(label= "Sair", command= Quit)
        filemenu.add_command(label= "Limpa Cliente", command= self.limpa_cliente)

        filemenu2.add_command(label= "Ficha do Cliente", command= self.geraRelatCliente)


        



Application()