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
            
            # Proceso básico de recuperación de indices 
            i = idx
            f = idx + len(frase) - 1
            count[' '.join(frase)] = count[' '.join(frase)] + 1
            v1 =  annotations[i]["vert"][0]
            v2 =  annotations[f]["vert"][1]

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

if __name__ == "__main__":
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    
    path = 'resources/caratula.jpg'
    path = 'resources/amortización.jpg'
    path = 'resources/CFE.jpg'

    annotations = ocr(path)
    save_json(my_dict=annotations, file_name=path.replace(".jpg","_general.json"))
    
    # caratura
    interes_words = [#"ANUAL", "Ordinaria", "CAT", "PAGAR", "PLAZO", "limite","corte", "Tipo", 
                     "PLAZO DEL CRÉDITO", 
                     "Costo Anual Total",
                     "Fecha limite de pago",
                     "Fecha de corte",
                     "TASA DE INTERÉS ANUAL FIJA",
                     "Tipo de Crédito",
                     "MONTO DEL CRÉDITO",
                     "MONTO TOTAL A PAGAR",
                     "Nombre comercial del Producto"]
    
    # amortización
    interes_words = ["Sucursal", "Contrato", "Nombre del Cliente", "Fecha de Apertura", "Producto"]
    
    # CFE
    interes_words = ["CFE", "TOTAL A PAGAR", "CORTE A PARTIR", "LIMITE DE PAGO"]
    modelo_words = ["01 NOV 2022"]

    interes = get_vertices(annotations, interes_words)
    save_json(my_dict=interes, file_name=path.replace(".jpg","_interes.json"))
    interes =  [w["vert"] for w in interes]
    
    modelo = get_vertices(annotations, modelo_words)
    save_json(my_dict=modelo, file_name=path.replace(".jpg","_modelo.json"))
    modelo =  [w["vert"] for w in modelo]
    
    draw_image(path=path, modelo=modelo, interes=interes)