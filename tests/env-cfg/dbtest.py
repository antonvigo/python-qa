#!/usr/bin/env python3
# This module is just for studying only!

import uuid

from calc2 import result_handler, cleanup_handler
from lib.db import connect_db
from lib.calc import OPERATORS, calculate

## Main function
if __name__ == '__main__':
    result_id = 'a103f175-be61-4252-986c-08f1369b5287'
    result_id_uuid = uuid.UUID('{%s}' % result_id)

    operation = "45,-,27"
    result_code = 0
    DATABASE = connect_db()

#        result_raw, result_code, result_error = calculate(operation)
#        result = str(result_raw)
#        result_id = uuid.uuid4()
    cursor = DATABASE.cursor()
#    cursor.execute("SELECT id, operation, result FROM results where id=?;", (result_id_uuid.bytes,))
    cursor.execute("SELECT id, operation, result FROM results")
    for i in cursor.fetchall():
        if result_id == str(uuid.UUID(bytes=i[0])):
            print(i[1], i[2])
