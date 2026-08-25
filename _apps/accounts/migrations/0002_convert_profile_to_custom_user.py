from django.db import migrations


def convert_profile_to_custom_user(apps, schema_editor):
    connection = schema_editor.connection

    if connection.vendor != "sqlite":
        return

    table_names = connection.introspection.table_names()
    if "accounts_usuario" not in table_names or "auth_user" not in table_names:
        return

    with connection.cursor() as cursor:
        columns = {
            column.name
            for column in connection.introspection.get_table_description(
                cursor,
                "accounts_usuario",
            )
        }

        if "username" in columns:
            return

        cursor.execute(
            """
            CREATE TABLE accounts_usuario_new (
                id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                password varchar(128) NOT NULL,
                last_login datetime NULL,
                is_superuser bool NOT NULL,
                username varchar(150) NOT NULL UNIQUE,
                first_name varchar(150) NOT NULL,
                last_name varchar(150) NOT NULL,
                email varchar(254) NOT NULL,
                is_staff bool NOT NULL,
                is_active bool NOT NULL,
                date_joined datetime NOT NULL,
                cpf varchar(14) NULL UNIQUE,
                telefone varchar(20) NOT NULL,
                cep varchar(9) NOT NULL,
                logradouro varchar(150) NOT NULL,
                numero varchar(20) NOT NULL,
                complemento varchar(100) NOT NULL,
                bairro varchar(100) NOT NULL,
                cidade varchar(100) NOT NULL,
                estado varchar(2) NOT NULL
            )
            """
        )
        cursor.execute(
            """
            INSERT INTO accounts_usuario_new (
                id,
                password,
                last_login,
                is_superuser,
                username,
                first_name,
                last_name,
                email,
                is_staff,
                is_active,
                date_joined,
                cpf,
                telefone,
                cep,
                logradouro,
                numero,
                complemento,
                bairro,
                cidade,
                estado
            )
            SELECT
                auth_user.id,
                auth_user.password,
                auth_user.last_login,
                auth_user.is_superuser,
                auth_user.username,
                auth_user.first_name,
                auth_user.last_name,
                auth_user.email,
                auth_user.is_staff,
                auth_user.is_active,
                auth_user.date_joined,
                accounts_usuario.cpf,
                COALESCE(accounts_usuario.telefone, ''),
                COALESCE(accounts_usuario.cep, ''),
                COALESCE(accounts_usuario.logradouro, ''),
                COALESCE(accounts_usuario.numero, ''),
                COALESCE(accounts_usuario.complemento, ''),
                COALESCE(accounts_usuario.bairro, ''),
                COALESCE(accounts_usuario.cidade, ''),
                COALESCE(accounts_usuario.estado, '')
            FROM auth_user
            LEFT JOIN accounts_usuario ON accounts_usuario.user_id = auth_user.id
            """
        )
        cursor.execute("DROP TABLE accounts_usuario")
        cursor.execute("ALTER TABLE accounts_usuario_new RENAME TO accounts_usuario")

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS accounts_usuario_groups (
                id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                usuario_id bigint NOT NULL REFERENCES accounts_usuario (id) DEFERRABLE INITIALLY DEFERRED,
                group_id integer NOT NULL REFERENCES auth_group (id) DEFERRABLE INITIALLY DEFERRED
            )
            """
        )
        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS accounts_usuario_groups_usuario_id_group_id_uniq
            ON accounts_usuario_groups (usuario_id, group_id)
            """
        )
        cursor.execute(
            """
            INSERT OR IGNORE INTO accounts_usuario_groups (usuario_id, group_id)
            SELECT user_id, group_id FROM auth_user_groups
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS accounts_usuario_user_permissions (
                id integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                usuario_id bigint NOT NULL REFERENCES accounts_usuario (id) DEFERRABLE INITIALLY DEFERRED,
                permission_id integer NOT NULL REFERENCES auth_permission (id) DEFERRABLE INITIALLY DEFERRED
            )
            """
        )
        cursor.execute(
            """
            CREATE UNIQUE INDEX IF NOT EXISTS accounts_usuario_user_permissions_usuario_id_permission_id_uniq
            ON accounts_usuario_user_permissions (usuario_id, permission_id)
            """
        )
        cursor.execute(
            """
            INSERT OR IGNORE INTO accounts_usuario_user_permissions (usuario_id, permission_id)
            SELECT user_id, permission_id FROM auth_user_user_permissions
            """
        )


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(convert_profile_to_custom_user, migrations.RunPython.noop),
    ]
