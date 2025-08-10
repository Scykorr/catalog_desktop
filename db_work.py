import sqlite3


def select_db_info(sql_request):
    conn = sqlite3.connect('desktop.db')
    cursor = conn.cursor()

    cursor.execute(sql_request)

    rows = cursor.fetchall()
    conn.close()
    return rows


def create_view():
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()
    cursor.execute('''
                   CREATE VIEW IF NOT EXISTS vvst_view AS
                   SELECT p.id,
                          p.predmet_inn,
                          p.predmet_oboznachenie,
                          p.predmet_name,
                          n.nops_number
                   FROM catapp_predmetsnabzeniavvst p
                            JOIN catapp_nopsvvst n ON p.nops_vvst_id = n.id
                   ''')
    conn.commit()
    conn.close()


def create_new_db():
    result_info_list = list()
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute(
        f"SELECT nops_vvst_id, predmet_inn, predmet_oboznachenie, predmet_name from catapp_predmetsnabzeniavvst")

    unit_list = cursor.fetchall()
    for row_index in range(len(unit_list)):
        # add group_number, class_number, sfo_number, nops_number, fnn(inn), oboznachenie_ps, name_ps
        nops_id = unit_list[row_index][0]
        cursor.execute(f"SELECT nops_number, nops_name, nops_description, sfo_vvst_id from catapp_nopsvvst WHERE id = {nops_id}")
        nops_info = cursor.fetchall()
        sfo_id = nops_info[0][3]
        cursor.execute(f"SELECT sfo_number, sfo_name, sfo_description, class_vvst_id from catapp_sfovvst WHERE id = {sfo_id}")
        sfo_info = cursor.fetchall()
        class_id = sfo_info[0][3]
        cursor.execute(f"SELECT class_number, class_name, class_description, class_description_include, class_description_exclude, group_vvst_id from catapp_classvvst WHERE id = {class_id}")
        class_info = cursor.fetchall()
        group_id = class_info[0][5]
        cursor.execute(f"SELECT group_number, group_name, group_description, group_description_include, group_description_exclude from catapp_groupvvst WHERE id = {group_id}")
        group_info = cursor.fetchall()
        result_info_list.append(
            [str(group_info[0][0]), group_info[0][1], group_info[0][2], group_info[0][3], group_info[0][4], str(class_info[0][0]), class_info[0][1], class_info[0][2], class_info[0][3], class_info[0][4], sfo_info[0][0], sfo_info[0][1], sfo_info[0][2], nops_info[0][0], nops_info[0][1], nops_info[0][2], unit_list[row_index][1], unit_list[row_index][2], unit_list[row_index][3]])
    conn.close()
    print(result_info_list)
    print(len(result_info_list))
    conn = sqlite3.connect('desktop.db')
    cursor = conn.cursor()

    # Создание таблицы с автоинкрементом (без ключевого слова AUTOINCREMENT)
    cursor.execute("CREATE TABLE IF NOT EXISTS all_ps (id INTEGER PRIMARY KEY, group_number TEXT, group_name TEXT, group_description TEXT, group_description_include TEXT, group_description_exclude TEXT, class_number TEXT, class_name TEXT, class_description TEXT, class_description_include TEXT, class_description_exclude TEXT, sfo_number TEXT, sfo_name TEXT, sfo_description TEXT, nops_number TEXT, nops_name TEXT, nops_description TEXT, predmet_inn TEXT, predmet_oboznachenie TEXT, predmet_name TEXT)")



    cursor.executemany("INSERT INTO all_ps (group_number, "
                       "group_name, "
                       "group_description, "
                       "group_description_include, "
                       "group_description_exclude, "
                       "class_number, "
                       "class_name, "
                       "class_description, "
                       "class_description_include, "
                       "class_description_exclude, "
                       "sfo_number, "
                       "sfo_name, "
                       "sfo_description, "
                       "nops_number, "
                       "nops_name, "
                       "nops_description, "
                       "predmet_inn, "
                       "predmet_oboznachenie, "
                       "predmet_name) "
                       "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                       result_info_list)

    # Проверка данных
    cursor.execute("SELECT * FROM all_ps")
    results = cursor.fetchall()

    print(results)

    conn.commit()
    conn.close()

# def insert_sfo(class_id: int, sfo_description, sfo_name, sfo_number):
#     conn = sqlite3.connect('../db.sqlite3')
#     cursor = conn.cursor()
#     sql_script = f'INSERT INTO catapp_sfovvst (class_vvst_id, sfo_description, sfo_name, sfo_number) VALUES ({class_id}, "{sfo_description}", "{sfo_name}", "{sfo_number}");'
#     print(sql_script)
#     cursor.execute(sql_script)
#
#     conn.commit()
#     conn.close()
#
#
# def insert_nops(nops_description, nops_name, nops_number, sfo_vvst_id: int):
#     conn = sqlite3.connect('../db.sqlite3')
#     cursor = conn.cursor()
#     sql_script = f'INSERT INTO catapp_nopsvvst (nops_description, nops_name, nops_number, sfo_vvst_id) VALUES ("{nops_description}", "{nops_name}", "{nops_number}", {sfo_vvst_id});'
#     print(sql_script)
#     cursor.execute(sql_script)
#
#     conn.commit()
#     conn.close()
#
#
# def delete_from_db():
#     conn = sqlite3.connect('../db.sqlite3')
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM catapp_predmetsnabzeniavvst")
#     # cursor.execute("DELETE FROM catapp_okpo")
#     # cursor.execute("DELETE FROM catapp_okato")
#     # cursor.execute("DELETE FROM catapp_nopsvvst")
#     # cursor.execute("DELETE FROM catapp_sfovvst")
#
#     conn.commit()
#     conn.close()
#
#
# def insert_okato(code_okato, control_num_okato, name_okato, description_okato):
#     conn = sqlite3.connect('../db.sqlite3')
#     cursor = conn.cursor()
#     sql_script = f'INSERT INTO catapp_okato (code_okato, control_num_okato, name_okato, description_okato) VALUES ("{code_okato}", "{control_num_okato}", "{name_okato}", "{description_okato}");'
#     print(sql_script)
#     cursor.execute(sql_script)
#
#     conn.commit()
#     conn.close()
#
#
# def insert_okpo(region_okpo, code_okpo, name_org_okpo, inn_okpo, ogrn_okpo, okogu_okpo, okato_okpo, oktmo_okpo,
#                 okfs_okpo, okopf_okpo):
#     conn = sqlite3.connect('../db.sqlite3')
#     cursor = conn.cursor()
#     sql_script = f"INSERT INTO catapp_okpo (region_okpo, code_okpo, name_org_okpo, inn_okpo, ogrn_okpo, okogu_okpo, okato_okpo, oktmo_okpo, okfs_okpo, okopf_okpo) VALUES ('{region_okpo}', '{code_okpo}', '{name_org_okpo}', '{inn_okpo}', '{ogrn_okpo}', '{okogu_okpo}', '{okato_okpo}', '{oktmo_okpo}', '{okfs_okpo}', '{okopf_okpo}');"
#     print(sql_script)
#     cursor.execute(sql_script)
#
#     conn.commit()
#     conn.close()
#
#
# def insert_predmetsnabz(nops_id_vvst, predmet_inn, predmet_name, predmet_oboznachenie, predmet_status, format_vvst_id):
#     conn = sqlite3.connect('../db.sqlite3')
#     cursor = conn.cursor()
#     sql_script = f"INSERT INTO catapp_predmetsnabzeniavvst (nops_vvst_id, predmet_inn, predmet_name, predmet_oboznachenie, predmet_status, format_vvst_id) VALUES ({nops_id_vvst}, '{predmet_inn}', '{predmet_name}', '{predmet_oboznachenie}', '{predmet_status}', {format_vvst_id});"
#     print(sql_script)
#     cursor.execute(sql_script)
#
#     conn.commit()
#     conn.close()
#
#
# sfo_id_sql = select_db_info(f"SELECT * from catapp_sfovvst WHERE sfo_number='{'0002'}'")
# print(sfo_id_sql)