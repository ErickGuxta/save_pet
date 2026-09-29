# Save Pet

Sistema web desenvolvido com Django para gerenciamento de tutores, pets, registros de vacinação e artigos informativos.

## Funcionalidades

- Cadastro, login e logout de usuários.
- Perfil de tutor com dados pessoais e endereço.
- Cadastro, listagem, edição, detalhe e exclusão de pets.
- Upload de foto para o cadastro do pet.
- Registro de vacinas por pet, com data de aplicação e reforço.
- Dashboard para tutores com resumo de pets, vacinas e artigos recentes.
- Dashboard administrativo com indicadores gerais do sistema.
- Controle de editores do blog por grupo.
- Blog com artigos e categorias gerenciados por editores do blog.

## Tecnologias

- Python
- Django
- SQLite
- HTML
- CSS
- Bootstrap

## Estrutura do projeto

```text
save_pet/
├── _apps/
│   ├── accounts/   # Cadastro, autenticação, perfil e permissões
│   ├── blog/       # Artigos e categorias
│   ├── pets/       # Cadastro e gestão de pets
│   └── vaccines/   # Registros de vacinação
├── save_pet/       # Configurações principais do Django
├── static/         # Arquivos CSS e imagens estáticas
├── templates/      # Templates HTML
├── manage.py
└── README.md
```

## Como rodar localmente

### 1. Clone o repositório

```bash
git clone <url-do-repositorio>
cd save_pet
```

### 2. Crie e ative um ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate
```

No Windows:

```bash
.venv\Scripts\activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Execute as migrações

```bash
python manage.py migrate
```

### 5. Configure o acesso administrativo

Crie um usuário e marque `is_staff=True` para ele conseguir acessar o painel `/admin/`.
Não é necessário usar `is_superuser=True` no uso normal do sistema.

Depois, pelo painel `/admin/`, crie e configure os grupos:

- `Dono de pet`
- `Editor do blog`
- `Administrador do sistema`

Se precisar fazer o primeiro usuário administrativo sem superuser, use o shell apenas para marcar esse usuário como staff:

```python
from django.contrib.auth.models import User

user = User.objects.get(username="seu_usuario")
user.is_staff = True
user.is_superuser = False
user.save(update_fields=["is_staff", "is_superuser"])
```

### 6. Inicie o servidor

```bash
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/
```

## Rotas principais

- `/` redireciona para a listagem de pets.
- `/accounts/` área de conta, login, cadastro e dashboard.
- `/pets/` gestão de pets.
- `/vaccines/` gestão de vacinas.
- `/blog/` artigos informativos.
- `/admin/` painel administrativo do Django.

## Permissões

O sistema usa permissões e grupos do Django por funcionalidade. As permissões devem ser configuradas pelo painel `/admin/` do Django. O código da aplicação não cria nem sincroniza grupos automaticamente.

Grupos esperados:

- `Dono de pet`: pode visualizar, criar, editar e excluir pets e registros de vacina, além de visualizar artigos do blog.
- `Editor do blog`: pode visualizar, criar, editar e excluir categorias e artigos do blog.
- `Administrador do sistema`: pode acessar o dashboard administrativo, a tela simples de editores do blog e o painel `/admin/` para manutenção sensível.

Use a tela `Editores do blog` da aplicação apenas para conceder ou remover o grupo `Editor do blog` de contas comuns. Para permissões detalhadas, contas `staff`, exclusão de usuários e grupos administrativos, use o painel `/admin/` do Django.

## Comandos úteis

Criar novas migrações:

```bash
python manage.py makemigrations
```

Aplicar migrações:

```bash
python manage.py migrate
```

Rodar testes:

```bash
python manage.py test
```

Coletar arquivos estáticos:

```bash
python manage.py collectstatic
```

## Observações

- O banco padrão configurado é SQLite.
- Os arquivos enviados pelos usuários são armazenados em `media/`.
- A aplicação está configurada em português do Brasil.
- As configurações atuais usam `DEBUG=True` e não devem ser usadas em produção sem ajustes de segurança.
