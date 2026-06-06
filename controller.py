import pandas as pd
import os

class SupermercadoController:
    def __init__(self, modelo):
        self.modelo = modelo

    def autenticar_usuario(self, email, password):
        return self.modelo.verificar_credenciales(email, password)

    def registrar_nuevo_usuario(self, email, password, nombre):
        return self.modelo.registrar_usuario(email, password, nombre)

    def obtener_lista_productos_maestro(self, usuario_id):
        return self.modelo.obtener_productos_maestro(usuario_id)

    def crear_producto_maestro(self, usuario_id, nombre, sector_id):
        return self.modelo.insertar_producto_maestro(usuario_id, nombre, sector_id)

    def obtener_recetas_catalogo(self, usuario_id):
        return self.modelo.obtener_recetas(usuario_id)

    def obtener_ingredientes_receta(self, receta_id):
        return self.modelo.obtener_ingredientes_receta(receta_id)

    def crear_receta_completa(self, usuario_id, nombre_receta, lista_ingredientes):
        return self.modelo.insertar_receta_completa(usuario_id, nombre_receta, lista_ingredientes)

    def obtener_compras_activas(self, usuario_id):
        return self.modelo.obtener_compras_activas(usuario_id)

    def agregar_a_lista(self, usuario_id, producto, cantidad, unidad, observaciones):
        self.modelo.insertar_compra(usuario_id, producto, cantidad, unidad, observaciones)

    def borrar_compra(self, compra_id, usuario_id):
        self.modelo.eliminar_compra(compra_id, usuario_id)

    def procesar_cierre_y_exportacion(self, usuario_id, sectores_dict):
        registros = self.modelo.obtener_compras_activas(usuario_id)
        if not registros:
            return False, "La lista se encuentra vacía."
        
        datos_limpios = []
        for reg in registros:
            compra_id, fecha, sector_id, prod_name, cant, unidad, obs = reg
            datos_limpios.append({
                "Pasillo": sectores_dict.get(sector_id, "Sin Sector"),
                "Producto": prod_name.capitalize(),
                "Cantidad": cant,
                "Unidad": unidad,
                "Notas": obs if obs else ""
            })
        
        df = pd.DataFrame(datos_limpios)
        csv_data = df.to_csv(index=False, encoding='utf-8-sig')
        self.modelo.vaciar_lista_compras(usuario_id)
        return True, csv_data