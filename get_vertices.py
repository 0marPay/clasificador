import sys
import json
import jmespath
from ocr import ocr
from draw import draw_image

def get_vertices(annotations, interes_words):
    
    words = []
    count = {i:0 for i in interes_words} 
    
    single_words = []
    frases = []
    
    for word in interes_words:
        split_frase = word.split(' ')
        if len(split_frase) == 1:
            single_words.append(word)
        else:
            frases.append(split_frase)
    
    for word in single_words:
        coincidencias = get_matches(data=annotations, word=word)
        words = words + coincidencias
        for word in words:
            count[word["word"]] = count[word["word"]] + 1
            print(word)
    
    for frase in frases:
        
        coincidencias = get_matches(data=annotations, word=frase[0])
        if coincidencias == [] : continue
        
        for coincidence in coincidencias: 
            idx = annotations.index(coincidence)
            # Creamos la frase de la misma longitud y preguntamos si es la misma de la origin
            frase_encontrada = [annotations[idx+idx_plus]["word"] for idx_plus in range(len(frase))]
            if frase != frase_encontrada: continue
            
            # Proceso de recuperación de indices 
            frase_range = range(idx, idx + len(frase))
            
            V1x = min([annotations[i]["vert"][0][0] for i in frase_range])
            V1y = min([annotations[i]["vert"][0][1] for i in frase_range])
            V2x = max([annotations[i]["vert"][1][0] for i in frase_range])
            V2y = max([annotations[i]["vert"][1][1] for i in frase_range])
            
            v1 =  [V1x, V1y]
            v2 =  [V2x, V2y]
            
            # Guardamos resultados
            count[' '.join(frase)] = count[' '.join(frase)] + 1
            w = {}
            w["word"] = ' '.join(frase)
            w["vert"] = [v1,v2]
            print(w)
            words.append(w)  
            
    print(count)
    return words

def normalize(s):
    replacements = (
        ("á", "a"),
        ("é", "e"),
        ("í", "i"),
        ("ó", "o"),
        ("ú", "u"),
        ("Á", "A"),
        ("É", "E"),
        ("Í", "I"),
        ("Ó", "O"),
        ("Ú", "U"),
        ("ı", "i")
    )
    for a, b in replacements:
        s = s.replace(a, b).replace(a.upper(), b.upper())
    return s

def get_matches(data, word):
    expression = f"[?word == '{word}']"
    return jmespath.search(expression, data)

def save_json(my_dict, file_name):
    json_string = json.dumps(my_dict)
    json_file = open(file_name, "w")
    json_file.write(json_string)
    json_file.close()

def check_unicity(input_dict, words):
    
    words_list = jmespath.search("[].word", input_dict)
    
    correct_index = []
    for idx, word in enumerate(words_list):
        if word not in words.keys():
            correct_index.append(idx)
    
    output_dict = [input_dict[idx] for idx in correct_index]
    for word, idx in words.items():
        current_word_list = jmespath.search(f"[?word == '{word}']", input_dict)
        output_dict.append(current_word_list[idx])
        
    return output_dict
    
