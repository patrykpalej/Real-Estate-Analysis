def generate_psql_connection_string(user, password, host, port, db):
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"
