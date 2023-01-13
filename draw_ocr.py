import sys
import pandas as pd
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
    
    for idx in range(len(annotations)):        
        w = {}
        w["word"] = annotations[idx]["description"]
        
        # Indentificar palabras
        if w["word"] in single_words:
            count[w["word"]] = count[w["word"]] + 1
            v =  annotations[idx]["boundingPoly"]["vertices"][0]
            v1 = (v["x"], v["y"])
            v =  annotations[idx]["boundingPoly"]["vertices"][2]
            v2 = (v["x"], v["y"])
            
            w["vertices"] = [v1,v2]
            print(w)
            words.append(w)
        
        # Identificar frases
        for frase in frases:
            
            # Si la palabra actual no corresponde con a primera letra de la frase, nos saltamos este ciclo
            if w["word"] != frase[0]: continue
            
            # Creamos la frase de la misma longitud y preguntamos si es la misma de la origin
            frase_encontrada = [annotations[idx+idx_plus]["description"] for idx_plus in range(0, len(frase))]
            if frase != frase_encontrada: continue
            
            # Proceso básico de recuperación de indices 
            i = idx
            f = idx + len(frase) - 1
            count[' '.join(frase)] = count[' '.join(frase)] + 1
            v =  annotations[i]["boundingPoly"]["vertices"][0]
            v1 = [v["x"], v["y"]]
            v =  annotations[f]["boundingPoly"]["vertices"][2]
            v2 = [v["x"], v["y"]]
            
            w["word"] = ' '.join(frase)
            w["vertices"] = [v1,v2]
            print(w)
            words.append(w)  
            
    print(count)
 

    df = pd.DataFrame(words)
    df.to_csv(path.replace(".jpg", ".csv"), index=False, header=False)

    return [w["vertices"] for w in words]

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

if __name__ == "__main__":
    sys.stdin.reconfigure(encoding='utf-8')
    sys.stdout.reconfigure(encoding='utf-8')
    
    path = 'resources/caratula.jpg'
    path = 'resources/amortización.jpg'
    path = 'resources/CFE.jpg'

    annotations = ocr(path)
    
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
    modelo = get_vertices(annotations, modelo_words)
    
    draw_image(path=path, modelo=[], interes=interes)