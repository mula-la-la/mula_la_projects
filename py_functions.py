import sqlite3
import subprocess

def db_connecting (db_name: str):
    """
    Создает подключение к БД и функции для работы с ней.

    Args:
         db_name: Название создаваемой БД.
    """
    connect = sqlite3.connect(f"{db_name}.db")
    cursor = connect.cursor()

    return connect, cursor

def db_table_check_exists(db_cursor: object, table_name: str):
    """
    Проверяет наличие таблицы в БД.

    Args:
        db_cursor: Объект для запросов к БД.
        table_name: Название проверяемой таблицы.
    """
    db_cursor.execute(f"SELECT EXISTS (SELECT name FROM sqlite_schema WHERE type='table' AND name='{table_name}')")
    have_old_user_data = db_cursor.fetchone()[0]   

    return have_old_user_data

def return_data_from_table(db_cursor: object, table_name: str):
    """
    Возвращает данные из таблицы.

    Args:
        db_cursor: Объект для запросов к БД.
        table_name: Название таблицы.
    """
    db_cursor.execute(f"SELECT * FROM {table_name}")
    table_data = db_cursor.fetchone()[0]

    return table_data

def delete_data_from_table(db_cursor: object, db_connect: object, table_name: str):
    """
    Удаляет данные из таблицы.

    Args:
        db_cursor: Объект для запросов к БД.
        db_connect: Объект для соединения с БД.
        table_name: Название таблицы.
    """
    db_cursor.execute(f"DELETE FROM {table_name}")
    db_connect.commit()
    
def create_table_if_not_exists(db_cursor: object, db_connect: object, table_name: str, table_column: str):
    """
    Создает новую таблицу, если не найдена существующая. 

    Args:
        db_cursor: Объект для запросов к БД.
        db_connect: Объект для соединения с БД.
        table_name: Название таблицы.
        table_column: Поля таблицы с типами данных.
    """
    db_cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name}( {table_column} );")
    db_connect.commit()

def insert_into_table_column(db_cursor: object, db_connect: object, table_name: str, column_value: str):  
    """
    Добавляет записи в таблицу. 

    Args:
        db_cursor: Объект для запросов к БД.
        db_connect: Объект для соединения с БД.
        table_name: Название таблицы.
        column_value: Записи для полей таблицы.
    """
    db_cursor.execute(f"INSERT INTO {table_name} VALUES(?);", [column_value])
    db_connect.commit()

def shell_command_run_text_return(shell_command: str):
    """
    Выполняет команду в консоли и возвращает результат. 

    Args:
        shell_command: Команда для выполнение в консоли. 
    """
    command_result = subprocess.run(shell_command, shell=True, capture_output=True, text=True)

    return command_result.stdout
