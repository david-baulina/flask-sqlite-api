from app.models.model import Model
import json

class DB(Model):
    def __init__(self):
        super().__init__()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                salary INTEGER NOT NULL,
                country TEXT NOT NULL,
                skills TEXT NOT NULL
            )
            ''')

    def create_job(self, job):
        if isinstance(job, str):
            job = json.loads(job)
        skills = json.dumps(job["skills"])
        job.pop('skills', None)
        job['skills'] = skills
        columns = ', '.join(job.keys())  
        placeholders = ', '.join(['?'] * len(job))  
        values = tuple(job.values())  
        sql = f'INSERT INTO jobs ({columns}) VALUES ({placeholders})'

        try:
            self.cursor.execute(sql, values)
            self.database.commit()
            print(f"Datos insertados correctamente en la tabla. ID: {self.cursor.lastrowid}")
            return self.cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Error al insertar datos: {e}")
            return None
        finally:
            self.database.close()

    def search_job(self, request):
        """
        Consulta una base de datos SQLite basada en campos opcionales.

        :param db_name: Nombre de la base de datos SQLite.
        :param name: (opcional) Nombre a buscar.
        :param salary: (opcional) Salario a buscar.
        :param country: (opcional) País a buscar.
        :param skills: (opcional) Lista de habilidades a buscar (como una cadena delimitada por comas).
        :return: Lista de filas que coinciden con los criterios.
        """
        print("REQUEST", request)
        # Base de la consulta
        query = "SELECT * FROM jobs WHERE 1=1"
        params = []

        # Agregar filtros opcionales
        if "name" in request:
            query += " AND name = ?"
            params.append(request["name"])
        if "salary" in request:
            query += " AND salary = ?"
            params.append(request["salary"])
        if "country" in request:
            query += " AND country = ?"
            params.append(request["country"])
        if "skills" in request:
            query += " AND skills LIKE ?"
            params.append(request["skills"])  # Busca habilidades de forma parcial

        try:
            # Ejecutar la consulta
            self.cursor.execute(query, tuple(params))
            results = self.cursor.fetchall()
            return results
        except sqlite3.Error as e:
            print(f"Error al consultar la base de datos: {e}")
            return None
        finally:
            # Cerrar conexión
            self.database.close()
