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
- Controle de permissões para administradores do sistema.
- Blog com artigos e categorias gerenciados por administradores.

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

### 5. Crie um superusuário

```bash
python manage.py createsuperuser
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

O sistema diferencia usuários comuns e administradores.

Usuários administradores são identificados por:

- `is_staff=True`
- `is_superuser=True`
- participação no grupo `Administrador do sistema`

Administradores podem visualizar dados gerais do sistema, gerenciar permissões de usuários, categorias e artigos do blog.

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
