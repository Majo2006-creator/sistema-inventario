import os

class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def to_line(self):
        return f"{self.id_producto},{self.nombre},{self.cantidad},{self.precio}"

    @staticmethod
    def from_line(linea):
        datos = linea.strip().split(",")
        return Producto(int(datos[0]), datos[1], int(datos[2]), float(datos[3]))


class Inventario:
    def __init__(self, archivo="inventario.txt"):
        self.archivo = archivo
        self.productos = []
        self.cargar_desde_archivo()

    def cargar_desde_archivo(self):
        try:
            if not os.path.exists(self.archivo):
                open(self.archivo, "w").close()
                print("Archivo creado correctamente.")
                return

            with open(self.archivo, "r") as f:
                for linea in f:
                    if linea.strip():
                        producto = Producto.from_line(linea)
                        self.productos.append(producto)

            print("Inventario cargado correctamente.")

        except FileNotFoundError:
            print("Error: Archivo no encontrado.")
        except PermissionError:
            print("Error: Sin permisos para leer el archivo.")
        except Exception as e:
            print("Error inesperado:", e)

    def guardar_en_archivo(self):
        try:
            with open(self.archivo, "w") as f:
                for producto in self.productos:
                    f.write(producto.to_line() + "\n")
            print("Cambios guardados en el archivo.")

        except PermissionError:
            print("Error: Sin permisos para escribir en el archivo.")
        except Exception as e:
            print("Error inesperado:", e)

    def agregar_producto(self, producto):
        self.productos.append(producto)
        self.guardar_en_archivo()
        print("Producto agregado exitosamente.")

    def eliminar_producto(self, id_producto):
        for producto in self.productos:
            if producto.id_producto == id_producto:
                self.productos.remove(producto)
                self.guardar_en_archivo()
                print("Producto eliminado exitosamente.")
                return
        print("Producto no encontrado.")

    def actualizar_producto(self, id_producto, cantidad, precio):
        for producto in self.productos:
            if producto.id_producto == id_producto:
                producto.cantidad = cantidad
                producto.precio = precio
                self.guardar_en_archivo()
                print("Producto actualizado exitosamente.")
                return
        print("Producto no encontrado.")

    def mostrar_inventario(self):
        if not self.productos:
            print("Inventario vacío.")
        else:
            for p in self.productos:
                print(f"ID: {p.id_producto} | Nombre: {p.nombre} | "
                      f"Cantidad: {p.cantidad} | Precio: ${p.precio:.2f}")


def menu():
    inventario = Inventario()

    while True:
        print("\n--- SISTEMA DE INVENTARIO ---")
        print("1. Agregar producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Mostrar inventario")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            try:
                id_producto = int(input("ID: "))
                nombre = input("Nombre: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
                inventario.agregar_producto(
                    Producto(id_producto, nombre, cantidad, precio)
                )
            except ValueError:
                print("Error: Datos inválidos.")

        elif opcion == "2":
            try:
                id_producto = int(input("ID a eliminar: "))
                inventario.eliminar_producto(id_producto)
            except ValueError:
                print("ID inválido.")

        elif opcion == "3":
            try:
                id_producto = int(input("ID a actualizar: "))
                cantidad = int(input("Nueva cantidad: "))
                precio = float(input("Nuevo precio: "))
                inventario.actualizar_producto(id_producto, cantidad, precio)
            except ValueError:
                print("Datos inválidos.")

        elif opcion == "4":
            inventario.mostrar_inventario()

        elif opcion == "5":
            print("Saliendo...")
            break

        else:
            print("Opción inválida.")


if __name__ == "__main__":
    menu()
