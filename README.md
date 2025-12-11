# Biblioteca Compartilhada

## Objetivo do Sistema

O sistema **Biblioteca Compartilhada** tem como objetivo incentivar o compartilhamento de livros por meio de armários físicos controlados digitalmente. Usuários podem doar, emprestar e devolver livros, acumulando ou gastando moedas virtuais como recompensa ou penalidade. O sistema promove o acesso à leitura e a circulação de livros na comunidade.

---

## Funcionamento do Sistema

- **Interface Web/Mobile:** Usuários acessam via navegador.
- **Cadastro/Login:** Acesso mediante autenticação segura.
- **Visualização de Livros:** Lista de livros disponíveis para empréstimo.
- **Doação de Livros:** Usuários cadastram livros e acumulam moedas.
- **Empréstimo e Devolução:** Registro de transações, controle de prazos e penalidades por atraso.
- **Controle de Armários:** Abertura dos armários apenas após autenticação.
- **Sistema de Moedas:** Moedas são acumuladas por doações e empréstimos de livros doados, e descontadas em caso de atraso na devolução.

---

## Requisitos Funcionais

- **RF01:** Cadastro e login de usuário.
- **RF02:** Controle de saldo de moedas por usuário.
- **RF03:** Liberação dos armários apenas após login.
- **RF04:** Cadastro de livros doados pelos usuários.
- **RF05:** Registro de empréstimos e devoluções.
- **RF06:** Aplicação de penalidades por atraso.
- **RF07:** Premiação de usuários por empréstimos dos seus livros doados.
- **RF08:** Premiação de usuários ao doar livros para o armário.
- **RF09:** Listagem de livros disponíveis para aluguel.
- **RF10:** Notificação das interações do usuário com o sistema.

---

## Requisitos Não Funcionais

- **RNF01:** Disponibilidade 24/7.
- **RNF02:** Interface responsiva e acessível via navegador.
- **RNF03:** Segurança dos dados dos usuários com autenticação segura.
- **RNF04:** Escalabilidade para grande número de usuários simultâneos.

---

## Estrutura do Projeto

```
biblioteca_compartilhada/
├── backend/                # API, lógica de negócio
│   ├── src/
│       ├── app.py
│       ├── extensions.py
├── diagrama/               # Modelagem do sistema com diagrama de Caso de Uso
├── frontend/               # Interface Web
│   ├── css/
│   ├── js/
│   ├── index.html
│   └── login.html
├── instance/               
│   ├── biblioteca.db       # Banco de Dados
├── venv                    # Ambiente virtual
├── videos/                 # Vídeos de demonstração
├── main.py                
├── README.md               # Este arquivo
├── requirements.txt
```

---

## Como Contribuir

1. Faça um fork do projeto.
2. Crie uma branch para sua feature (`git checkout -b feature/nome-da-feature`).
3. Commit suas alterações (`git commit -m 'feat: nova feature'`).
4. Faça push para a branch (`git push origin feature/nome-da-feature`).
5. Abra um Pull Request.

---

