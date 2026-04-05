from tkinter import *
from tkinter import ttk, messagebox
import sqlite3
import webbrowser
from reportlab.pdfgen import canvas
import unicodedata
from datetime import datetime
import requests

root = Tk()
try:
    root.iconbitmap("icone.ico")
except:
    pass 

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
        campos = [
            ("Código............:", self.codigoRel),
            ("CPF...............:", self.CPFRel),
            ("Nome..............:", self.nomeRel),
            ("Data de Nascimento:", self.data_nascimentoRel),
            ("Sexo..............:", self.sexoRel),
            ("Telefone..........:", self.telefoneRel),
            ("CEP...............:", self.cepRel),
            ("Rua...............:", self.ruaRel),
            ("Número............:", self.numeroRel),
            ("Complemento.......:", self.complementoRel),
            ("Bairro............:", self.bairroRel),
            ("Cidade............:", self.cidadeRel),
            ("Estado............:", self.estadoRel),
            ("Observações.......:", self.observacoesRel),
        ]
        y = 760
        for label, valor in campos:
            self.c.drawString(50, y, label)
            self.c.setFont("Courier", 14)
            self.c.drawString(220, y, valor)
            self.c.setFont("Courier-Bold", 14)
            y -= 20

        self.c.showPage()
        self.c.save()
        self.printCliente()

