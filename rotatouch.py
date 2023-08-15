from py_functions import *

db_connect, db_cursor = db_connecting("user_data")

have_old_user_data = db_table_check_exists(db_cursor, 'ts_hosts')

if have_old_user_data == 1:
    old_ts_host = return_data_from_table(db_cursor, 'ts_hosts')
    old_test_user = return_data_from_table(db_cursor, 'test_users')

    ts_host = input(f"URL тестового хоста\nПри пустом вводе используется {old_ts_host} ") or old_ts_host
    test_user = input(f"Пользователь, которого нужно вернуть\nПри пустом вводе используется {old_test_user} ") or old_test_user

    delete_data_from_table(db_cursor, db_connect, "ts_hosts")
    delete_data_from_table(db_cursor, db_connect, "test_users")
else: 
    ts_host = input(f"URL тестового хоста: ")
    test_user = input(f"Пользователь, которого нужно вернуть: ")

create_table_if_not_exists(db_cursor, db_connect, "ts_hosts", "ts_name TEXT")
create_table_if_not_exists(db_cursor, db_connect, "test_users", "test_user TEXT")

insert_into_table_column(db_cursor, db_connect, "ts_hosts", ts_host)
insert_into_table_column(db_cursor, db_connect, "test_users", test_user)

shell_command_run_text_return(f"curl -X POST -utest:test http://10.0.1.240:3000/api/delete_user_reserve/{ts_host}/regRuHardUsers/{test_user}")
response = shell_command_run_text_return(f"curl -X GET -utest:test http://10.0.1.240:3000/api/free_users/{ts_host}")

if test_user in response: 
    print('Пользователь откинулся')
else:
    print('Что-то пошло не так - вернуть пользователя не удалось')



### Работа с контейнерами.

# docker_container_name = subprocess.run("docker ps -f 'name=^autotests_selenoid-tests_run' --format '{{.Names}}'", shell=True, capture_output=True, text=True)

# if docker_container_name.stdout:
#     connect = sqlite3.connect("user_data.db")
#     cursor = connect.cursor()

#     cursor.execute("SELECT EXISTS (SELECT name FROM sqlite_schema WHERE type='table' AND name='is_kill_container')")
#     have_old_user_data = cursor.fetchone()[0]

#     if have_old_user_data == 1:
#         cursor.execute("SELECT * FROM is_kill_container")
#         old_is_kill_container = cursor.fetchone()[0]

#         is_kill_container = input(f"Убить контейнеры:\n{docker_container_name.stdout}(да/нет)\n'{old_is_kill_container}' при пустом вводе. ") or old_is_kill_container

#         cursor.execute("DELETE FROM is_kill_container") 
#         connect.commit()  
#     else:
#         is_kill_container = input(f"Убить контейнеры: {docker_container_name.stdout} (да/нет)? ")

#     if is_kill_container.lower() == 'да':
#         subprocess.run("docker stop $(docker ps -f 'name=^autotests_selenoid-tests_run' --format '{{.Names}}')", shell=True, capture_output=True, text=True)

#         dead_container_check = subprocess.run("docker ps -f 'name=^autotests_selenoid-tests_run' --format '{{.Names}}'", shell=True, capture_output=True, text=True)

#         if "autotests_selenoid-tests_run" in dead_container_check.stdout:
#             print(f"По неизвестной причине остановить контейнеры {docker_container_name.stdout} не удалось") 
#         else:
#             print(f"Контейнеры {docker_container_name.stdout} остановлены") 
#     else: 
#         print(f'Контейнеры {docker_container_name.stdout} отстанутся неприкосновенными')  
        
#     cursor.execute("CREATE TABLE IF NOT EXISTS is_kill_container( ts_name TEXT );")
#     connect.commit()
#     cursor.execute("INSERT INTO is_kill_container VALUES(?);", [is_kill_container])
#     connect.commit()


