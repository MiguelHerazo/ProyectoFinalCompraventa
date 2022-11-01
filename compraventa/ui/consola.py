from compraventa.mundo.modelo import Compraventa
import sys


class UIConsola:
    def __init__(self):
        self.compraventa = Compraventa()
        self.opciones = {
            "1": self.registrar_usuario,
            "2": self.mostrar_catalogo_global,
            "3": self.filtrar_busqueda_por_categoria,
            "4": self.ver_carrito,
            "5": self.mostrar_informacion_de_moto,
            "6": self.agregar_moto_al_carrito,
            "7": self.eliminar_item_carrito,
            "8": self.comprar_carrito,
            "9": self.ver_mi_catalogo,
            "10": self.registrar_moto,
            "0":  self.salir

        }

    def menu(self):
        print("""
        \n
        ------------Menu de opciones--------------
        Seleccione la opcion que desee ejecutar:
        1. Registrar usuario
        2. Mostrar catalogo de motos disponibles
        3. Filtrar Busqueda por categoria motos: Nuevas y Usadas
        4. Mostrar carrito de compras
        5. Ver mas informacion y detalles de una moto
        6. Agregar moto al carrito de compras
        7. Eliminar item del carrito
        8. Comprar el carrito
        9. Mostrar mi catalogo de motos disponibles a la venta
        10.Registrar moto para vender
        11.Eliminar de mi catalogo moto publicada a la venta 
        0. Salir
        
        ------------------------------------------
        ------------------------------------------
        """)

    def capturar_entero(self, mensaje):
        while True:
            try:
                numero = int(input(f"{mensaje}: "))
                return numero

            except ValueError:
                print("ERROR: debe digitar un numero entero")

            print()

    def capturar_flotante(self, mensaje):
        while True:
            try:
                numero = float(input(f"{mensaje}: "))
                return numero

            except ValueError:
                print("ERROR: debe digitar un numero real")

            print()

    def capturar_cadena_caracteres(self, mensaje):
        while True:
            try:
                cadena = input(f"{mensaje}: ").strip()

                if len(cadena):
                    return cadena
                else:
                    print("MENSAJE: debe ingresar texto para que el mensaje sea valido")

            except ValueError:
                print("ERROR: debe digitar un numero real")

            print()

    def ejecutar(self):
        while True:
            self.menu()
            respuesta: str = input("Seleccione una opcion:")
            opcion = self.opciones.get(respuesta)
            if opcion is None:
                print("La opcion ingresada no es valida, debe ser un numero entre el 1 y 9")
            else:
                opcion()
                if opcion == 1:
                    self.registrar_usuario()

                if opcion == 2:
                    self.mostrar_catalogo_global()



    def registrar_usuario(self):
        print("Registrar usuario")
        id: str = self.capturar_cadena_caracteres("Ingrese su numero de cedula:")
        nombre: str = self.capturar_cadena_caracteres("Ingrese su nombre completo:")
        celular: str = self.capturar_cadena_caracteres("Ingrese su numero de celular:")
        if self.compraventa.registrar_usuario(id, nombre, celular):
            print("El usuario fue registrado correctamente")

        else:
            print(f"ERROR: El usuario con la cedula {id} ya se habia registrado anteriormente")

    def mostrar_catalogo_global(self):

        print("\n Lista de catalogo de motos en venta disponibles" )

        print("\n+--------------------+---------------+---------------+------------------+----------------------+")
        print("   CODIGO SKU        |MODELO         |MARCA          |PRECIO UNITARIO   |UNIDADES DISPONIBLES  ")
        print("+--------------------+---------------+---------------+------------------+----------------------+")

        for moto in self.compraventa.catalogo_global.values():
            print(moto)

        print("+--------------------+---------------+---------------+------------------+----------------------+")

    def filtrar_busqueda_por_categoria(self):
        print("\n Filtrar catalogo por categoria Motos nuevas/Motos usadas")
        categoria: int = self.capturar_entero("\nIngrese:"
                                              "\n1.Para ver el catalogo de solo motos NUEVAS"
                                              "\n2.Para ver el catalogo de solo motos USADAS")

        self.compraventa.filtrar_busqueda_por_categoria(categoria)

        if categoria == 1:
            filtrado_nuevas = self.compraventa.filtrado_nuevas
            if len(filtrado_nuevas) > 0:
                print("este es el catalogo de moto nuevas")
                print("+--------------------+---------------+---------------+------------------+----------------------+")
                print("                             CATALOGO SOLO MOTOS NUEVAS                                         ")
                print("+--------------------+---------------+---------------+------------------+----------------------+")
                print("   CODIGO SKU        |MODELO         |MARCA          |PRECIO UNITARIO   |UNIDADES DISPONIBLES  ")
                print(
                    "+--------------------+---------------+---------------+------------------+----------------------+")

                for moto in filtrado_nuevas.values():
                    print(moto)

                print("+--------------------+---------------+---------------+------------------+----------------------+")

            else:
                print("+--------------------+---------------+---------------+------------------+----------------------+")
                print("   CODIGO SKU          |MODELO         |MARCA          |PRECIO UNITARIO   |UNIDADES DISPONIBLES ")
                print("            |  ACTUALMENTE EL CATALOGO NO TIENE MOTOS NUEVAS DISPONIBLES     |                 ")
                print("+--------------------+---------------+---------------+------------------+----------------------+")

        elif categoria == 2:
            filtrado_usadas = self.compraventa.filtrado_usadas
            if len(filtrado_usadas) > 0:
                print("este es el catalogo de moto usadas")
                print("+--------------------+---------------+---------------+------------------+----------------------+")
                print("                             CATALOGO SOLO MOTOS USADAS                                         ")
                print("+--------------------+---------------+---------------+------------------+----------------------+")
                print("   CODIGO SKU        |MODELO         |MARCA          |PRECIO UNITARIO   |UNIDADES DISPONIBLES  ")
                print("+--------------------+---------------+---------------+------------------+----------------------+")

                for moto in filtrado_usadas.values():
                    print(moto)

                print("+--------------------+---------------+---------------+------------------+----------------------+")

            else:
                print("+--------------------+---------------+---------------+------------------+----------------------+")
                print("   CODIGO SKU          |MODELO         |MARCA          |PRECIO UNITARIO   |UNIDADES DISPONIBLES ")
                print("            |  ACTUALMENTE EL CATALOGO NO TIENE MOTOS USADAS DISPONIBLES     |                 ")
                print("+--------------------+---------------+---------------+------------------+----------------------+")

        else:
            print("ERROR: valor ingresado como categoria no es valido. debe ser un numero entero entre 1 y 2")

    def mostrar_informacion_de_moto(self):
        print("Ver mas informacion de una moto")
        sku: str = self.capturar_cadena_caracteres("Ingrese el codigo sku de la moto que desea ver mas a detalle")
        moto = self.compraventa.buscar_moto_por_sku(sku=sku)
        if moto.sku.startswith("NU"):
            print(f"Detalles de la moto"
                  f"\n-codigo sku: {moto.sku}"
                  f"\n-modelo:{moto.modelo}"
                  f"\n-marca: {moto.marca} "
                  f"\n-cilindraje: {moto.cilindraje}"
                  f"\n-precio: {moto.precio_unitario}"
                  f"\n-Unidades disponibles: {moto.cantidad}"
                  f"\n-descripcion: {moto.descripcion}")

        elif moto.sku.startswith("US"):
            print(f"Detalles de la moto"
                  f"\n-codigo sku: {moto.sku}"
                  f"\n-placa:{moto.placa}"
                  f"\n-modelo:{moto.modelo}"
                  f"\n-marca: {moto.marca} "
                  f"\n-cilindraje: {moto.cilindraje}"
                  f"\n-precio: {moto.precio_unitario}"
                  f"\n-descripcion: {moto.descripcion}")

    def ver_carrito(self):
        print("\nLista carrito de compras actual")
        id: str = self.capturar_cadena_caracteres("Ingrese su numero de cedula:")
        items = self.compraventa.mostrar_carrito(id=id)

        if len(items) > 0:
            print("\n+----------+------------------------------+----------+----------------------+")
            print("  CODIGO   |      INFORMACION MOTO        | CANTIDAD |      VALOR TOTAL     |")
            print("+----------+------------------------------+----------+----------------------+")
            for item in items.values():
                print(item)
            print("+----------+------------------------------+----------+----------------------+")

        elif len(items) == 0:
            print("\n+--------------------+---------------+---------------+------------------+----------------------+")
            print("                       |    EL CARRITO DE COMPRAS ESTA VACIO     |                               ")
            print("+--------------------+---------------+---------------+------------------+----------------------+")

        elif items == -1:
            print(f"ERROR: no existe un usuario con el numero de cedula {id}, debe registrarse para poder comprar")

    def agregar_moto_al_carrito(self):
        print("Agregar moto al carrito de compras")
        self.mostrar_catalogo_global()
        id: str = self.capturar_cadena_caracteres("Ingrese su numero de cedula")
        sku: str = self.capturar_cadena_caracteres("Ingrese el codigo sku de la moto que desea comprar")
        cantidad: int = self.capturar_entero(f"Ingrese la cantidad de motos de codigo {sku} que desea comprar")
        retorno = self.compraventa.agregar_moto_a_carrito(id=id, sku=sku, cantidad=cantidad)
        if retorno == 0:
            print(f"La moto de codigo {sku} se agrego correctamente al carrito de compras ")

        elif retorno == -1:
            print(f"ERROR: codigo incorrecto, no se encontro una moto con el codigo sku {sku}")

        elif retorno == -2:
            print(f"ERROR: No hay suficientes unidades disponibles para la cantidad {cantidad} de motos de mismo codigo "
                  f"que desea comprar ")

        elif retorno == -3:
            print(f"ERROR: no existe un usuario con el numero de cedula {id}")

    def eliminar_item_carrito(self):
        print("Eliminar un item del carrito")
        self.ver_carrito()
        id: str = self.capturar_cadena_caracteres("Ingrese su numero de cedula")
        codigo: int = self.capturar_entero("Ingrese el codigo del item que desea eliminar")
        retorno = self.compraventa.eliminar_item_de_carrito(id=id, codigo=codigo)

        if retorno == 0:
            print(f"El item de codigo {codigo} fue eliminado correctamente de tu carrito de compras")

        elif retorno == -1:
            print(f"ERROR: no existe un usuario con el numero de cedula {id}")

        elif retorno == -2:
            print(f"ERROR: el carrito de compras esta vacio, no esposible eliminar items ")

        elif retorno == -3:
            print(f"ERROR: el codigo de item: {codigo} ingresado NO EXISTE")

    def comprar_carrito(self):
        print("Comprar el carrito de compras")
        id: str = self.capturar_cadena_caracteres("Ingrese su numero de cedula")
        retorno = self.compraventa.comprar_carrito(id)

        if retorno == 0:
            self.compraventa.mostrar_detalles_de_la_compra(id)
            detalles_compra = self.compraventa.detalles_compra
            if len(detalles_compra) > 0:
                print("LA COMPRA DEL CARRITO FUE EXITOSA")
                print()
                print("                                     Detalles de la compra                  ")
                for item in detalles_compra.values():
                    print(
                        f"\n-{item.codigo} moto:       codigo sku= {item.moto.sku}       precio_unitario={item.moto.precio_unitario}"
                        f"        cantidad compradas={item.cantidad} _________________total={item.valor_total_item}")
                    print(f"                                                                      TOTAL DE LA COMPRA"
                          f"                 {self.compraventa.total_ventas}")

            elif len(detalles_compra) == 0:
                print("ERROR: El carrito esta vacio, no es posible realizar la compra")

        elif retorno == -1:
            print(f"ERROR: no existe un usuario con el numero de cedula {id}")

    def registrar_moto(self):
        print("\n Por favor ingrese la siguiente informacion para publicar su moto a la venta:")

        categoria: int  = int(input("\n La moto que desea registrar es 1.Nueva o 2.Usada:"))
        if categoria == 1:
            id: str = self.capturar_cadena_caracteres("Ingrese su numero de cedula:")
            sku: str = self.capturar_cadena_caracteres("Ingrese el codigo sku de la moto:")
            modelo: str = self.capturar_cadena_caracteres("Ingrese el modelo de la moto: ")
            marca: str = self.capturar_cadena_caracteres("ingrese la marca de la moto:")
            cilindraje: int = self.capturar_entero("ingrese el cilindraje de la moto:")
            precio_unitario: float = self.capturar_flotante("ingrese el precio unitario de venta para asignarle a la "
                                                            "moto:")
            cantidad: int = self.capturar_entero("ingrese la cantidad de unidades que vendera de esta referencia:")
            descripcion: str = self.capturar_cadena_caracteres("ingrese una descripcion de la moto:")
            retorno = self.compraventa.registrar_moto_nueva(id=id, sku=sku, modelo=modelo, marca=marca, cilindraje=cilindraje,
                                                            precio_unitario=precio_unitario, descripcion=descripcion,
                                                            cantidad=cantidad, id_vendedor=id)

            if retorno == 0:
                print("La moto usada fue registrada y publicada al catalogo de ventas correctamente")

            elif retorno == -1:
                print(f"ERROR: La moto con el codigo SKU {sku} ya existe, se habia registrado anteriormente")

            elif retorno == -2:
                print(f"ERROR: El usuario con el numero de cedula {id} aun no ha sido registrado, debe registrarlo")

        elif categoria == 2:
            id: str = self.capturar_cadena_caracteres("Ingrese su numero de cedula:")
            sku: str = self.capturar_cadena_caracteres("Ingrese el codigo sku de la moto:")
            placa: str = self.capturar_cadena_caracteres("Ingrese la placa de la moto: ")
            modelo: str = self.capturar_cadena_caracteres("Ingrese el modelo de la moto: ")
            marca = self.capturar_cadena_caracteres("ingrese la marca de la moto:")
            cilindraje = self.capturar_entero("ingrese el cilindraje de la moto:")
            precio_unitario = self.capturar_flotante("ingrese el precio unitario de venta para asignarle a la moto:")
            descripcion = self.capturar_cadena_caracteres("ingrese la descripcion de la moto:")
            retorno = self.compraventa.registrar_moto_usada(id, sku, placa, modelo, marca, cilindraje, precio_unitario,
                                                     descripcion, id_vendedor=id)

            if retorno == 0:
                print("La moto usada fue registrada y publicada al catalogo de ventas correctamente")

            elif retorno == -1:
                print(f"ERROR: La moto con el codigo SKU {sku} ya existe, se habia registrado anteriormente")

            elif retorno == -2:
                print(f"ERROR: El usuario con el numero de cedula {id} aun no ha sido registrado, debe registrarlo")

    def ver_mi_catalogo(self):
        print("Catalogo mi publicaciones:  motos disponibles a la venta")
        id: str = self.capturar_cadena_caracteres("Ingrese su numero de cedula:")
        mi_catalogo = self.compraventa.mostrar_mi_catalogo(id=id)

        if len(mi_catalogo) > 0:
            print("+--------------------+---------------+---------------+------------------+----------------------+")
            print("                                        MI CATALOGO                                             ")
            print("+--------------------+---------------+---------------+------------------+----------------------+")
            print("   CODIGO SKU        |MODELO         |MARCA          |PRECIO UNITARIO   |UNIDADES DISPONIBLES   ")
            print("+--------------------+---------------+---------------+------------------+----------------------+")
            for mi_moto in mi_catalogo.values():
                print(mi_moto)
            print("+--------------------+---------------+---------------+------------------+----------------------+")
            print()
            self.ver_mis_ventas()

        elif len(mi_catalogo) == 0:
            print("                                     MI CATALOGO VACIO                                          ")
            print("+--------------------+---------------+---------------+------------------+----------------------+")
            print("                    |    NO TIENES REGITRADAS MOTOS PARA VENDER     |                           ")
            print("+--------------------+---------------+---------------+------------------+----------------------+")

        elif mi_catalogo == -1:
            print(f"ERROR: no existe un usuario con el numero de cedula {id}, debe registrarse para poder comprar")


    def ver_mis_ventas(self):
        print("Listado de mis motos vendidas")
        id: str = self.capturar_cadena_caracteres("Ingrese su numero de cedula:")
        print("LISTA DE MIS VENTAS REALIZADAS")
        mis_ventas = self.compraventa.mostrar_mis_ventas(id)
        if len(mis_ventas) > 0:
            for venta in mis_ventas:
                print(f"Moto: -codigo sku= |{venta[0]}"
                      f"\n      -modelo    = |{venta[1]}"
                      f"\n      -Cantidad  = |{venta[2]}"
                      f"\n                   -----------------"
                      f"\n     TOTAL VENTA    {venta[3]}")
        else:
            print("ERROR: Su lista de ventas esta vacia, aun no ha vendido motos")

    def salir(self):
        print("\n Se cierra la aplicacion Compraventa de motos , Gracias por usarla!")
        sys.exit(0)