class Funcs():
   
    def limpa_cliente(self):
        self.codigo_entry.configure(state="normal")
        self.codigo_entry.delete(0, END)
        self.codigo_entry.configure(state="disabled")
        
        self.CPF_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.data_nascimento_entry.delete(0, END)
        self.sexo_entry.set("")
        self.telefone_entry.delete(0, END)
        self.cep_entry.delete(0, END)
        
        # Limpa campos de endereço permitindo escrita temporária
        for campo in [self.rua_entry, self.numero_entry, self.complemento_entry, 
                      self.bairro_entry, self.cidade_entry, self.estado_entry]:
            campo.configure(state="normal")
            campo.delete(0, END)
            
        # Limpa o widget de Texto (Observações)
        self.observacoes_entry.delete("1.0", END)
        
        # 4. Define o foco inicial no CPF
        self.CPF_entry.focus_set()

    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.bd")
        self.conn.create_function("remover_acentos", 1, self.remover_acentos)
        self.cursor = self.conn.cursor()

    def desconecta_bd(self):
        self.conn.close()

    def montaTabelas(self):
        self.conecta_bd()
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
            ); """)
        self.conn.commit()
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
        self.observacoes = self.observacoes_entry.get("1.0", END).strip()

    def validar_cpf_logica(self, cpf):
        """ Algoritmo Real de Validação de CPF """
        cpf = "".join(filter(str.isdigit, cpf))
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        # Validação do 1º dígito
        soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
        digito_1 = (soma * 10 % 11) % 10
        # Validação do 2º dígito
        soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
        digito_2 = (soma * 10 % 11) % 10
        return cpf[-2:] == f"{digito_1}{digito_2}"

    def validar_entrada_num(self, novo_valor, limite):
        if novo_valor == "": return True
        # Durante a digitação, permitimos apenas números, pontos e traços (para a máscara)
        permitidos = "0123456789.-"
        if all(c in permitidos for c in novo_valor) and len(novo_valor) <= int(limite):
            return True
        return False

    def formatar_cpf_evento(self, event):
        valor = self.CPF_entry.get()
        num = "".join(filter(str.isdigit, valor))
        
        if len(num) == 0: return

        if len(num) == 11:
            if self.validar_cpf_logica(num):
                formatado = f"{num[:3]}.{num[3:6]}.{num[6:9]}-{num[9:]}"
                self.CPF_entry.configure(validate="none")
                self.CPF_entry.delete(0, END)
                self.CPF_entry.insert(0, formatado)
                self.CPF_entry.configure(validate="key")
            else:
                messagebox.showerror("Erro", "CPF Inválido! Verifique os dados.")
                self.CPF_entry.delete(0, END)
                self.CPF_entry.focus_set()
        else:
            messagebox.showwarning("Aviso", "O CPF deve conter 11 dígitos.")
            self.CPF_entry.focus_set()

    def add_cliente(self):
        self.variaveis()
        if not self.validar_cpf_logica(self.CPF):
            messagebox.showerror("Erro", "Não é possível salvar: CPF inválido.")
            return
        self.conecta_bd()
        try:
            self.cursor.execute(""" INSERT INTO clientes (CPF, nome, data_nascimento, sexo, telefone, cep, rua, numero, complemento, bairro, cidade, estado, observacoes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (self.CPF, self.nome, self.data_nascimento, self.sexo, self.telefone, self.cep, self.rua, self.numero, self.complemento, self.bairro, self.cidade, self.estado, self.observacoes))
            self.conn.commit()
            self.desconecta_bd()
            self.select_lista()
            self.limpa_cliente()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Este CPF já está cadastrado!")
            self.desconecta_bd()

    def select_lista(self):
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
            valores = self.listaCli.item(n, 'values')
            
            # 1. Código (Índice 0)
            self.codigo_entry.configure(state="normal")
            self.codigo_entry.insert(END, valores[0])
            self.codigo_entry.configure(state="disabled")

            # 2. Dados Pessoais (Índices 1 a 5)
            self.CPF_entry.insert(END, valores[1])
            self.nome_entry.insert(END, valores[2])
            self.data_nascimento_entry.insert(END, valores[3])
            self.sexo_entry.set(valores[4])
            self.telefone_entry.insert(END, valores[5])
            
            # 3. Endereço (Índices 6 a 12)
            # Precisamos de abrir o estado para inserir dados nos campos que ficam readonly
            campos_endereco = [
                (self.cep_entry, valores[6]),
                (self.rua_entry, valores[7]),
                (self.numero_entry, valores[8]),
                (self.complemento_entry, valores[9]),
                (self.bairro_entry, valores[10]),
                (self.cidade_entry, valores[11]),
                (self.estado_entry, valores[12])
            ]

            for campo, valor in campos_endereco:
                campo.configure(state="normal")
                campo.insert(END, valor)
                # Se for Rua, Bairro, Cidade ou UF, volta a travar após inserir
                if campo in [self.rua_entry, self.bairro_entry, self.cidade_entry, self.estado_entry]:
                    if valor.strip() != "":
                        campo.configure(state="readonly")

            # 4. Observações (Busca direta no Banco)
            # Como a Obs não está na tabela, usamos o Código para ler do BD
            self.conecta_bd()
            cod_id = valores[0]
            obs_bd = self.cursor.execute("SELECT observacoes FROM clientes WHERE cod = ?", (cod_id,)).fetchone()
            if obs_bd:
                self.observacoes_entry.insert("1.0", obs_bd[0])
            self.desconecta_bd()

    def deleta_cliente(self):
        self.variaveis()
        if not self.codigo:
            messagebox.showwarning("Aviso", "Selecione um cliente na lista primeiro.")
            return
        confirmar = messagebox.askyesno("Confirmar", f"Deseja excluir o registro de {self.nome}?")
        if confirmar:
            self.conecta_bd()
            self.cursor.execute("""DELETE FROM clientes WHERE cod = ?""", (self.codigo,))
            self.conn.commit()
            self.desconecta_bd()
            self.limpa_cliente()
            self.select_lista()

    def altera_cliente(self):
        self.variaveis()
        if not self.codigo:
            messagebox.showwarning("Aviso", "Selecione um cliente para alterar.")
            return
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET CPF = ?, nome = ?, data_nascimento = ?, sexo = ?, telefone = ?, cep = ?, rua = ?, numero = ?, complemento = ?, bairro = ?, cidade = ?, estado = ?, observacoes = ? WHERE cod = ? """, (self.CPF, self.nome, self.data_nascimento, self.sexo, self.telefone, self.cep, self.rua, self.numero, self.complemento, self.bairro, self.cidade, self.estado, self.observacoes, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_cliente()

    def busca_cpf(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())
        
        # Pega o que o usuário digitou
        cpf_digitado = self.CPF_entry.get()
        # Remove qualquer formatação manual para ter apenas os números
        num = "".join(filter(str.isdigit, cpf_digitado))
        
        # Se o usuário digitou os 11 dígitos, aplicamos a máscara para a busca
        if len(num) == 11:
            cpf_para_busca = f"{num[:3]}.{num[3:6]}.{num[6:9]}-{num[9:]}"
        else:
            # Se digitou menos (busca parcial), usamos o que ele digitou com curingas
            cpf_para_busca = '%' + cpf_digitado + '%'

        self.cursor.execute(
            "SELECT cod, CPF, nome, data_nascimento, sexo, telefone, cep, rua, numero, complemento, bairro, cidade, estado, observacoes "
            "FROM clientes WHERE CPF LIKE ? ORDER BY nome ASC", (cpf_para_busca,))
        
        buscas = self.cursor.fetchall()
        for i in buscas:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()

    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())
        nome = self.nome_entry.get()
        # Note o uso do remover_acentos que você já tem no sistema
        self.cursor.execute("SELECT cod, CPF, nome, data_nascimento, sexo, telefone, cep, rua, numero, complemento, bairro, cidade, estado, observacoes FROM clientes WHERE remover_acentos(nome) LIKE remover_acentos(?) ORDER BY nome ASC", ('%' + nome + '%',))
        buscas = self.cursor.fetchall()
        for i in buscas:
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()
    
    def validar_tamanho_nome(self, novo_valor):
        # Permite a digitação apenas se tiver 50 caracteres ou menos
        return len(novo_valor) <= 50

    def tratar_nome(self, event):
        # Pega o texto, transforma em maiúsculo e remove espaços inúteis nas pontas
        texto_maiusculo = self.nome_entry.get().upper().strip()
        self.nome_entry.delete(0, END)
        self.nome_entry.insert(0, texto_maiusculo)

    def forcar_maiusculo(self, event):
        widget = event.widget
        posicao = widget.index(INSERT) # Guarda a posição do cursor
        conteudo = widget.get().upper()
        widget.delete(0, END)
        widget.insert(0, conteudo)
        widget.icursor(posicao) # Devolve o cursor para o lugar certo

    def remover_acentos(self, texto):
        if not texto: return ""
        return "".join(c for c in unicodedata.normalize('NFD', texto)
                   if unicodedata.category(c) != 'Mn').upper()

    def validar_data_evento(self, event):
        data_digita = self.data_nascimento_entry.get()
        # Remove barras para análise, caso já existam
        num = "".join(filter(str.isdigit, data_digita))
        
        if len(num) == 0: 
            return

        if len(num) == 8:
            try:
                dia = int(num[:2])
                mes = int(num[2:4])
                ano = int(num[4:])
                datetime(ano, mes, dia)
                
                # --- O SEGREDO ESTÁ AQUI ---
                # 1. Desliga a validação de teclado para não dar conflito
                self.data_nascimento_entry.configure(validate="none")
                
                # 2. Formata o campo
                self.data_nascimento_entry.delete(0, END)
                self.data_nascimento_entry.insert(0, f"{num[:2]}/{num[2:4]}/{num[4:]}")
                
                # 3. Liga a validação de volta
                self.data_nascimento_entry.configure(validate="key")
                
            except ValueError:
                messagebox.showerror("Erro", "Data Inválida! Digite uma data real.")
                self.data_nascimento_entry.delete(0, END)
                self.data_nascimento_entry.focus_set()
        else:
            # Caso tenha menos de 8 dígitos e não esteja vazio
            messagebox.showwarning("Aviso", "A data deve ter 8 dígitos (DDMMAAAA).")
            self.data_nascimento_entry.focus_set()

    def formatar_telefone_evento(self, event):
        valor = self.telefone_entry.get()
        # Remove qualquer máscara anterior para analisar apenas os números
        num = "".join(filter(str.isdigit, valor))
        
        if len(num) == 0: return

        # Desativa validação para formatar
        self.telefone_entry.configure(validate="none")
        self.telefone_entry.delete(0, END)

        if len(num) == 11: # Celular: (XX) 9XXXX-XXXX
            self.telefone_entry.insert(0, f"({num[:2]}){num[2:7]}-{num[7:]}")
        elif len(num) == 10: # Fixo: (XX) XXXX-XXXX
            self.telefone_entry.insert(0, f"({num[:2]}){num[2:6]}-{num[6:]}")
        else:
            # Se não tiver 10 nem 11, devolve os números e avisa
            self.telefone_entry.insert(0, num)
            messagebox.showwarning("Aviso", "Telefone deve ter 10 (fixo) ou 11 (celular) dígitos.")
            self.telefone_entry.focus_set()

        # Reativa validação
        self.telefone_entry.configure(validate="key")

    def consulta_cep(self, cep):
        try:
            # Remove qualquer máscara e limpa espaços
            cep = "".join(filter(str.isdigit, cep))
            if len(cep) != 8:
                return None
                
            url = f"https://viacep.com.br/ws/{cep}/json/"
            retorno = requests.get(url, timeout=5)
            dados = retorno.json()
            
            if "erro" in dados:
                return None
            return dados
        except:
            return None # Se a internet cair, por exemplo
    
    def preencher_endereco_cep(self, event):
        cep_digitado = self.cep_entry.get()
        dados = self.consulta_cep(cep_digitado)
        
        # Lista dos campos que serão afetados
        campos = [self.rua_entry, self.bairro_entry, self.cidade_entry, self.estado_entry]
        
        if dados:
            # 1. Prepara os campos (destrava e limpa)
            for campo in campos:
                campo.configure(state="normal")
                campo.delete(0, END)
            
            # 2. Insere os dados formatados em Maiúsculo
            self.rua_entry.insert(0, dados.get('logradouro', '').upper())
            self.bairro_entry.insert(0, dados.get('bairro', '').upper())
            self.cidade_entry.insert(0, dados.get('localidade', '').upper())
            self.estado_entry.insert(0, dados.get('uf', '').upper())
            
            # 3. Trava os campos e aplica a cor de fundo cinza escuro
            for campo in campos:
                campo.configure(state="readonly", readonlybackground="#bebebe")
            
            # Move o foco para o Número, que é o próximo passo lógico do usuário
            self.numero_entry.focus_set()
        else:
            # Se o CEP for inválido ou erro de rede, libera para digitação manual
            for campo in campos:
                campo.configure(state="normal", background="white")
                campo.delete(0, END)
            
            if len("".join(filter(str.isdigit, cep_digitado))) == 8:
                messagebox.showinfo("CEP", "CEP não localizado. Por favor, digite o endereço manualmente.")

    def atalho_teclado_sexo(self, event):
        # Captura a tecla pressionada e coloca em minúsculo para comparar
        tecla = event.char.lower()
        
        if tecla == 'm':
            self.sexo_entry.set("MASCULINO")
        elif tecla == 'f':
            self.sexo_entry.set("FEMININO")
        elif tecla == 't':
            self.sexo_entry.set("TRANS")
            
        # Retorna "break" para impedir que o sistema tente escrever a letra na caixa
        return "break"
    
    def pular_para_telefone(self, event):
        self.telefone_entry.focus_set()
        # Retorna "break" para o TAB original do sistema não interferir
        return "break"

    def validar_alfanumerico(self, novo_valor, limite):
        if novo_valor == "": return True
        # Verifica se o tamanho está dentro do limite e se não há caracteres estranhos
        # (Opcional: você pode remover o isalnum() se quiser aceitar símbolos como / ou -)
        if len(novo_valor) <= int(limite):
            return True
        return False

    def validar_obs(self, event):
        # Pega todo o conteúdo do widget Text
        conteudo = self.observacoes_entry.get("1.0", END).upper()
        
        # Se passar de 200 caracteres, corta
        if len(conteudo) > 200:
            conteudo = conteudo[:200]
        
        # Guarda a posição do cursor (index)
        posicao = self.observacoes_entry.index(INSERT)
        
        # Atualiza o campo com o texto em maiúsculo e limitado
        self.observacoes_entry.delete("1.0", END)
        self.observacoes_entry.insert("1.0", conteudo)
        
        # Devolve o cursor para o lugar certo
        self.observacoes_entry.mark_set(INSERT, posicao)

class Application(Funcs, Relatorios):
    def __init__(self):
        self.root = root
        self.opcoes_sexo = ["MASCULINO", "FEMININO", "TRANS"]
        self.v_nome = self.root.register(self.validar_tamanho_nome)
        self.vcmd = self.root.register(self.validar_entrada_num)
        self.v_alfanum = self.root.register(self.validar_alfanumerico)
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.montaTabelas()
        self.select_lista()
        self.Menus()
        root.mainloop()

    def tela(self):
        self.root.title("Hotel Rampim - Gestão de Clientes")
        self.root.configure(background="#CFE3BB")
        self.root.geometry("1200x800")
        self.root.resizable(True, True)
        self.root.state("zoomed")

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd=4, bg="#c0c3cc", highlightbackground='#8C8C8C', highlightthickness=3)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46)
        self.frame_2 = Frame(self.root, bd=4, bg='#c0c3cc', highlightbackground='#8C8C8C', highlightthickness=3)
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):
        # --- CONTAINER ESQUERDA (DADOS) ---
        self.frame_dados = LabelFrame(self.frame_1, text=" Dados do Cliente ", bg="#c0c3cc", 
                                      font=("DejaVu Sans Mono", 10, "bold"), bd=2, relief="groove")
        self.frame_dados.place(relx=0.01, rely=0.01, relwidth=0.62, relheight=0.96)

        # --- SUB-FRAME BUSCAS (CONTORNO) ---
        self.area_busca = LabelFrame(self.frame_dados, text=" Consultas ", bg="#c0c3cc", bd=2)
        self.area_busca.place(relx=0.02, rely=0.01, relwidth=0.42, relheight=0.18)

        self.bt_buscar = Button(self.area_busca, text="Nome", font=("DejaVu Sans Mono", 10, "bold"), command=self.busca_cliente)
        self.bt_buscar.place(relx=0.05, rely=0.1, relwidth=0.45, relheight=0.8)
        self.bt_buscar_cpf = Button(self.area_busca, text="CPF", font=("DejaVu Sans Mono", 10, "bold"), command=self.busca_cpf)
        self.bt_buscar_cpf.place(relx=0.52, rely=0.1, relwidth=0.45, relheight=0.8)

        # --- SUB-FRAME CRUD (CONTORNO) ---
        self.area_crud = LabelFrame(self.frame_dados, text=" Ações ", bg="#c0c3cc", bd=2)
        self.area_crud.place(relx=0.46, rely=0.01, relwidth=0.52, relheight=0.18)

        botoes = [("Novo", self.add_cliente, 0.02), ("Alterar", self.altera_cliente, 0.27), 
                  ("Apagar", self.deleta_cliente, 0.52), ("Limpar", self.limpa_cliente, 0.77)]
        for texto, comando, x in botoes:
            Button(self.area_crud, text=texto, font=("DejaVu Sans Mono", 9, "bold"), command=comando).place(relx=x, rely=0.1, relwidth=0.21, relheight=0.8)

        # LABELS E ENTRADAS (REORGANIZADOS NA ESQUERDA)
        # Linha 1: Código e CPF
        Label(self.frame_dados, text="Código", bg="#c0c3cc", font=("DejaVu Sans Mono", 10, "bold")).place(relx=0.02, rely=0.22)
        self.codigo_entry = Entry(self.frame_dados, font=("DejaVu Sans Mono", 12), state="disabled", disabledbackground="#bebebe")
        self.codigo_entry.place(relx=0.02, rely=0.28, relwidth=0.12, relheight=0.06)

        Label(self.frame_dados, text="CPF", bg="#c0c3cc", font=("DejaVu Sans Mono", 10, "bold")).place(relx=0.18, rely=0.22)
        self.CPF_entry = Entry(self.frame_dados, font=("DejaVu Sans Mono", 12), validate="key", validatecommand=(self.vcmd, '%P', 14))
        self.CPF_entry.place(relx=0.18, rely=0.28, relwidth=0.25, relheight=0.06)
        self.CPF_entry.bind("<FocusOut>", self.formatar_cpf_evento)

        Label(self.frame_dados, text="Nome", bg="#c0c3cc", font=("DejaVu Sans Mono", 10, "bold")).place(relx=0.46, rely=0.22)
        self.nome_entry = Entry(self.frame_dados, font=("DejaVu Sans Mono", 12), validate="key", validatecommand=(self.v_nome, '%P'))
        self.nome_entry.place(relx=0.46, rely=0.28, relwidth=0.52, relheight=0.06)
        self.nome_entry.bind("<KeyRelease>", self.forcar_maiusculo)

        # Linha 2: Nascimento, Sexo, Telefone
        Label(self.frame_dados, text="Nascimento", bg="#c0c3cc", font=("DejaVu Sans Mono", 10, "bold")).place(relx=0.02, rely=0.38)
        self.data_nascimento_entry = Entry(self.frame_dados, font=("DejaVu Sans Mono", 12), validate="key", validatecommand=(self.vcmd, '%P', 8))
        self.data_nascimento_entry.place(relx=0.02, rely=0.44, relwidth=0.25, relheight=0.06)
        self.data_nascimento_entry.bind("<FocusOut>", self.validar_data_evento)

        Label(self.frame_dados, text="Sexo", bg="#c0c3cc", font=("DejaVu Sans Mono", 10, "bold")).place(relx=0.30, rely=0.38)
        self.sexo_entry = ttk.Combobox(self.frame_dados, values=self.opcoes_sexo, font=("DejaVu Sans Mono", 12), state="readonly")
        self.sexo_entry.place(relx=0.30, rely=0.44, relwidth=0.18, relheight=0.06)
        self.sexo_entry.bind("<Key>", self.atalho_teclado_sexo)
        self.sexo_entry.bind("<Tab>", self.pular_para_telefone)

        Label(self.frame_dados, text="Telefone", bg="#c0c3cc", font=("DejaVu Sans Mono", 10, "bold")).place(relx=0.51, rely=0.38)
        self.telefone_entry = Entry(self.frame_dados, font=("DejaVu Sans Mono", 12), validate="key", validatecommand=(self.vcmd, '%P', 11))
        self.telefone_entry.place(relx=0.51, rely=0.44, relwidth=0.47, relheight=0.06)
        self.telefone_entry.bind("<FocusOut>", self.formatar_telefone_evento)

        # Linha 3: CEP e Rua
        Label(self.frame_dados, text="CEP", bg="#c0c3cc", font=("DejaVu Sans Mono", 10, "bold")).place(relx=0.02, rely=0.54)
        self.cep_entry = Entry(self.frame_dados, font=("DejaVu Sans Mono", 12), validate="key", validatecommand=(self.vcmd, '%P', 8))
        self.cep_entry.place(relx=0.02, rely=0.60, relwidth=0.20, relheight=0.06)
        self.cep_entry.bind("<FocusOut>", self.preencher_endereco_cep)

        Label(self.frame_dados, text="Rua", bg="#c0c3cc", font=("DejaVu Sans Mono", 10, "bold")).place(relx=0.25, rely=0.54)
        self.rua_entry = Entry(self.frame_dados, font=("DejaVu Sans Mono", 12), readonlybackground="#bebebe")
        self.rua_entry.place(relx=0.25, rely=0.60, relwidth=0.73, relheight=0.06)

        # Linha 4: Nº, Compl, Bairro
        Label(self.frame_dados, text="Nº", bg="#c0c3cc", font=("DejaVu Sans Mono", 10, "bold")).place(relx=0.02, rely=0.70)
        self.numero_entry = Entry(self.frame_dados, font=("DejaVu Sans Mono", 12), validate="key", validatecommand=(self.vcmd, '%P', 6))
        self.numero_entry.place(relx=0.02, rely=0.76, relwidth=0.12, relheight=0.06)

        Label(self.frame_dados, text="Compl.", bg="#c0c3cc", font=("DejaVu Sans Mono", 10, "bold")).place(relx=0.16, rely=0.70)
        self.complemento_entry = Entry(self.frame_dados, font=("DejaVu Sans Mono", 12), validate="key", validatecommand=(self.v_alfanum, '%P', 30))
        self.complemento_entry.place(relx=0.16, rely=0.76, relwidth=0.25, relheight=0.06)
        self.complemento_entry.bind("<KeyRelease>", self.forcar_maiusculo)

        Label(self.frame_dados, text="Bairro", bg="#c0c3cc", font=("DejaVu Sans Mono", 10, "bold")).place(relx=0.43, rely=0.70)
        self.bairro_entry = Entry(self.frame_dados, font=("DejaVu Sans Mono", 12), readonlybackground="#bebebe")
        self.bairro_entry.place(relx=0.43, rely=0.76, relwidth=0.55, relheight=0.06)

        # Linha 5: Cidade e UF
        Label(self.frame_dados, text="Cidade", bg="#c0c3cc", font=("DejaVu Sans Mono", 10, "bold")).place(relx=0.02, rely=0.86)
        self.cidade_entry = Entry(self.frame_dados, font=("DejaVu Sans Mono", 12), readonlybackground="#bebebe")
        self.cidade_entry.place(relx=0.02, rely=0.91, relwidth=0.75, relheight=0.06)

        Label(self.frame_dados, text="UF", bg="#c0c3cc", font=("DejaVu Sans Mono", 10, "bold")).place(relx=0.80, rely=0.86)
        self.estado_entry = Entry(self.frame_dados, font=("DejaVu Sans Mono", 12), readonlybackground="#bebebe")
        self.estado_entry.place(relx=0.80, rely=0.91, relwidth=0.18, relheight=0.06)

        # --- CONTAINER DIREITA (OBSERVAÇÕES) ---
        self.frame_obs = LabelFrame(self.frame_1, text=" Observações Internas ", bg="#c0c3cc", 
                                    font=("DejaVu Sans Mono", 10, "bold"), bd=2, relief="groove")
        self.frame_obs.place(relx=0.64, rely=0.01, relwidth=0.35, relheight=0.96)

        self.observacoes_entry = Text(self.frame_obs, font=("DejaVu Sans Mono", 11), wrap=WORD)
        self.observacoes_entry.place(relx=0.05, rely=0.05, relwidth=0.90, relheight=0.90)
        # Bind para Maiúsculo e Limite
        self.observacoes_entry.bind("<KeyRelease>", self.validar_obs)

        self.CPF_entry.focus_set()

    def lista_frame2(self):
        # Configuração do Estilo para Negrito e Linhas de Grade
        style = ttk.Style()
        style.theme_use("alt") # O tema 'alt' suporta melhor a customização de grades
        style.configure("Treeview.Heading", 
                        font=("DejaVu Sans Mono", 10, "bold"), 
                        anchor="w") # Título alinhado à esquerda
        
        style.configure("Treeview", 
                        highlightthickness=0, 
                        bd=0, 
                        font=("DejaVu Sans Mono", 9),
                        rowheight=25)
        
        # Cores para as linhas de grade (efeito zebrado opcional)
        style.map("Treeview", background=[('selected', '#108ecb')])

        colunas = ("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8", "col9", "col10", "col11", "col12", "col13")
        
        # O 'show=headings' oculta a coluna fantasma #0, mas mantém os títulos
        self.listaCli = ttk.Treeview(self.frame_2, height=3, columns=colunas, show='headings')
        
        # Configuração das Colunas
        # Nome reduzido de 250 para 200, Rua e Bairro aumentados
        config_colunas = [
            ("col1", "Cod", 45, "center", False),
            ("col2", "CPF", 110, "w", False),
            ("col3", "Nome do Cliente", 200, "w", True), # Ainda expande, mas com base menor
            ("col4", "Nasc.", 90, "w", False),
            ("col5", "Sexo", 80, "w", False),
            ("col6", "Telefone", 110, "w", False),
            ("col7", "CEP", 80, "w", False),
            ("col8", "Rua", 220, "w", True),   # Rua agora também expande
            ("col9", "Nº", 50, "w", False),
            ("col10", "Compl.", 100, "w", False),
            ("col11", "Bairro", 150, "w", False),
            ("col12", "Cidade", 130, "w", False),
            ("col13", "UF", 40, "center", False)
        ]

        for col, nome, larg, alinh, exp in config_colunas:
            self.listaCli.heading(col, text=nome, anchor="w") # Título à esquerda
            self.listaCli.column(col, width=larg, anchor=alinh, stretch=exp)

        # Posicionamento
        self.listaCli.place(relx=0.01, rely=0.05, relwidth=0.95, relheight=0.90)

        # Scrollbar
        self.scrollLista = Scrollbar(self.frame_2, orient="vertical")
        self.listaCli.configure(yscroll=self.scrollLista.set)
        self.scrollLista.place(relx=0.96, rely=0.05, relwidth=0.02, relheight=0.90)
        
        self.listaCli.bind("<Double-1>", self.OnDoubleClick)

    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        filemenu = Menu(menubar, tearoff=0)
        filemenu2 = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opções", menu=filemenu)
        menubar.add_cascade(label="Relatórios", menu=filemenu2)
        filemenu.add_command(label="Sair", command=self.root.destroy)
        filemenu.add_command(label="Limpa Cliente", command=self.limpa_cliente)
        filemenu2.add_command(label="Ficha do Cliente", command=self.geraRelatCliente)

if __name__ == "__main__":
    Application()