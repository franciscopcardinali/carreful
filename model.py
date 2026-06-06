import sqlite3
import hashlib
import os
from datetime import datetime

class ProductoModel:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self._SALT = "Carrefull_Salt_Secure_2026_#"
        self.inicializar_tablas()

    def _conectar(self):
        return sqlite3.connect(self.db_path)

    def _generar_hash(self, password):
        input_string = password + self._SALT
        return hashlib.sha256(input_string.encode('utf-8')).hexdigest()

    def inicializar_tablas(self):
        with self._conectar() as conn:
            cursor = conn.cursor()
            
            # Tabla de Usuarios Autorizados
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                nombre TEXT NOT NULL
            )
            """)
            
            # Catálogo Maestro por Usuario
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos_maestro (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                nombre TEXT NOT NULL,
                sector_id INTEGER NOT NULL,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                UNIQUE(usuario_id, nombre)
            )
            """)
            
            # Recetas por Usuario
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS recetas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                nombre TEXT NOT NULL,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id),
                UNIQUE(usuario_id, nombre)
            )
            """)
            
            # Ingredientes de Recetas
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingredientes_receta (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                recipe_id INTEGER NOT NULL,
                producto_nombre TEXT NOT NULL,
                cantidad REAL NOT NULL,
                unidad TEXT NOT NULL,
                FOREIGN KEY(recipe_id) REFERENCES recetas(id) ON DELETE CASCADE
            )
            """)
            
            # Compras Activas por Usuario
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS compras_activas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                fecha TEXT NOT NULL,
                producto_nombre TEXT NOT NULL,
                cantidad REAL NOT NULL,
                unidad TEXT NOT NULL,
                observaciones TEXT,
                FOREIGN KEY(usuario_id) REFERENCES usuarios(id)
            )
            """)
            
            conn.commit()
            self._crear_usuarios_por_defecto()

    def _crear_usuarios_por_defecto(self):
        # Alta automática de cuentas autorizadas fijas
        usuarios_iniciales = [
            ("francisco@carrefull.com", "admin123", "Francisco"),
            ("mujer@carrefull.com", "mujer123", "Mi Mujer")
        ]
        with self._conectar() as conn:
            cursor = conn.cursor()
            for email, password, nombre in usuarios_iniciales:
                hash_p = self._generar_hash(password)
                try:
                    cursor.execute("INSERT INTO usuarios (email, password_hash, nombre) VALUES (?, ?, ?)",
                                   (email, hash_p, nombre))
                except sqlite3.IntegrityError:
                    pass
            conn.commit()

    def verificar_credenciales(self, email, password):
        hash_p = self._generar_hash(password)
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, email, nombre FROM usuarios WHERE email = ? AND password_hash = ?", 
                           (email.strip().lower(), hash_p))
            res = cursor.fetchone()
            if res:
                return {"id": res[0], "email": res[1], "nombre": res[2]}
            return None

    def registrar_usuario(self, email, password, nombre):
        hash_p = self._generar_hash(password)
        with self._conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO usuarios (email, password_hash, nombre) VALUES (?, ?, ?)", 
                               (email.strip().lower(), hash_p, nombre))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def obtener_productos_maestro(self, usuario_id):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT nombre, sector_id FROM productos_maestro WHERE usuario_id = ? ORDER BY nombre ASC", (usuario_id,))
            return cursor.fetchall()

    def insertar_producto_maestro(self, usuario_id, nombre, sector_id):
        with self._conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO productos_maestro (usuario_id, nombre, sector_id) VALUES (?, ?, ?)", 
                               (usuario_id, nombre.strip().lower(), sector_id))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def obtener_recetas(self, usuario_id):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre FROM recetas WHERE usuario_id = ? ORDER BY nombre ASC", (usuario_id,))
            return cursor.fetchall()

    def insertar_receta_completa(self, usuario_id, nombre_receta, lista_ingredientes):
        with self._conectar() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO recetas (usuario_id, nombre) VALUES (?, ?)", (usuario_id, nombre_receta.strip().lower()))
                receta_id = cursor.lastrowid
                for ing in lista_ingredientes:
                    cursor.execute("INSERT INTO ingredientes_receta (recipe_id, producto_nombre, cantidad, unidad) VALUES (?, ?, ?, ?)",
                                   (receta_id, ing[0], ing[1], ing[2]))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False

    def obtener_ingredientes_receta(self, receta_id):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT producto_nombre, cantidad, unidad FROM ingredientes_receta WHERE recipe_id = ?", (receta_id,))
            return cursor.fetchall()

    def obtener_compras_activas(self, usuario_id):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT c.id, c.fecha, IFNULL(m.sector_id, 99) as sector, c.producto_nombre, c.cantidad, c.unidad, c.observaciones
            FROM compras_activas c
            LEFT JOIN productos_maestro m ON c.usuario_id = m.usuario_id AND LOWER(c.producto_nombre) = LOWER(m.nombre)
            WHERE c.usuario_id = ?
            ORDER BY sector ASC, c.producto_nombre ASC
            """, (usuario_id,))
            return cursor.fetchall()

    def insertar_compra(self, usuario_id, producto, cantidad, unidad, observaciones):
        with self._conectar() as conn:
            cursor = conn.cursor()
            fecha_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute("""
            INSERT INTO compras_activas (usuario_id, fecha, producto_nombre, cantidad, unidad, observaciones)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (usuario_id, fecha_str, producto.strip().lower(), cantidad, unidad, observaciones))
            conn.commit()

    def eliminar_compra(self, compra_id, usuario_id):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM compras_activas WHERE id = ? AND usuario_id = ?", (compra_id, usuario_id))
            conn.commit()

    def vaciar_lista_compras(self, usuario_id):
        with self._conectar() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM compras_activas WHERE usuario_id = ?", (usuario_id,))
            conn.commit()