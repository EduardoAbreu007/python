import mysql.connector
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput

class CRUDApp(App):
    def build(self):
        # Conexão com o banco de dados
        self.mydb = mysql.connector.connect(
            host="localhost",
            port=3307,  # Especificando a porta
            user="root",
            password="senac",
            database="parque_diversao",
        )
        return self.create_layout()

    def create_layout(self):
        layout = GridLayout(cols=2, spacing=10, padding=10)

        # Campos para Produto
        layout.add_widget(Label(text="Nome do Produto:"))
        self.nome_produto_input = TextInput(multiline=False)
        layout.add_widget(self.nome_produto_input)

        layout.add_widget(Label(text="Preço do Produto:"))
        self.preco_produto_input = TextInput(multiline=False)
        layout.add_widget(self.preco_produto_input)

        criar_produto_button = Button(text="Criar Produto")
        criar_produto_button.bind(on_press=self.criar_produto)
        layout.add_widget(criar_produto_button)

        # Campos para Serviço
        layout.add_widget(Label(text="Nome do Serviço:"))
        self.nome_servico_input = TextInput(multiline=False)
        layout.add_widget(self.nome_servico_input)

        layout.add_widget(Label(text="Descrição do Serviço:"))
        self.descricao_servico_input = TextInput(multiline=False)
        layout.add_widget(self.descricao_servico_input)

        criar_servico_button = Button(text="Criar Serviço")
        criar_servico_button.bind(on_press=self.criar_servico)
        layout.add_widget(criar_servico_button)

        # Campos para Cliente
        layout.add_widget(Label(text="Nome do Cliente:"))
        self.nome_cliente_input = TextInput(multiline=False)
        layout.add_widget(self.nome_cliente_input)

        layout.add_widget(Label(text="Email do Cliente:"))
        self.email_cliente_input = TextInput(multiline=False)
        layout.add_widget(self.email_cliente_input)

        criar_cliente_button = Button(text="Criar Cliente")
        criar_cliente_button.bind(on_press=self.criar_cliente)
        layout.add_widget(criar_cliente_button)

        # Listagem
        self.listar_layout = BoxLayout(orientation="vertical")
        scrollview = ScrollView()
        scrollview.add_widget(self.listar_layout)
        layout.add_widget(scrollview)

        self.atualizar_lista()
        return layout

    def execute_sql(self, query, values=None):
        """Função genérica para executar comandos SQL."""
        cursor = self.mydb.cursor()
        try:
            if values:
                cursor.execute(query, values)
            else:
                cursor.execute(query)
            self.mydb.commit()
        except mysql.connector.Error as err:
            print(f"Erro ao executar query: {err}")
        finally:
            cursor.close()

    def criar_produto(self, instance):
        nome = self.nome_produto_input.text
        preco = self.preco_produto_input.text
        if nome and preco:
            query = "INSERT INTO produtos (nome, preco) VALUES (%s, %s)"
            values = (nome, preco)
            self.execute_sql(query, values)
            self.atualizar_lista()
        else:
            print("Nome e preço são obrigatórios!")

    def criar_servico(self, instance):
        nome = self.nome_servico_input.text
        descricao = self.descricao_servico_input.text
        if nome and descricao:
            query = "INSERT INTO servicos (nome, descricao) VALUES (%s, %s)"
            values = (nome, descricao)
            self.execute_sql(query, values)
            self.atualizar_lista()
        else:
            print("Nome e descrição são obrigatórios!")

    def criar_cliente(self, instance):
        nome = self.nome_cliente_input.text
        email = self.email_cliente_input.text
        if nome and email:
            query = "INSERT INTO clientes (nome, email) VALUES (%s, %s)"
            values = (nome, email)
            self.execute_sql(query, values)
            self.atualizar_lista()
        else:
            print("Nome e e-mail são obrigatórios!")

    def atualizar_lista(self):
        self.listar_layout.clear_widgets()
        cursor = self.mydb.cursor()

        # Listar Produtos
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()
        for produto in produtos:
            label = Label(text=f"Produto: {produto[1]} - R$ {produto[2]}")
            self.listar_layout.add_widget(label)

        # Listar Serviços
        cursor.execute("SELECT * FROM servicos")
        servicos = cursor.fetchall()
        for servico in servicos:
            label = Label(text=f"Serviço: {servico[1]} - {servico[2]}")
            self.listar_layout.add_widget(label)

        # Listar Clientes
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        for cliente in clientes:
            label = Label(text=f"Cliente: {cliente[1]} - {cliente[2]}")
            self.listar_layout.add_widget(label)

        cursor.close()

    def on_stop(self):
        """Fechar a conexão com o banco de dados ao finalizar o aplicativo."""
        if self.mydb.is_connected():
            self.mydb.close()
            print("Conexão com o banco de dados fechada.")

if __name__ == "__main__":
    CRUDApp().run()