import os
import mysql.connector
from mysql.connector import Error

def insert_data_in_bulk(df_joined, table_name='clientes', second_table_name="pqrs"):
    connection = None
    cursor = None

    try:
        #Esto despuès se debe enmascarar con os.getenv
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="telepizza"
        )

        if connection.is_connected():
            cursor = connection.cursor()

            data_clients = df_joined[['NombreCompleto', 'Sexo', 'Edad', 'Ciudad']].values.tolist()

          
            data_pqrs = df_joined[['Tipo', 'ClienteFk', 'FechaCaso', 'Asunto', 'Estado', 'FechaCierre', 'Urgencia']].values.tolist()

            # # Prepare the insert query
            insert_query = f"""
            INSERT INTO {table_name} (NombreCompleto, Sexo, Edad, Ciudad)
            VALUES (%s, %s, %s, %s)
            """
        
            # Execute the insert query in bulk
            cursor.executemany(insert_query, data_clients)

            insert_query_2 = f"""
            INSERT INTO {second_table_name} (Tipo, ClienteFk, FechaCaso, Asunto, Estado, FechaCierre, Urgencia)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            cursor.executemany(insert_query_2, data_pqrs)
            
             # Convert DataFrame to list of tuples
            imported_data = df_joined.to_records(index=False).tolist()

            # Commit the transaction
            connection.commit()

            print(f"{cursor.rowcount} rows inserted successfully.")

    except Error as e:
        print(f"Error: {e}")
        if connection:
            connection.rollback()

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

# Example usage
# Assuming df is the DataFrame you want to insert:
# insert_clients_in_bulk(df)
