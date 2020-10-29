import psycopg2


def connect(host='localhost', user='postgres', password='coderslab',
            dbname='workshop', port='5432'):
    connection = psycopg2.connect(host=host, port=port, user=user,
                                  password=password, dbname=dbname)
    connection.autocommit = True
    return connection


if __name__ == "__main__":
    connection = connect()
    connection.close()
