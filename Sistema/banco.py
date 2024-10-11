import sqlite3

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('consultas.db')
c = conn.cursor()

# Criar tabela de pacientes
c.execute('''
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT,
        telefone TEXT
    )
''')

# Criar tabela de consultas
c.execute('''
    CREATE TABLE IF NOT EXISTS consultas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        hora TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'agendada',
        FOREIGN KEY (paciente_id) REFERENCES pacientes (id) ON DELETE CASCADE
    )
''')

conn.commit()
conn.close()

print("Banco de dados criado com sucesso!")
