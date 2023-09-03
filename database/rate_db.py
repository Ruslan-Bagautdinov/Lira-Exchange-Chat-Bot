import sqlite3


def sql_start():
    global base, cursor
    base = sqlite3.connect('rates.db')
    cursor = base.cursor()
    if base:
        print('Data_base connection: OK')
    cursor.execute("CREATE TABLE IF NOT EXISTS rates (city TEXT, rate REAL)")
    base.commit()


def read_rate(city):
    cursor.execute("SELECT rate FROM rates WHERE city = ?", (city,))
    result = cursor.fetchone()
    if result:
        return float(result[0])
    else:
        return None


def change_rate(city, new_rate):
    if city == 'Алания':
        config_var_name = 'ALANYA'
    else:
        config_var_name = 'ANTALYA'

    cursor.execute("UPDATE rates SET rate = ? WHERE city = ?", (new_rate, config_var_name))
    base.commit()