# main.py
from backend.src.app import create_app
from backend.src.extensions import db
from backend.src.models.entities import Usuario, Livro, Emprestimo, Notificacao
from backend.src.factories.object_factory import ObjectFactory
import bcrypt
import os

# Crie a instância do aplicativo
app = create_app()

def seed_database(app):
    """
    Função para popular o banco de dados com dados iniciais.
    """
    with app.app_context():
        db.create_all()
        print("Banco de dados criado/atualizado (biblioteca.db).")
        
        # Verifica se já existem usuários para evitar adicionar duplicatas em cada reinício
        if not Usuario.query.first():
            print("Populando o banco de dados com dados iniciais...")
            object_factory = ObjectFactory()

            # Gerar o hash da senha padrão
            hashed_password = bcrypt.hashpw('senha123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Adicionar usuários iniciais, agora passando a senha E O EMAIL
            usuario1 = object_factory.create_usuario("Alice Silva", "alice123", senha=hashed_password, email="alice@example.com", saldo_moedas=500)
            usuario2 = object_factory.create_usuario("Bob Souza", "bob456", senha=hashed_password, email="bob@example.com", saldo_moedas=200)
            usuario3 = object_factory.create_usuario("Charlie Santos", "charlie789", senha=hashed_password, email="charlie@example.com", saldo_moedas=100)
            usuario4 = object_factory.create_usuario("David Lima", "david101", senha=hashed_password, email="david@example.com", saldo_moedas=300)
            usuario5 = object_factory.create_usuario("Eva Costa", "eva202", senha=hashed_password, email="eva@example.com", saldo_moedas=400)

            db.session.add(usuario1)
            db.session.add(usuario2)
            db.session.add(usuario3)
            db.session.add(usuario4)
            db.session.add(usuario5)
            db.session.commit()

            # Adicionar livros iniciais
            livro1 = object_factory.create_livro(
                "O diário de Anne Frank", "Anne Frank", "978-8501044457", 1995, "alice123"
            )
            livro2 = object_factory.create_livro(
                "O menino do pijama listrado", "John Boyne", "978-8535911121", 2007, "bob456"
            )
            livro3 = object_factory.create_livro(
                "A menina que roubava livros", "Markus Zusak", "978-8598078175", 2013, "alice123"
            )
            livro4 = object_factory.create_livro(
                "A Biblioteca da Meia-Noite", "Matt Haig", "978-6558380542", 2021, "charlie789"
            )
            livro5 = object_factory.create_livro(
                "Harry Potter e a Pedra Filosofal", "J.K. Rowling", "9788532511010", 2015, "david101"
            )
            livro6 = object_factory.create_livro(
                "Dom Casmurro", "Machado de Assis", "0520007905", 1966, "eva202"
            )
            livro7 = object_factory.create_livro(
                "O Senhor dos Anéis: A Sociedade do Anel", "J.R.R. Tolkien", "978-8595084759", 2019, "eva202"
            )
            livro8 = object_factory.create_livro(
                "1984", "George Orwell", "978-6555522266", 2021, "eva202"
            )
            livro9 = object_factory.create_livro(
                "A garota do lago", "Charlie Donlea", "978-8562409882", 2017, "eva202"
            )
            livro10 = object_factory.create_livro(
                "Harry Potter e o Prisioneiro de Azkaban", "J. K. Rowling", "9789722365611", 2020, "eva202"
            )
            

            db.session.add(livro1)
            db.session.add(livro2)
            db.session.add(livro3)
            db.session.add(livro4)
            db.session.add(livro5)
            db.session.add(livro6)
            db.session.add(livro7)
            db.session.add(livro8)
            db.session.add(livro9)
            db.session.add(livro10)
            db.session.commit()

            print("Banco de dados populado com sucesso!")
        else:
            print("O banco de dados já está populado. Ignorando o seeding.")

if __name__ == '__main__':
    seed_database(app)
    print("Iniciando o servidor Flask...")
    print("Acesse: http://127.0.0.1:5000/")
    app.run(debug=True, port=5000)