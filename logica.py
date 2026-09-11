# ==========================================
# logica.py
# PARTE 1
# ==========================================

import sqlite3
from pathlib import Path

class Config:

    tantoA = 0
    tantoB = 0

    juegoA = 0
    juegoB = 0

    ganador = False


class Logica:
    
    def __init__(
        self,
        mostrar_callback,
        resultado_callback=None,
        bloque_callback=None
    ):

        self.colision_ganadora = None
        self.posicion_ganadora = None

        self.mostrar = mostrar_callback
        self.mostrar_resultado = resultado_callback
        self.mostrar_bloque_arriba = bloque_callback

        self.posicion_resaltada = None
        self.falta_terminar = False
        self.repite_saque = False
        self.punto = ""

        db_file = Path(__file__).resolve().parent / "colisionables.db"

        self.bd_disponible = db_file.is_file()

        if self.bd_disponible:

            self.conn = sqlite3.connect(db_file)
            self.cursor = self.conn.cursor()

        else:

            self.conn = None
            self.cursor = None

#            self.mostrar(
#                "[color=ff0000][b]ERROR[/b][/color]\n"
 #               "BASE DE DATOS 'colisionables.db' NO ENCONTRADA."
#            )

    # --------------------------------------

    def cerrar_bd(self):

        if hasattr(self, "cursor"):
            self.cursor.close()

        if hasattr(self, "conn"):
            self.conn.close()

    # --------------------------------------

    def establecer_punto(
        self,
        punto
    ):

        self.punto = punto.upper()

    # --------------------------------------

    def buscar_colision(
        self,
        pong
    ):

        if self.cursor is None:
            return None

        try:

            self.cursor.execute(
                """
                SELECT ZONA
                FROM colisionables
                WHERE ABREVIO LIKE ?
                """,
                (pong,)
            )

            resultado = self.cursor.fetchone()

            if resultado:
                return resultado[0]

            return None

        except sqlite3.Error as error:

            self.mostrar(
                f"ERROR DE BASE DE DATOS\n\n{error}"
            )

            return None

    # --------------------------------------

    def imprime_ganador(
        self,
        ta,
        tb,
        colision,
        posicion,
        falta_de_saque=False,
        punto_de_saque=False,
        falta_terminar=False
    ):

        if falta_de_saque:

            zona = "FALTA DE SAQUE"
            
        elif punto_de_saque:
        	
        	zona = "PUNTO DE SAQUE"
        
        elif falta_terminar:
        	
        	zona = "FALTA TERMINAR JUGADA....?"

        else:

            zona = self.buscar_colision(colision)

        if len(colision) == 1:
            self.posicion_resaltada = posicion + 6
        else:
            self.posicion_resaltada = posicion + 5

        if ta:

            ganador = "A"
            Config.tantoA += 1

            if Config.tantoA == 3:
                Config.juegoA += 1
                Config.tantoA = 0
                Config.tantoB = 0

        else:

            ganador = "B"
            Config.tantoB += 1

            if Config.tantoB == 3:
                Config.juegoB += 1
                Config.tantoA = 0
                Config.tantoB = 0

        if Config.juegoA == 3 or Config.juegoB == 3:
            Config.ganador = True

        if self.mostrar_resultado:

            self.mostrar_resultado(
                ganador,
                zona,
                self.posicion_resaltada,
                Config.ganador,
                falta_terminar
            )

    # --------------------------------------

    def error_secuencia(
        self,
        caracter_erroneo,
        posicion
    ):

        self.posicion_resaltada = posicion

        bloque = (
            "[color=ff0000][b]"
            "_______________________________________\n\n"
            "ANOMALIA SECUENCIAL\n\n"
            "JUGADA MAL DEFINIDA\n"
            "_______________________________________"
            "[/b][/color]"
        )

        self.mostrar_bloque_arriba(bloque)
#        self.mostrar(
#            f"\nANOMALIA SECUENCIAL\n\n"
#            f"'{caracter_erroneo}'. "
#            f"JUGADA MAL DEFINIDA EN LA POSICIÓN "
#            f"{posicion + 1}\n"
#            f"JUGADA MAL DEFINIDA"
#        )

#        cadena = "'"

#        for i in range(len(self.punto)):

#           if i == posicion:

#                self.posicion_resaltada = i
#                cadena += (
#                    f"[b]{self.punto[i].upper()}[/b]"
#                )

#            else:

