from typing import Union


class Vehiculo:

    def __init__(self, sku: str,   modelo: str, marca: str, cilindraje: int, precio_unitario: float, descripcion: str,
                 id_vendedor: str, cantidad: int):

        self.sku: str = sku
        self.modelo: str = modelo
        self.marca: str = marca
        self.cilindraje: int = cilindraje
        self.precio_unitario: float = precio_unitario
        self.descripcion: str = descripcion
        self.id_vendedor: str = id_vendedor
        self.cantidad: int = cantidad

    def __str__(self):
        formato_impresion="|{0:<20}|{1:>15}|{2:>15}|{3:>18}|{4:>22}|"
        return formato_impresion.format(self.sku, self.modelo, self.marca, self.precio_unitario, self.cantidad)

    def descontar_unidades_disponibles(self, cantidad) -> int:
        self.cantidad -= cantidad
        return self.cantidad



class MotoNueva(Vehiculo):

    def __init__(self, sku: str, modelo: str, marca: str, cilindraje: int, precio_unitario: float, descripcion: str,
                 id_vendedor: str, cantidad: int):
        super().__init__(sku, modelo, marca, cilindraje, precio_unitario, descripcion, id_vendedor, cantidad)

    def hay_cantidad_unidades_disponibles(self, cantidad) -> bool:
        return self.cantidad >= cantidad


class MotoUsada(Vehiculo):

    def __init__(self, sku: str, placa: str, modelo: str, marca: str, cilindraje: int, precio_unitario: float,
                 descripcion: str, id_vendedor, cantidad: int = 1):
        super().__init__(sku, modelo, marca, cilindraje, precio_unitario, descripcion, id_vendedor, cantidad)

        self.placa: str = placa

class Item:

    def __init__(self, codigo, moto, cantidad: int):
        self.codigo: int = codigo
        self.moto: Union[MotoUsada, MotoNueva] = moto
        self.cantidad = cantidad
        self.valor_total_item = self.moto.precio_unitario * self.cantidad

    def __str__(self):
        formato_impresion = "|{0:<10}|{1:>5}--{2:>0}--{3:>5}--{4:>5}|{5:>10}|{6:>22}|"
        return formato_impresion.format(self.codigo, self.moto.sku, self.moto.modelo, self.moto.marca,
                                        self.moto.precio_unitario, self.cantidad, self.valor_total_item)

    def calcular_total(self) -> float:
        valor_total_item = self.moto.precio_unitario * self.cantidad
        return valor_total_item


class Carrito:

    def __init__(self):
        self.items: dict[int, Item] = {}
        self.total_carrito = 0

    def agregar_item(self, moto, cantidad):
        codigo = len(self.items) + 1
        item = Item(codigo, moto, cantidad)
        self.items[codigo] = item

    def calcular_total(self) -> float:
        for item in self.items.values():
            valor_total_item = item.calcular_total()
            self.total_carrito += valor_total_item
            return self.total_carrito

    def eliminar_item(self, codigo):
        if self.hay_items():
            item = self.buscar_item_por_codigo(codigo)
            if item is not None:
                del self.items[codigo]
            else:
                return -3
        else:
            return -2

    def hay_items(self) -> bool:
        return len(self.items) > 0

    def buscar_item_por_codigo(self, codigo) -> Union[Item, None]:
        if codigo in self.items.keys():
            return self.items[codigo]

        else:
            return None

    def comprar(self):
        for item in self.items.values():
            item.moto.descontar_unidades_disponibles(item.cantidad)

class MiCatalogo:

    def __init__(self):
        self.mi_catalogo: dict[str, Vehiculo] = {}
        self.mis_ventas: list[Union[MotoUsada, MotoNueva]] = []
        self.valor_total_ventas: float = 0

    def agregar_moto(self, moto):
        self.mi_catalogo[moto.sku] = moto

    def agregar_venta(self, info_venta):
        self.valor_total_ventas += info_venta[3]
        self.mis_ventas.append(info_venta)

    def eliminar_moto(self, moto):
        del self.mi_catalogo[moto.sku]


class Usuario:

    def __init__(self, id: str, nombre: str, celular: str):
        self.id: str = id
        self.nombre: str = nombre
        self.celular: str = celular

        self.mi_catalogo: MiCatalogo = MiCatalogo()
        self.carrito: Carrito = Carrito()
        self.total_ventas_acumuladas: float = 0

    def __str__(self):
        return f"el usuario {self.id} se llama {self.nombre}"

    def agregar_moto_a_mi_catalogo(self, moto):
        self.mi_catalogo.agregar_moto(moto)

    def agregar_moto_a_mi_carrito(self, moto, cantidad):
        self.carrito.agregar_item( moto, cantidad)

    def eliminar_moto_de_carrito(self, codigo):
        self.carrito.eliminar_item(codigo)

    def agregar_venta_catalogo_vendedor(self, info_venta):
        self.mi_catalogo.agregar_venta( info_venta)

    def eliminar_moto_mi_catalogo(self, moto):
        self.mi_catalogo.eliminar_moto(moto)

    def comprar_carrito(self):
        self.carrito.comprar()


