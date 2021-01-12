#!/usr/bin/env python3
# Integration tests for QA-12

import uuid

from integrate import TestCase, test
from calc2 import result_handler, cleanup_handler
from lib.db import connect_db
from lib.calc import OPERATORS, calculate

class Test(TestCase):
    "AVG QA-12 integration tests"

    @test()
    def db_interaction_test(self, check):
        "Database interacation test"
        operation = "45,-,27"
        result_code = 0
        DATABASE = connect_db()

        cleanup_handler()

        result_raw, result_code, result_error = calculate(operation)
        result = str(result_raw)
        result_id = uuid.uuid4()
        cursor = DATABASE.cursor()
        cursor.execute('INSERT INTO results VALUES (?,?,?)', (result_id.bytes, operation, result_raw))
        DATABASE.commit()

        cursor.execute("SELECT id, operation, result FROM results where id=?;", (result_id.bytes,))
        raw_fetch = cursor.fetchall()[0]
        check.equal(tuple(raw_fetch), (result_id.bytes, operation, int(result)))
#        APP = Flask(__name__)
#        check.equal(result_handler(result_id),
#             true)
#            render_template(
#                "result.html",
#                operation = operation,
#                result = result,
#                result_code = result_code,
#                result_id = result_id))