#                cadena += (
#                    self.punto[i].upper()
#                )

#        cadena += "'"

#        self.mostrar(cadena)
#        self.mostrar(" ")

    # --------------------------------------

    def se_repite_saque(
        self,
        cadena,
        n_redes
    ):

        self.repite_saque = True

        self.posicion_resaltada = 4

    # -------------------------------------------------

    def ganador_tanto(
        self,
        resto_jugada,
        ganador
    ):

    # ==================================
    # INICIO: todavía no sabemos si falta                     terminar o punto de saque
    # ==================================

        self.falta_terminar = False

    # ==================================
    # SI NO HAY JUGADA DESPUÉS DEL SAQUE
    # ==================================

        if resto_jugada == "":

            self.falta_terminar = True

            return

        mesa = True
        jugador = False
        punto_saque = True

        match ganador:

            case "A":
                turnoA = True
                turnoB = False

            case "B":
                turnoB = True
                turnoA = False

        for i in range(len(resto_jugada)):

            match resto_jugada[i]:

                case "J":

                    if jugador:
                        if turnoA:
                            turnoB = True
                            turnoA = False
                        elif turnoB:
                            turnoB = False
                            turnoA = True

                        self.imprime_ganador(
                            turnoA,
                            turnoB,
                            resto_jugada[i:(i + 2)],
                            i + 1
                        )

                        return

                    jugador = True
                    mesa = False
                    punto_saque = False

                case "M":
                    
                    if mesa:

                        self.imprime_ganador(
                            turnoA,
                            turnoB,
                            resto_jugada[i:(i + 2)],
                            i + 1
                        )

                        return
                    
                    elif jugador:

                        if (
                            turnoA
                            and i + 1 < len(resto_jugada)
                            and resto_jugada[i + 1] == "A"
                        ):

                            self.imprime_ganador(
                                False,
                                True,
                                resto_jugada[i:(i + 2)],
                                i + 1
                            )

                            return

                        elif (
                            turnoB
                            and i + 1 < len(resto_jugada)
                            and resto_jugada[i + 1] == "B"
                        ):

                            self.imprime_ganador(
                                True,
                                False,
                                resto_jugada[i:(i + 2)],
                                i + 1
                            )

                            return
                            
                    mesa = True
                    jugador = False
                    punto_saque = False 

                case "T":
                    
                    if jugador:
                        if turnoA:
                            turnoB = True
                            turnoA = False
                        elif turnoB:
                            turnoB = False
                            turnoA = True
                    
                    self.imprime_ganador(
                            turnoA,
                            turnoB,
                            resto_jugada[i : (i + 2)],
                            i + 1,
                            None,
                            punto_saque
                    )
                    
                    return

                case "A":

                    # ===========================
                    # SI ACABA LA JUGADA EN "A"       
                    # ===========================
                    if i == len(resto_jugada) - 1:

                        if turnoB:
                            self.falta_terminar = True  
                        else:
                            self.imprime_ganador(
                                False,
                                True,
                                resto_jugada[(i - 1):(i + 1)],
                                i
                            )

                        return

                    # ===========================
                    # SI ACABA EN "R" PERO LA 
                    # JUGADA TERMINA ANTES
                    # =========================== 
                    elif turnoA and (resto_jugada[i + 1] == "R"):
                        
                        self.imprime_ganador(
                            False,
                            True,
                            resto_jugada[i - 1:i + 1],
                            i
                        )
                            
                        return
                    
                    # ===========================
                    # SI EXISTE "JAJA" o "JBJA" 
                    # ===========================
                    elif jugador:
                        if turnoB:
                            turnoB = False
                            turnoA = True

                            if (
                                i + 1 < len(resto_jugada)
                               and resto_jugada[i + 1] == "J"
                            ):

                                self.imprime_ganador(
                                    False,
                                    True,
                                    resto_jugada[(i + 1):(i + 3)],
                                    i + 2
                                )

                                return
                                
                        elif turnoA:
                            turnoA = False
                            turnoB = True

                            if (
                                i + 1 < len(resto_jugada)
                                and resto_jugada[i + 1] == "J"
                            ):

                                self.imprime_ganador(
                                    False,
                                    True,
                                    resto_jugada[(i - 1):(i + 1)],
                                    i
                                )

                                return
                            
                    # ===========================
                    # SI EXISTE "MAMA" o "MAMB"
                    # ===========================
                    elif mesa and (i < len(resto_jugada) - 1) and (resto_jugada[i + 1] == "M"):

                        if turnoA:
                        	self.imprime_ganador(
                                False,
                                True,
                                resto_jugada[i - 1:i + 1],
                                i
                            )
                        else:                     
                            self.imprime_ganador(
                                False,
                                True,
                                resto_jugada[i + 1:i + 3],
                                (i + 2)
                            )
                        
                        return

                case "B":

                    # ===========================
                    # SI ACABA LA JUGADA EN "B"       
                    # ===========================
                    if i == len(resto_jugada) - 1:

                        if turnoA:
                            self.falta_terminar = True
                        else:
                            self.imprime_ganador(
                                True,
                                False,
                                resto_jugada[(i - 1):(i + 1)],
                                i
                            )

                        return

                    # ===========================
                    # SI ACABA EN "R" PERO LA 
                    # JUGADA TERMINA ANTES
                    # =========================== 
                    elif turnoB and (resto_jugada[i + 1] == "R"):
                        self.imprime_ganador(
                            True,
                            False,
                            resto_jugada[i - 1:i + 1],
                            i
                        )
                            
                        return
                    
                    # ===========================
                    # SI EXISTE "JBJB" o "JBJA"      
                    # =========================== 
                    elif jugador:
                        if turnoA:
                            turnoB = True
                            turnoA = False

                            if (
                                i + 1 < len(resto_jugada)
                               and resto_jugada[i + 1] == "J"
                            ):

                                self.imprime_ganador(
                                    True,
                                    False,
                                    resto_jugada[(i + 1):(i + 3)],
                                    i + 2
                                )

                                return
                                
                        elif turnoB:
                            turnoA = True
                            turnoB = False

                            if (
                                i + 1 < len(resto_jugada)
                                and resto_jugada[i + 1] == "J"
                            ):

                                self.imprime_ganador(
                                    True,
                                    False,
                                    resto_jugada[(i - 1):(i + 1)],
                                    i
                                )

                                return
                        	
                    # ===========================
                    # SI EXISTE "MBMB" o "MBMA"
                    # ===========================
                    elif mesa and (i < len(resto_jugada) - 1) and (resto_jugada[i+1] == "M"):
                    	
                        if turnoB:
                        	self.imprime_ganador(
                                True,
                                False,
                                resto_jugada[i - 1:i + 1],
                                i
                            )
                        else:                     
                            self.imprime_ganador(
                                True,
                                False,
                                resto_jugada[i + 1:i + 3],
                                (i + 2)
                            )
                        
                        return

                case "V" | "L" | "S":
                    
                    if jugador:
                        if turnoA:
                            turnoB = True
                            turnoA = False
                        elif turnoB:
                            turnoB = False
                            turnoA = True
                    
                    self.imprime_ganador(
                        turnoA,
                        turnoB,
                        resto_jugada[i],
                        i,
                        None,
                        punto_saque
                    )
                    
                    return

                case "P":
                    
                    self.imprime_ganador(
                        turnoA,
                        turnoB,
                        resto_jugada[(i - 1):(i + 1)],
                        i,
                        None,
                        punto_saque
                    )
                    
                    return

                case "R":

                    if i == len(resto_jugada) - 1:

                        self.falta_terminar = True
                        return
                        
    # -------------------------------------------------

    def evaluar_saque(
        self,
        punto
    ):

        saque = punto[0:2]
        ganador = ""

        match saque:

            case "JA":

                # SACA JUGADOR A
                match punto[2:4]:

                    case "MA":

                        # BOTA EN LA MESA A
                        match punto[4:6]:
  
                            case "MB":

                                # BIEN SACADO
                                ganador = "A"

                                self.ganador_tanto(
                                    punto[6:],
                                    ganador
                                )

                            case "RM":

                                # POSIBLE RED AL SACAR
                                if punto[6] == "B":

                                    self.se_repite_saque(
                                        punto,
                                        4
                                    )

                                else:

                                    self.imprime_ganador(
                                        False,
                                        True,
                                        punto[5:7],
                                        0,
                                        True
                                    )

                            case "RR":

                            # POSIBLES VARIAS REDES                                   CONSECUTIVAS
                                for i in range(4, len(punto)):
                                    i2 = i

                                    if punto[i] != "R":
                                        break

                                if (
                                    punto[i2] == "M"
                                    and punto[i2 + 1] == "B"
                                ):

                                    if i2 < len(punto) - 1:

                                        self.se_repite_saque(
                                        punto,
                                        i2 - 1
                                    )

                                elif (
                                    punto.endswith("R")
                                    and i2 == len(punto) - 1
                                ):

                                    # TERMINA EN RED
                                    self.falta_terminar = True
                                    return

                                else:

                                    match punto[i2]:

                                          case "M" | "B" | "T":

                                              self.imprime_ganador(
                                                  False,
                                                  True,
                                                  punto[i2:i2 + 2], i2 - 5,
                                                  True
                                              )

                                          case _:

                                              self.imprime_ganador(
                                                  False,
                                                  True,
                                                  punto[i2], i2 - 6,
                                                  True
                                              )

                            case _:
                            # punto[4:6]

                                if len(punto) == 4:
                                # SI LA CADENA ES "JAMA"  
                                    self.falta_terminar = True
                                    return
                                elif (
                                    punto.endswith("R")
                                    and len(punto) == 5
                            ):

                                    self.falta_terminar = True
                                    return

                                else:

                                    match punto[4]:

                                        case "M" | "B" | "T":

                                            self.imprime_ganador(
                                                False,
                                                True,
                                                punto[4:6],
                                                -1,
                                                True
                                            )

                                        case "R":

                                            if len(punto) > 5:

                                            # SI ES
                                            # "JAMAR/BP/TM/MA/MB"
                                               match punto[5]:

                                                    case "M" | "B" | "T":

                                                        self.imprime_ganador(
                                                            False,
                                                            True,
                                                            punto[5:7],
                                                            0,
                                                            True
                                                        )

                                                    case _:
                                                    # SI ES "JAMAR"
                                                        self.imprime_ganador(
                                                            False,
                                                            True,
                                                            punto[5],
                                                            -1,
                                                            True
                                                        )

                                            else:

                                                self.imprime_ganador(
                                                    False,
                                                    True,
                                                    punto[4],
                                                    -2,
                                                    True
                                                )

                                        case _:
                                        # SI ES "JAMA/V/L/S"

                                            self.imprime_ganador(
                                                False,
                                                True,
                                                punto[4],
                                                -2,
                                                True
                                            )

                    case _:
                    # punto[2:4]

                        if len(punto) == 2:
                        # SI LA CADENA ES SOLO "JA"     
                            self.falta_terminar = True
                            return

                        else:

                            if len(punto) == 3:
                                    self.imprime_ganador(
                                        False,
                                        True,
                                        punto[2],
                                        -4,
                                        True
                                    )
                            else:
                                match punto[2]:

                                    case "R" | "V" | "L" | "S":

                                        self.imprime_ganador(
                                            False,
                                            True,
                                            punto[2],
                                            -4,
                                            True
                                        )

                                    case _:
                                                        
                                        self.imprime_ganador(
                                            False,
                                            True,
                                            punto[2:4],
                                            -3,
                                            True
                                    )
                                
            case "JB":

                # SACA JUGADOR B
                match punto[2:4]:

                    case "MB":

                        # BOTA EN LA MESA B
                        match punto[4:6]:

                            case "MA":

                                # BIEN SACADO
                                ganador = "B"

                                self.ganador_tanto(
                                    punto[6:],
                                    ganador
                                )

                            case "RM":

                                # POSIBLE RED AL SACAR
                                if punto[6] == "A":

                                    self.se_repite_saque(
                                        punto,
                                        4
                                    )

                                else:

                                    self.imprime_ganador(
                                        True,
                                        False,
                                        punto[5:7],
                                        0,
                                        True
                                    )

                            case "RR":

                            # POSIBLES VARIAS REDES                                   CONSECUTIVAS
                                for i in range(4, len(punto)):
                                    i2 = i

                                    if punto[i] != "R":
                                        break

                                if (
                                    punto[i2] == "M"
                                    and punto[i2 + 1] == "A"
                                ):

                                    if i2 < len(punto) - 1:

                                        self.se_repite_saque(
                                        punto,
                                        i2 - 1
                                    )

                                elif (
                                    punto.endswith("R")
                                    and i2 == len(punto) - 1
                                ):

                                    # TERMINA EN RED
                                    self.falta_terminar = True
                                    return

                                else:

                                    match punto[i2]:

                                          case "M" | "B" | "T":

                                              self.imprime_ganador(
                                                  False,
                                                  True,
                                                  punto[i2:i2 + 2], i2 - 5,
                                                  True
                                              )

                                          case _:

                                              self.imprime_ganador(
                                                  False,
                                                  True,
                                                  punto[i2], i2 - 6,
                                                  True
                                              )

                            case _:
                            # punto[4:6]

                                if len(punto) == 4:
                                # SI LA CADENA ES "JBMB"  
                                    self.falta_terminar = True
                                    return

                                elif (
                                    punto.endswith("R")
                                    and len(punto) == 5
                                ):
   
                                    self.falta_terminar = True
                                    return

                                else:

                                    match punto[4]:

                                        case "M" | "B" | "T":

                                            self.imprime_ganador(
                                                True,
                                                False,
                                                punto[4:6],
                                                -1,
                                                True
                                            )

                                        case "R":

                                            if len(punto) > 5:

                                            # SI ES
                                            # "JBMBR/BP/TM/MA/MB"
                                                match punto[5]:

                                                    case "M" | "B" | "T":

                                                        self.imprime_ganador(
                                                            True,
                                                            False,
                                                            punto[5:7],
                                                            0,
                                                            True
                                                        )

                                                    case _:
                                                    # SI ES "JBMBR"
                                                        self.imprime_ganador(
                                                            True,
                                                            False,
                                                            punto[5],
                                                            -1,
                                                            True
                                                        )

                                            else:

                                                self.imprime_ganador(
                                                    True,
                                                    False,
                                                    punto[4],
                                                    -2,
                                                    True
                                                )

                                        case _:

                                        # SI ES "JBMB/V/L/S"
                                            self.imprime_ganador(
                                                True,
                                                False,
                                                punto[4],
                                                -2,
                                                True
                                            )

                    case _:
                    # punto[2:4]

                        if len(punto) == 2:
                        # SI LA CADENA ES SOLO "JB"     
                            self.falta_terminar = True
                            return

                        else:

                            if len(punto) == 3:
                                    self.imprime_ganador(
                                        True,
                                        False,
                                        punto[2],
                                        -4,
                                        True
                                    )
                            else:
                                match punto[2]:

                                    case "R" | "V" | "L" | "S":

                                        self.imprime_ganador(
                                            True,
                                            False,
                                            punto[2],
                                            -4,
                                            True
                                        )

                                    case _:
                                                        
                                        self.imprime_ganador(
                                            True,
                                            False,
                                            punto[2:4],
                                            -3,
                                            True
                                    )

            case _:
                # saque

                self.error_secuencia(
                    saque[0],
                    0
                )
                
    # -------------------------------------------------

    def evaluar_cadena(
        self,
        ping
    ):

        try:

            c = 0
            jugada = ""
            doble = False
            punto_correcto = True

            for i in range(len(ping)):

                if not doble:

                    encontrado = self.buscar_colision(
                        ping[i]
                    )

                    if encontrado:

                        jugada += encontrado[2]
                        doble = False

                    elif (c + 1) < len(ping):

                        if len(ping) > 1:

                            ping2 = (
                                ping[i]
                                + ping[i + 1]
                            )

                        else:

                            ping2 = ping

                        encontrado2 = (
                            self.buscar_colision(
                                ping2
                            )
                        )

                        if encontrado2:

                            jugada += (
                                encontrado2[2]
                            )

                            doble = True

                        else:

                            punto_correcto = False
                            break

                    else:

                        punto_correcto = False
                        break

                else:

                    doble = False

                c += 1

            # DEVUELVE SI ES PUNTO O NO,
            # LA LETRA DONDE TERMINA Y SU POSICIÓN
            return (
                punto_correcto,
                ping[i],
                i
            )

        except sqlite3.Error as error:

            self.mostrar(
                f"ERROR DEL PROGRAMA\n\n{error}"
            )

            return (
                False,
                "",
                0
            )
    # -------------------------------------------------

    def procesar_punto(self, punto):

        # Reiniciar estados de la nueva jugada
        self.falta_terminar = False
        self.repite_saque = False
        self.punto = punto.strip().upper()

        if not self.punto:
            return

        punto_correcto, caracter, posicion = (
            self.evaluar_cadena(self.punto)
        )

        if punto_correcto:

            self.evaluar_saque(self.punto)

            return (
                True,
                self.posicion_resaltada
            )

        else:

            self.error_secuencia(
                caracter,
                posicion
            )

            return (
                False,
                self.posicion_resaltada
            )