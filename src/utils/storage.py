def generate_psql_connection_string(user, password, host, port, db):
    print("1")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"