if __name__ == "__main__":

    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    
    document = "IZZI"
    path = f'resources/{document}.jpg'
    
    annotations = ocr(path)
    save_json(my_dict=annotations, file_name=path.replace(".jpg","_general.json"))
    
    # CFE
    # interes_words = ["Como Federal Electricidad", 
    #                  "TOTAL A PAGAR :", 
    #                  "CORTE A PARTIR", 
    #                  "LIMITE DE PAGO",
    #                  "RMU :",
    #                  "NO . DE SERVICIO :",
    #                  "CORTE A PARTIR :",
    #                  "PERIODO FACTURADO"]
    # modelo_words = ["ARCELIA DE RICO",
    #                 "MARKO 402 ANUEL BERNAL Y MARIA PAVON . CPSIBIẾ NEZAHUALCOYOTL , MEX",
    #                 "01 NOV 2022",
    #                 "$ 974",
    #                 "991821001311",
    #                 "57610 82-10-26 XAXX - 010101 001 CFE",
    #                 "02 NOV 2022",
    #                 "01 NOV 2022",
    #                 "15 AGO 22-13 OCT 22"]
    # words={"$ 974":0, "991821001311": 0}
    
    # caratura
    # interes_words = [#"ANUAL", "Ordinaria", "CAT", "PAGAR", "PLAZO", "limite","corte", "Tipo", 
    #                  "CARÁTULA DEL CRÉDIO",
    #                  "PLAZO DEL CRÉDITO", 
    #                  "Costo Anual Total",
    #                  "Fecha limite de pago",
    #                  "Fecha de corte",
    #                  "TASA DE INTERÉS ANUAL FIJA",
    #                  "Tipo de Crédito",
    #                  "MONTO DEL CRÉDITO",
    #                  "MONTO TOTAL A PAGAR",
    #                  "Nombre comercial del Producto"]
    # modelo_words = ["Contrato Múltiple / Crédito Simple Digital",
    #                 "Simple",
    #                 "270.7 %",
    #                 "110.34 %",
    #                 "$ 6,715.30 M.N",
    #                 "$ 10,264.00 M.N",
    #                 "13 Quincenas",
    #                 "19/12/2022"]
    # words={"Simple": 0}
    
    # IZZI
    interes_words = ["izzı",
                     "Realiza tu pago escaneando este código :",
                     "Total a pagar",
                     "Fecha Límite de pago",
                     "Teléfono",
                     "Referencia",
                     "Realiza tu pago escaneando este código :",
                     "Período facturación"]
    modelo_words = ["JAFET MAXIMILIANO JIMENEZ RAMIREZ",
                    "PRIV GERBERA 16 VALLE SAN PEDRO TIJUANA BAJA CALIFORNIA C.P. 22263 , MEXICO",
                    "$ 600.00",
                    "07 de sep del 22",
                    "6649094725",
                    "0342437944",
                    "34243794",
                    "del 02 - ago - 22 al 01 - sep - 22"]
    words={"$ 600.00": 1}
    
    # SOLICITUD
    # interes_words = ["AF01 - S",
    #                  "SOLICITUD DE CREDITO",
    #                  "Monto del prestamo solicitado",
    #                  "Plazo a que se requiere el Préstamo",
    #                  "Para que tene pensado utilizar e Préstamo",
    #                  "Nombres ) sin abreviaturas",
    #                  "Apelido Palermo",
    #                  "Apelido Matamo",
    #                  "Correo electrónico ( si cuenta con",
    #                  "Género",
    #                  "Nacionalidad",
    #                  "RFC con Homoclave",
    #                  "Casado ( a )", "Solter )", "Divorciado ( a )",
    #                  "Union LibreO", "Separado ( a )", "Viudoja )",
    #                  "Primaria", "Secundana i", "Preparatoria",
    #                  "Posgrado", "Técnico", "Licenciatura",
    #                  "Fecha de Nacimiento ( DMA )",
    #                  "Entidad federativa de nacimiento",
    #                  "Dependientes Económicos",
    #                  "Colonia",
    #                  "Pais de nacimiento",
    #                  "Entre que calles se encuentr",
    #                  "Dirección actual ( calle y número ) exterior e interior",
    #                  "CURP",
    #                  "Estado",
    #                  "Municipio / Delegación",
    #                  "Código Postal",
    #                  "Tiempo en este domicilio",
    #                  "Telefono ( s )",
    #                  "Tel Celular",
    #                  "Empleado ( asalanado )",
    #                  "Nombre de la Empresa , Negocio o Patrón",
    #                  "Dirección Actual ( calle y numero",
    #                  "País", "Pais",
    #                  "Entre que calles se encuentr",
    #                  "Municipio / Delegación",
    #                  "Codigo Postal",
    #                  "Tiempo en este Empleo",
    #                  "Municipio Delegación",
    #                  "Micronegocio ( independente )",
    #                  "Actividad / Giro de la Empresa",
    #                  "Entre que calles se encuentra",
    #                  "Teléfono ( s )",
    #                  "Sueldo Mensual Fo",
    #                  "Oros ingresos Variables",
    #                  "Fuente de estos ingresos",
    #                  "Ares / Departamento / Sección donde labora",
    #                  "Puesto / Posición en el empleo",
    #                  "Pago Casa", "Pago Servicios",
    #                  "Pago Otros",
    #                  "Gasto mensual da predial , agua , otros",
    #                  "Valor de la casa",
    #                  "Si está hipotecada saldo de la hipoteca",
    #                  "Empresa que financia la hipoteca",
    #                  "Nombre del Propietario", 
    #                  "Parentesco",
    #                  "Posen Automov ?", "Marca Modelo y Año",
    #                  "Valor factura",
    #                  "En caso de estar papándolo , empresa que financial crédito",
    #                  "Mensualidad",
    #                  "LUGAR Y FECHA : en que firma la autorización de consulta",
    #                  "Folio de consulta"
    #                  ]
    # modelo_words = ["21066",
    #                 "JOSE ALEJANDRO OLAYA SANCHEZ",
    #                 "$ 6,715.30",
    #                 "13",
    #                 "Quincenas",
    #                 "GASTOS PERSONALES E IMPREVISTOS",
    #                 "JULIO CESAR",
    #                 "RODRIGUEZ",
    #                 "TEJEDA",
    #                 "juliocesar97@gmail.com",
    #                 "MEX",
    #                 "ROTJ971108L60",
    #                 "ROTJ971108HDFDJL03",
    #                 "8 11 1997",
    #                 "CIUDAD DE MEXICO",
    #                 "0",
    #                 "LAS AGUILAS",
    #                 "AV4 Y AV 6",
    #                 "CALLE 13 No. NUM 135",
    #                 "NEZAHUALCOYOT",
    #                 "MEXICO",
    #                 "57900",
    #                 "24 Años",
    #                 "5576140091", "5571897727",
    #                 "FARMACIA DE SIMILARES SA DE CV",
    #                 "FALEMAN 10 COL INDEPENDENCIA",
    #                 "Ados", "Mess 5",
    #                 "5554227090",
    #                 "$ 10,123.62",
    #                 "$ 0.00",
    #                 "AYUDANTE",
    #                 "$ 300.00", "$ 500.00",
    #                 "26/11/22",  "2753942809"
    #                 ]
    # words={"13": 1}
    
    # SEGURO_DESEMPLEO
    # interes_words = ["Póliza",
    #                 "Certificado",
    #                 "Datos Generales",
    #                 "Nombre del Asegurado", 
    #                 "Fecha Nacimiento",
    #                 "Vigencia",
    #                 "Actividad / Ocupación",
    #                 "Sexo",
    #                 "Fecha Ingreso",
    #                 "Suma Asegurada",
    #                 "Pesos M.N.",
    #                 "Invalidez Total Temporal"+" ***",
    #                 "Lugar y Fecha de Emisión" 
    #                 ]
    # words={"Certificado": 2, "Póliza":0}
    # modelo_words = ["10-17187",
    #                 "TEP6999D",
    #                 "APOYO ECONÓMICO FAMILIAR SA DE CV SOFOM ENR",
    #                 "RODRIGUEZ TEJEDA JULIO CESAR",
    #                 "07/11/1997",
    #                 "26/11/2022",
    #                 "AYUDANTE",
    #                 "XM",
    #                 "26/11/2022",
    #                 "26/06/2023",
    #                 "3 mensualidades ( 6 Q , 13 S ) pagos de su crédito",
    #                 "Titular : 3 ( 6 Q , 13 S ) pagos del crédito con un tope total de $ 16.500",
    #                 "Titular : 3 ( 6 Q. 13 S ) pagos del crédito con un tope total de $ 16.500",
    #                 "LOS REYES , ESTADO DE MEXICO , a 26 del mes noviembre del año 2022" 
    #                 ]
    
    # SEGURO_GENERAL
    # interes_words = ["Póliza",
    #                 "Datos Generales",
    #                 "Nombre del Asegurado", 
    #                 "Fecha de Nacimiento",
    #                 "Vigencia certificado",
    #                 "Sexo",
    #                 "Fecha de Ingreso",
    #                 "Suma Asegurada",
    #                 "Edad",
    #                 "Ocupación",
    #                 "Domicilio",
    #                 "Beneficiarios",
    #                 "Parentesco",
    #                 "Porcentaje",
    #                 "Fallecimiento Invalidez total y permanente"
    #                 ]
    # modelo_words = ["APOYO ECONÓMICO FAMILIAR SA DE CV SOFOM ENR",
    #                 "PEREZ CASTRO ARMANDO GILBERTO", "M",
    #                 "12-19368", "NZ1169630", "25",
    #                 "16/11/2022", "16/11/2023", "16/02/1997",
    #                 "AYUDANTE", "$ 50,000.00 Pesos MN",
    #                 "CALLE MARIO No Ext 40 No. Int SN Col. PAVON SECCION SILVIA Estado MEXICO Pais MEXICO , CP . 57610",
    #                 "ALEJADRA MARIA DE LOS SANTOS MARTINEZ", "OTRO", "100.00 %"]
    
    # CURP
    # interes_words = ["Clave :", "Nombre",
    #                  "Fecha de inscripción",
    #                  "Folio", "Entidad de registro",
    #                  ]
    # modelo_words = ["CAPA970216HDFSRR07",
    #                 "ARMANDO GILBERTO CASTRO PEREZ",
    #                 "31/01/2000", "49934058",
    #                 "MEXICO"]
    # words={"ARMANDO GILBERTO CASTRO PEREZ": 1}
    
    # disposición
    # interes_words = ["TITULAR :",
    #                  "BANCO :",
    #                  "CLABE :",
    #                  "CUENTA :",
    #                  "NUMERO DE TARJETA DE DÉBITO :",
    #                  "por la cantidad de",
    #                  "número de contrato"]
    # modelo_words = ["CRUZ HERNANDEZ FELIPE", "40878",
    #                 "AZTECA", "127180013681399713", "4027665783645295",
    #                 "$ 100000 ( CIEN MIL PESOS 00/100 MN )"]
    
    # TABLA_AMORTIZACION
    # interes_words = ["Sucursal", "Contrato", "Nombre del Cliente",
    #                  "Fecha de Apertura", "Producto", "Frecuencia",
    #                  "Plazo", "Tasa Anual", "CAT", "Saldo Inicial",
    #                  "Fecha Elaboración", "Monto del Crédito", 
    #                  "Comisiones e / IVA", "Seguros", "Total :"]
    # modelo_words = ["NZI", "48573", "CASTRO PEREZ ARMANDO",
    #                 "16/11/2022", "Colto Simple", "Semanas",
    #                 "78", "135.81 %", "403.3 %", "$ 10,576.40",
    #                 "$ 8,000.00", "$ 1,206.40", "$ 1,370.00"]
    # words={"ARMANDO GILBERTO CASTRO PEREZ": 1}
    
    # INE_1
    # interes_words = ["NOMBRE","DOMICILIO", "CLAVE DE ELECTOR", "CURP",
    #                 "ESTADO",  "LOCALIDAD", "FECHA DE NACIMENTO", "SEXO",
    #                 "ANO DE REGISTRO", "MUNICIPIO",  "SECCION", "EMISION",
    #                 "VIGENCIA"]
    # modelo_words = ["RODRIGUEZ TEJEDA JULIO CESAR", "RDTJJL97110809H900",
    #                 "C 13 135 COL LAS AGUILAS 57900 NEZAHUALCOYOTL , MEX",
    #                 "ROTJ971108HDFDJL03", "15", "0001", "08/11/1997", "H",
    #                 "2015 00", "060", "3625", "2015", "2025"]
    # words={"2015": 1}
    
    # INE_2
    # interes_words = ["NOMBRE","DOMICILIO", "CLAVE DE ELECTOR", "CURIP",
    #                 "ESTADO",  "LOCALIDAD", "FECHA DE NACIMENTO", "sexo",
    #                 "ANO DE REGISTRO", "MUNICIPIO",  "SECCION", "EMISION",
    #                 "VIGENCIA"]
    # modelo_words = []
    
    # SEGURO_INTEGRAL
    # interes_words = ["Contratante :", "Nombre Completo del asegurado :",
    #                 "Fecha de nacimiento :", "Muerte Accidental", "Género",
    #                 "Diagnóstico de Enfermedades Graves", "Porcentaje",
    #                 "Renta diaria por Hospitalización", "Nombre Completo",
    #                 "Lugar y Fecha", "Fecha de Aplicación :", "Póliza :",
    #                 "Certificado :", "Inicio de Vigencia", "Fin de Vigencia",
    #                 "Parentesco"]
    # words={"Nombre Completo": 1}
    # modelo_words = ["APOYO ECONÓMICO FAMILIAR SA DE CV SOFOM ENR", "OTRO",
    #                 "FELIPE CRUZ HERNANDEZ", "28/05/1978", "IXC15789P",
    #                 "$ 20,000", "$ 300.00", "MA . ALICIA RENTERIA TERAN",
    #                 "ESTADO DE MEXICO a 16 de Noviembre del 2022",
    #                 "16/11/2022", "PIA221152", "MASCULINO", "16/11/2023",
    #                 "100.00 %"]
    
    interes = get_vertices(annotations, interes_words)
    # interes = check_unicity(interes, words={"Nombre Completo": 1})
    save_json(my_dict=interes, file_name=path.replace(".jpg","_interes.json"))
    interes =  [w["vert"] for w in interes]
    
    modelo = get_vertices(annotations, modelo_words)
    modelo = check_unicity(modelo, words={"$ 600.00": 1})
    save_json(my_dict=modelo, file_name=path.replace(".jpg","_modelo.json"))
    modelo =  [w["vert"] for w in modelo]
    
    draw_image(path=path, modelo=modelo, interes=interes, show=False, save=True)