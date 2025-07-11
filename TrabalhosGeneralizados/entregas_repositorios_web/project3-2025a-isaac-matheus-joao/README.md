# Projeto Django - Autenticação com Usuários Pré-Cadastrados

Este é um projeto simples em Django que implementa um sistema de autenticação com tela de login, logout seguro via POST, e dois usuários criados automaticamente.

![Screenshot do Site](projeto_lutadores/staticfiles/screenshot_typesouls.jpg "Screenshot do projeto")

### Desenvolvedores
Matheus - Sistemas de Informação

João Marcos - Sistemas de Informação

Isaac - Sistemas para internet

#### Tecnologias
-HTML

-CSS

-Python

-Django

#### Ambiente de desenvolvimento
-VS Code

-Pixlr(Para criação da logo)

#### Referências e créditos
-ChatGPT(Auxílio no desenvolvimente e criação de algumas imagens)

##  Requisitos

- Python 3.10 ou superior
- Django 5.2.1
- Ambiente virtual (recomendado)

##  Como rodar o projeto

1. **Clone ou extraia o projeto em uma pasta**
2. **Abra o terminal na pasta do projeto**
3. **Crie o ambiente virtual** (caso ainda não tenha):
   ```bash
   py -m venv venv
   ```
4. **Ative o ambiente virtual**:

   - PowerShell:
     ```bash
     .\venv\Scripts\Activate.ps1
     ```

   - CMD:
     ```bash
     .\venv\Scripts\activate
     ```

5. **Instale o Django**:
   ```bash
   pip install django
   ```

6. **Rode as migrações**:
   ```bash
   py manage.py migrate
   ```

7. **Crie os usuários automaticamente**:
   ```bash
   py criar_usuarios.py
   ```

8. **Inicie o servidor**:
   ```bash
   py manage.py runserver
   ```

9. **Acesse o sistema**:
   - [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/)

## 👤 Usuários cadastrados

| Usuário     | Senha     |
|-------------|-----------|
| johnwik25   | nerdgeek  |
| manolo123   | qwe123    |

##  Segurança

- O logout é feito via formulário `POST` com CSRF token.
- Não é permitido logout via método GET.
- Login obrigatório para acessar a página principal (`/`).

##  Estrutura básica

```
projeto_lutadores_login/
├── app_lutadores/
│   └── views.py, urls.py, apps.py
├── projeto_lutadores_login/
│   └── settings.py, urls.py
├── templates/
│   └── base.html, home.html, login.html
├── criar_usuarios.py
├── manage.py
```

##  Observações

- O Django Admin está disponível em `/admin/`, mas requer criação de superusuário (`createsuperuser`).
- O projeto usa SQLite por padrão.

---
Projeto entregue para a disciplina de [Desenvolvimento de Software para a Web](http://github.com/andreainfufsm/elc1090-2025a) em 2025a
