import tkinter as tk
from tkinter import ttk
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

class BlogApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blog App")

        # Conexión a la base de datos
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['blogdb']

        # Definición de las colecciones
        self.users_collection = self.db['users']
        self.comments_collection = self.db['comments']
        self.categories_collection = self.db['categories']
        self.articles_collection = self.db['articles']

        # Crear el widget Notebook para las pestañas
        self.notebook = ttk.Notebook(root)

        # Pestañas para cada tabla
        self.create_user_tab()
        self.create_comment_tab()
        self.create_category_tab()
        self.create_article_tab()

        # Ajustar la geometría de la interfaz
        self.notebook.pack(expand=1, fill="both")

    def create_user_tab(self):
        user_tab = ttk.Frame(self.notebook)
        self.notebook.add(user_tab, text="Usuarios")

        # Treeview para mostrar los usuarios
        self.user_tree = ttk.Treeview(user_tab, columns=('Name', 'Email'), show='headings')
        self.user_tree.heading('Name', text='Nombre')
        self.user_tree.heading('Email', text='Email')
        self.user_tree.pack(fill='both', expand=True)

        # Cuadros de entrada para agregar usuarios
        self.user_name_entry = tk.Entry(user_tab)
        self.user_name_entry.pack()
        self.user_email_entry = tk.Entry(user_tab)
        self.user_email_entry.pack()

        # Botones para CRUD de usuarios
        add_user_button = tk.Button(user_tab, text="Agregar Usuario", command=self.add_user)
        add_user_button.pack(side=tk.LEFT)

        delete_user_button = tk.Button(user_tab, text="Eliminar Usuario", command=self.delete_user)
        delete_user_button.pack(side=tk.LEFT)

    def create_comment_tab(self):
        comment_tab = ttk.Frame(self.notebook)
        self.notebook.add(comment_tab, text="Comentarios")

        # Treeview para mostrar los comentarios
        comment_tree = ttk.Treeview(comment_tab, columns=('Name', 'URL', 'User ID', 'Article ID'), show='headings')
        comment_tree.heading('Name', text='Nombre')
        comment_tree.heading('URL', text='URL')
        comment_tree.heading('User ID', text='ID de Usuario')
        comment_tree.heading('Article ID', text='ID de Artículo')
        comment_tree.pack(fill='both', expand=True)

        # Cuadros de entrada para agregar comentarios
        self.comment_name_entry = tk.Entry(comment_tab)
        self.comment_name_entry.pack()
        self.comment_url_entry = tk.Entry(comment_tab)
        self.comment_url_entry.pack()

        # Botones para CRUD de comentarios
        add_comment_button = tk.Button(comment_tab, text="Agregar Comentario", command=self.add_comment)
        add_comment_button.pack(side=tk.LEFT)

        delete_comment_button = tk.Button(comment_tab, text="Eliminar Comentario", command=self.delete_comment)
        delete_comment_button.pack(side=tk.LEFT)

    def create_category_tab(self):
        category_tab = ttk.Frame(self.notebook)
        self.notebook.add(category_tab, text="Categorías")

        # Treeview para mostrar las categorías
        category_tree = ttk.Treeview(category_tab, columns=('Name', 'URL'), show='headings')
        category_tree.heading('Name', text='Nombre')
        category_tree.heading('URL', text='URL')
        category_tree.pack(fill='both', expand=True)

        # Cuadros de entrada para agregar categorías
        self.category_name_entry = tk.Entry(category_tab)
        self.category_name_entry.pack()
        self.category_url_entry = tk.Entry(category_tab)
        self.category_url_entry.pack()

        # Botones para CRUD de categorías
        add_category_button = tk.Button(category_tab, text="Agregar Categoría", command=self.add_category)
        add_category_button.pack(side=tk.LEFT)

        delete_category_button = tk.Button(category_tab, text="Eliminar Categoría", command=self.delete_category)
        delete_category_button.pack(side=tk.LEFT)

    def create_article_tab(self):
        article_tab = ttk.Frame(self.notebook)
        self.notebook.add(article_tab, text="Artículos")

        # Treeview para mostrar los artículos
        article_tree = ttk.Treeview(article_tab, columns=('Title', 'Date', 'Text', 'User ID', 'Tag IDs', 'Category IDs'), show='headings')
        article_tree.heading('Title', text='Título')
        article_tree.heading('Date', text='Fecha')
        article_tree.heading('Text', text='Texto')
        article_tree.heading('User ID', text='ID de Usuario')
        article_tree.heading('Tag IDs', text='ID de Etiquetas')
        article_tree.heading('Category IDs', text='ID de Categorías')
        article_tree.pack(fill='both', expand=True)

        # Cuadros de entrada para agregar artículos
        self.article_title_entry = tk.Entry(article_tab)
        self.article_title_entry.pack()
        self.article_data_entry = tk.Entry(article_tab)
        self.article_data_entry.pack()
        self.article_text_entry = tk.Entry(article_tab)
        self.article_text_entry.pack()
        self.comment_username_entry = tk.Entry(article_tab)
        self.comment_username_entry.pack()

        # Botones para CRUD de artículos
        add_article_button = tk.Button(article_tab, text="Agregar Artículo", command=self.add_article)
        add_article_button.pack(side=tk.LEFT)

        delete_article_button = tk.Button(article_tab, text="Eliminar Artículo", command=self.delete_article)
        delete_article_button.pack(side=tk.LEFT)


    def add_user(self):
        # Obtener datos de los cuadros de entrada
        name = self.user_name_entry.get()
        email = self.user_email_entry.get()

        # Operación CREATE: Agregar un nuevo usuario a la base de datos
        try:
            if name and email:
                user_data = {"name": name, "email": email}
                self.users_collection.insert_one(user_data)
                print("Usuario creado exitosamente.")

                # Recargar datos y actualizar el Treeview
                self.reload_user_data()
            else:
                print("Se requiere nombre y correo electrónico.")
        except (ConnectionError, OperationFailure) as e:
            print(f"Error al agregar usuario a la base de datos: {e}")

    def read_users(self):
        try:
            return list(self.users_collection.find())
        except (ConnectionError, OperationFailure) as e:
            print(f"Error al leer usuarios de la base de datos: {e}")
            return []

    def delete_user(self):
        # Obtener el nombre del usuario a eliminar
        name = self.user_name_entry.get()

        # Operación DELETE: Eliminar un usuario por nombre
        try:
            if name:
                user_to_delete = {"name": name}
                self.users_collection.delete_one(user_to_delete)
                print("Usuario eliminado exitosamente.")

                # Recargar datos y actualizar el Treeview
                self.reload_user_data()
            else:
                print("Se requiere el nombre del usuario.")
        except (ConnectionError, OperationFailure) as e:
            print(f"Error al eliminar usuario de la base de datos: {e}")

    def reload_user_data(self):
        # Limpiar el Treeview
        for item in self.user_tree.get_children():
            self.user_tree.delete(item)

        # Cargar datos de la base de datos
        users = self.read_users()
        for user in users:
            self.user_tree.insert('', 'end', values=(user['name'], user['email']))

    def add_comment(self):
        # Obtener datos de los cuadros de entrada
        name = self.comment_name_entry.get()
        url = self.comment_url_entry.get()
        # Operación CREATE: Agregar un nuevo comentario a la base de datos
        if name and url:
            comment_data = {"name": name, "url": url}
            self.comments_collection.insert_one(comment_data)
            print("Comment created successfully.")
        else:
            print("Name and URL are required.")

    def read_comments(self):
        try:
            return list(self.comments_collection.find())
        except (ConnectionError, OperationFailure) as e:
            print(f"Error al leer comentarios de la base de datos: {e}")
            return []

    def delete_comment(self, name):
        # Operación DELETE: Eliminar un comentario por nombre
        try:
            if name:
                comment_to_delete = {"name": name}
                self.comments_collection.delete_one(comment_to_delete)
                print("Comentario eliminado exitosamente.")
            else:
                print("Se requiere el nombre del comentario.")
        except (ConnectionError, OperationFailure) as e:
            print(f"Error al eliminar comentario de la base de datos: {e}")

    def add_category(self):
        # Obtener datos de los cuadros de entrada
        name = self.category_name_entry.get()
        url = self.category_url_entry.get()
        # Operación CREATE: Agregar una nueva categoría a la base de datos
        if name and url:
            category_data = {"name": name, "url": url}
            self.categories_collection.insert_one(category_data)
            print("Category created successfully.")
        else:
            print("Name and URL are required.")

    def read_categories(self):
        try:
            return list(self.categories_collection.find())
        except (ConnectionError, OperationFailure) as e:
            print(f"Error al leer categorías de la base de datos: {e}")
            return []

    def delete_category(self, name):
        # Operación DELETE: Eliminar una categoría por nombre
        try:
            if name:
                category_to_delete = {"name": name}
                self.categories_collection.delete_one(category_to_delete)
                print("Categoría eliminada exitosamente.")
            else:
                print("Se requiere el nombre de la categoría.")
        except (ConnectionError, OperationFailure) as e:
            print(f"Error al eliminar categoría dela base de datos: {e}")

    def add_article(self):
        # Obtener datos de los cuadros de entrada
        title = self.article_title_entry.get()
        data = self.article_data_entry.get()
        text = self.article_text_entry.get()
        nombreDeUsuario = self.comment_username_entry.get()
        usuario = next((user for user in self.read_users() if user['name'] == nombreDeUsuario), None)
        # Obtener el ID del usuario basado en su nombre
        IDusuario = ""
        if usuario:
            IDusuario = usuario['_id']
        else:
            print(f"Usuario con nombre '{nombreDeUsuario}' no encontrado.")
        # Operación CREATE: Agregar un nuevo artículo a la base de datos
        if title and data and text:
            article_data = {"title": title, "data": data, "text": text, "UserID": IDusuario}
            self.articles_collection.insert_one(article_data)
            print("Article created successfully.")
        else:
            print("Title, data, and text are required.")

    def read_articles(self):
        try:
            return list(self.articles_collection.find())
        except (ConnectionError, OperationFailure) as e:
            print(f"Error al leer artículos de la base de datos: {e}")
            return []

    def delete_article(self, title):
        # Operación DELETE: Eliminar un artículo por título
        try:
            if title:
                article_to_delete = {"title": title}
                self.articles_collection.delete_one(article_to_delete)
                print("Artículo eliminado exitosamente.")
            else:
                print("Se requiere el título del artículo.")
        except (ConnectionError, OperationFailure) as e:
            print(f"Error al eliminar artículo de la base de datos: {e}")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = BlogApp(root)
        root.geometry("800x600")
        root.mainloop()
    except ConnectionError as e:
        print(f"Error de conexión a la base de datos: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")