#!/usr/bin/env python3
import re
import uuid

#from flask import Flask, request, jsonify, render_template
from flask import Flask, request, render_template

from lib.db import connect_db
from lib.calc import OPERATORS, calculate


## Global constants
# Flask app
APP = Flask(__name__)

DATABASE = connect_db()

DESCRIPTION = """
Сомнительный калькулятор® 2.0

В строку ниже вводится операция для подсчета

Формат ввода: NUM1,OPERATOR,NUM2

Поддерживаемые операторы:
{}

Пример строки ввода:
1,+,2

В системе есть ограничение на хранение результатов в 100 результатов. Если вы получили ошибку, то почистите базу данных нажатием на соответствующую кнопку ниже
""".format(','.join(OPERATORS.keys()))

## Handlers
@APP.route('/', methods=['GET'])
def root_handler():
    return render_template(
        "root.html",
        DESCRIPTION=DESCRIPTION)

@APP.route('/calc', methods=['POST'])
def calc_handler():
    # Predefined vars
    result = "deadbeef"
    result_code = 0
    result_id = "deadbeef"

    # Get POST params
    operation = request.form['operation']

    if not re.match(r'^-?[0-9]\d*(\.\d+)?,.+,-?[0-9]\d*(\.\d+)?$', operation):
        result_code = 1
        result = "Некорректный ввод"
    else:
        result_raw, result_code, result_error = calculate(operation)
        if result_code == 0:
            result = str(result_raw)
            # Check if database has less than 100 records
            cursor = DATABASE.cursor()
            cursor.execute('SELECT COUNT(*) FROM results')
            current_results = cursor.fetchone()
            if current_results[0] < 100:
                # Add database result addition
                # Most compact way to store https://wtanaka.com/node/8106
                result_id = uuid.uuid4()
                cursor.execute('INSERT INTO results VALUES (?,?,?)', (result_id.bytes, operation, result_raw))
                DATABASE.commit()
            else:
                result_code = 2
                result = "Превышено количество хранимых результатов расчетов"
        else:
            result = result_error

    return render_template(
        "result.html",
        operation = operation,
        result = result,
        result_code = result_code,
        result_id = result_id)

@APP.route('/result/<result_id>', methods=['GET'])
def result_handler(result_id):
    # Predefined vars
    operation = "deadbeef"
    result = "deadbeef"

    # Get operation, result from database
    cursor = DATABASE.cursor()

    #result_id_uuid = uuid.UUID('{%s}' % result_id)
    #cursor.execute("SELECT id, operation, result FROM results where id=?;", (result_id_uuid.bytes,))
    cursor.execute('SELECT id, operation, result FROM results')
    #raw_fetch = cursor.fetchall()[0]
    raw_fetch = cursor.fetchall()

    for single_result in raw_fetch:
        if result_id == str(uuid.UUID(bytes = single_result[0])):
            operation, result = single_result[1], single_result[2]
            break

    if raw_fetch is None or result == 'deadbeef':
        return "Result {} not found".format(result_id), 404

    else:
        #_, operation, result = raw_fetch

        return render_template(
            "result.html",
            operation = operation,
            result = result,
            result_code = 0,
            result_id = result_id)

@APP.route('/results_secret', methods=['GET'])
def results_secret_handler():
    cursor = DATABASE.cursor()
    cursor.execute('SELECT * FROM results')
    raw_fetch = cursor.fetchall()

    operations = [(str(uuid.UUID(bytes=op[0])), op[1], op[2]) for op in raw_fetch]

    return render_template(
            "results_secret.html",
            operations = operations
            )

@APP.route('/cleanup', methods=['POST'])
def cleanup_handler():
    # Delete all records from database
    cursor = DATABASE.cursor()
    cursor.execute('DELETE FROM results')
    DATABASE.commit()

    return "Database cleared"

## Main function
if __name__ == '__main__':
    # Run app
    APP.run()