class Compraventa:

    def __init__(self):

        self.usuarios: dict[str, Usuario] = {}
        self.catalogo_global: dict[str, Union[MotoUsada, MotoNueva]] = {}
        self.catalogo_vendedores: dict[str, Union[MotoUsada, MotoNueva]] = {}

        self.filtrado_nuevas: dict[str, MotoNueva] = {}
        self.filtrado_usadas: dict[str, MotoUsada] = {}
        self.detalles_compra: dict[int, Item] = {}

        self.total_ventas: float = 0

    def registrar_usuario(self, id, nombre, celular) -> bool:

        if self.buscar_usuario_por_id(id) is None:
            usuario = Usuario(id, nombre, celular)
            self.usuarios[id] = usuario
            return True
        else:
            return False

    def buscar_usuario_por_id(self, id) -> Union[Usuario, None]:

        if id in self.usuarios.keys():
            return self.usuarios[id]

        else:
            return None

    def buscar_moto_por_sku(self, sku) -> Union[MotoUsada, MotoNueva, None]:

        if sku in self.catalogo_global.keys():
            return self.catalogo_global[sku]

        else:
            return None

    def registrar_moto_usada(self, id, sku, placa, modelo, marca, cilindraje, precio_unitario, descripcion,
                             id_vendedor, cantidad: int = 1):

        if self.buscar_moto_por_sku(sku) is None:
            moto = MotoUsada(sku, placa, modelo, marca, cilindraje, precio_unitario, descripcion, id_vendedor, cantidad)
            self.catalogo_global[sku] = moto
            self.catalogo_vendedores[id_vendedor] = moto
            if self.buscar_usuario_por_id(id) is not None:
                usuario = self.buscar_usuario_por_id(id)
                usuario.agregar_moto_a_mi_catalogo(moto)
            else:
                return -2

        else:
            return -1

        return 0

    def registrar_moto_nueva(self, id, sku, modelo, marca, cilindraje, precio_unitario, descripcion,
                             id_vendedor, cantidad):

        if self.buscar_moto_por_sku(sku) is None:
            moto = MotoNueva(sku, modelo, marca, cilindraje, precio_unitario, descripcion, id_vendedor, cantidad)
            self.catalogo_global[sku] = moto
            self.catalogo_vendedores[id_vendedor] = moto
            if self.buscar_usuario_por_id(id) is not None:
                usuario = self.buscar_usuario_por_id(id)
                usuario.agregar_moto_a_mi_catalogo(moto)
            else:
                return -2

        else:
            return -1

        return 0

    def filtrar_busqueda_por_categoria(self, categoria) -> Union[dict, int]:

        if categoria == 1:
            for sku, values in self.catalogo_global.items():
                if sku.startswith("NU"):
                    self.filtrado_nuevas[sku] = values
                    return self.filtrado_nuevas

        elif categoria == 2:
            for sku, values in self.catalogo_global.items():
                if sku.startswith("US"):
                    self.filtrado_usadas[sku] = values
                    return self.filtrado_usadas

        else:
            return -1

    def agregar_moto_a_carrito(self, sku, cantidad, id):

        moto = self.buscar_moto_por_sku(sku)
        if moto is not None:
            if sku.startswith("NU"):
                if moto.hay_cantidad_unidades_disponibles(cantidad):
                    if sku.startswith("US") or moto.hay_cantidad_unidades_disponibles(cantidad) is True:
                        if self.buscar_usuario_por_id(id) is not None:
                            usuario = self.buscar_usuario_por_id(id)
                            usuario. agregar_moto_a_mi_carrito(moto, cantidad)


                        else:
                            return -3
                else:
                    return -2

        else:
            return -1

        return 0

    def eliminar_item_de_carrito(self, id, codigo):

        usuario = self.buscar_usuario_por_id(id)
        if usuario is not None:
            usuario.eliminar_moto_de_carrito(codigo)

        else:
            return -1

        return 0

    def comprar_carrito(self, id):
        usuario = self.buscar_usuario_por_id(id)
        if usuario is not None:
            if usuario.carrito.hay_items():
                total_carrito = usuario.carrito.calcular_total()
                self.total_ventas += total_carrito
                self.mostrar_detalles_de_la_compra(id)
                for item in usuario.carrito.items.values():
                    id_vendedor = item.moto.id_vendedor
                    total_venta = item.moto.cantidad * item.moto.precio_unitario
                    info_venta = [item.moto.sku, item.moto.modelo, item.moto.cantidad, total_venta]
                    self.agregar_venta_catalogo_vendedor(id_vendedor, info_venta)
                    usuario.carrito.comprar()
                    for moto in self.catalogo_global.values():
                        if moto.cantidad == 0:
                            self.eliminar_moto_catalogo_vendedor(moto)
                            del self.catalogo_global[moto.sku]
            usuario.carrito.items.clear()

        else:
            return -1

        return 0

    def eliminar_moto_catalogo_vendedor(self, moto):
        usuario = self.buscar_usuario_por_id(moto.id_vendedor)
        if usuario is not None:
            usuario.eliminar_moto_mi_catalogo(moto)

    def mostrar_detalles_de_la_compra(self, id) -> Union[dict, int]:
        usuario = self.buscar_usuario_por_id(id)
        if usuario is not None:
            if usuario.carrito.hay_items():
                for codigo, item in usuario.carrito.items.items():
                    self.detalles_compra[codigo] = item
                return self.detalles_compra

            else:
                return -2

    def agregar_venta_catalogo_vendedor(self, id_vendedor, info_venta):
        usuario = self.buscar_usuario_por_id(id_vendedor)
        if usuario is not None:
            usuario.agregar_venta_catalogo_vendedor(info_venta)

    def mostrar_carrito(self, id) -> Union[dict, int]:
        usuario = self.buscar_usuario_por_id(id)
        if usuario is not None:
            return usuario.carrito.items

        else:
            return -1

    def mostrar_mis_ventas(self, id) -> Union[list, int]:
        usuario = self.buscar_usuario_por_id(id)
        if usuario is not None:
            return usuario.mi_catalogo.mis_ventas

        else:
            return -1

    def mostrar_mi_catalogo(self, id) -> Union[dict, int]:
        usuario = self.buscar_usuario_por_id(id)
        if usuario is not None:
            return usuario.mi_catalogo.mi_catalogo

        else:
            return -1















                










