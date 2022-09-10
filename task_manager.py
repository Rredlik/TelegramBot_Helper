import psycopg2
from config import host, user, password, db_name

from time import gmtime, strftime


def db_manipulations(operation):
    try:
        db_connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        db_connection.autocommit = True
        # формфактор + message.from_user.id
        task_table_name = 'task_table_' + operation[1]
        # cursor = connection.cursor()

        if operation[0] == "create_new_user":

            time_now = strftime("%Y-%m-%d %H:%M:%S", gmtime())

            # 1) Таблица пользователя:
            # название: user_id(телеграмный),
            # поля: номер пользователя(id, в моей таблице), имя пользователя, дата регистрации
            with db_connection.cursor() as cursor:
                cursor.execute(
                    f"""CREATE TABLE {task_table_name}(
                                        id serial PRIMARY KEY,
                                        task varchar(100) NOT NULL,
                                        is_completed BOOLEAN DEFAULT FALSE);
                            INSERT INTO users(id, nick_name, registration_date) VALUES
                                        ('{operation[1]}', '{operation[2]}', '{time_now}');"""
                )
                print(f"[DB info] User {operation[2]} {operation[1]} data created")

        elif operation[0] == "insert_data":

            with db_connection.cursor() as cursor:
                cursor.execute(
                    f"""INSERT INTO {task_table_name}(task) VALUES
                        ('{operation[2]}');"""
                )
                print(f'[DB info] User {operation[1]} data inserted')

        elif operation[0] == "print_data":
            tasks_message = []
            with db_connection.cursor() as cursor:
                cursor.execute(
                    f"""SELECT * FROM {task_table_name};"""
                )
                print(f'[DB info] User {operation[1]} data printed')
                tasks = cursor.fetchall()
                return tasks

        elif operation[0] == "delete_data":

            with db_connection.cursor() as cursor:
                cursor.execute(
                    f"""DELETE FROM {task_table_name} WHERE id='{operation[2]}';
                        SELECT * FROM {task_table_name};"""
                )
                print(f'[DB info] User {operation[1]} data deleted')
                tasks = cursor.fetchall()
                return tasks


    except Exception as _ex:
        print(f"[DB error] Error for user {operation[1]}:", _ex)
    finally:
        if db_connection:
            # cursor.close()
            db_connection.close()
            print("[DB info] Connection closed")



# Изменение значений в бд
# UPDATE users SET user_coins = user_coins + 10 WHERE id = 351931465;

# Добавление полей в бд заданий
# INSERT INTO task_table_351931465 (task) VALUES ('task');

# Удалить пользователя из главной базы
# delete FROM users WHERE nick_name='Skidikis';

# Удалить личную бд пользователя
# DROP TABLE task_table_351931465;


# Добавление нового столбца в бд
# ALTER TABLE users
# ADD user_small_box bigint;

# Установиит дефолт значение новому столбцу
# ALTER TABLE users
# ALTER  user_small_box SET DEFAULT 0;





