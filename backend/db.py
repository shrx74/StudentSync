from database.connection import Database


def query(sql, values=(), many=False):
    with Database.connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, values)

            if cursor.description is None:
                return None

            columns = [col.name for col in cursor.description]

            if many:
                rows = cursor.fetchall()
                return [dict(zip(columns, row)) for row in rows]

            row = cursor.fetchone()

            if row is None:
                return None

            return dict(zip(columns, row))


def execute(sql, values=()):
    with Database.connect() as connection:
        with connection.cursor() as cursor:
            cursor.execute(sql, values)
            return cursor.rowcount