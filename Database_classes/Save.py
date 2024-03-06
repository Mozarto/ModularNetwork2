import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def create_tables():
    # conectando...
    conn = create_connection('modular_network.db')
    # definindo um cursor
    cursor = conn.cursor()

    # criando a tabela (schema)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lineages (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            n_individuals INTEGER,
            n_receptors INTEGER,
            zoom INTEGER,
            gen_time INTEGER,
            map_size INTEGER,
            food_timer INTEGER,
            food_density INTEGER,
            generation INTEGER
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS individuals (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            id_lin INTEGER NOT NULL,
            origin INTEGER NOT NULL,
            lineage INTEGER NOT NULL,
            score INTEGER,
            distance_travelled REAL,
            generation INTEGER,
            FOREIGN KEY (lineage) REFERENCES lineages(id)
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS neurons (
            id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            id_ind TEXT NOT_NULL,
            individual INTEGER NOT NULL,
            first_neuron INTEGER,
            to_neuron TEXT,
            threshold REAL,
            to_depolarization_rate TEXT,
            repolarization INTEGER,
            to_depolarization TEXT,     
            FOREIGN KEY (individual) REFERENCES individuals(id)
    );
    """)

    # cursor.execute("""
    # DROP TABLE lineages;
    # """)
    print('Tabelas criadas com sucesso.')

    # desconectando...
    conn.close()


def insert_lineage(values, db):
    # conectando...

    conn = create_connection(db)
    # definindo um cursor
    cur = conn.cursor()

    cur.execute(f"""
    INSERT INTO lineages (name, n_individuals, n_receptors, zoom, gen_time, map_size, food_timer, food_density)
    VALUES ('{values["name"]}', {values["n_individuals"]}, {values["n_receptors"]},
     {values["zoom"]}, {values["gen_time"]}, {values["map_size"]}, {values["food_timer"]}, {values["food_density"]})
    """)

    # gravando no bd
    conn.commit()

    # desconectando...
    #cur.close()
    conn.close()


def insert_individuals(values, db):
    # conectando...
    conn = create_connection(db)
    # definindo um cursor
    cur = conn.cursor()

    cur.execute(f"""
    INSERT INTO individuals (id_lin, origin, lineage, score, distance_travelled, generation)
    VALUES ({values["id_lin"]}, {values["origin"]}, {values["lineage"]}, {values["score"]}, {values["distance_travelled"]}, {values["generation"]})
    """)

    # gravando no bd
    conn.commit()

    # desconectando...
    #cur.close()
    conn.close()



def insert_neuron(values, db):
    # conectando...
    conn = create_connection(db)
    # definindo um cursor
    cur = conn.cursor()
    #print([i for i in values.values()])
    cur.execute(f"""
    INSERT INTO neurons (id_ind, individual, first_neuron, to_neuron, threshold, to_depolarization_rate, repolarization, to_depolarization)
    VALUES ('{values["id_ind"]}', {values["individual"]}, {values["first_neuron"]}, '{values["to_neuron"]}', {values["threshold"]},
    '{values["to_depolarization_rate"]}', {values["repolarization"]}, '{values["to_depolarization"]}')
    """)

    # gravando no bd
    conn.commit()

    # desconectando...
    #cur.close()
    conn.close()

#create_tables()


