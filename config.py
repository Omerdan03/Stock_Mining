class sql_conf:
    host = 'localhost'
    user = 'root'
    password = ''

    @staticmethod
    def get_connection_info():
        return sql_conf.host, sql_conf.user, sql_conf.password


db_name = 'stocks_db'

api_key = ''