from save_drawings import flat, read_json 
import os

def modify_all_verts(verts, add=[[0,0],[0,0]], p=0):
    nx1, ny1, nx2, ny2 = flat(add)
    for vert in verts:
        x1, y1, x2, y2 = flat(vert["vert"])
        a = int((x2-x1)*p/2) 
        x1 -= (a+nx1); x2 += (a+nx2)
        a = int((y2-y1)*p/2)
        y1 -= (a+ny1); y2 += (a+ny2)
        vert["vert"] = [[x1,y1],[x2,y2]]
        
def pprint_json(j):
    '''
    "word": "21066",
    "vert": [[541,8],[567,16]]
    '''
    l = len(j) - 1
    p = '['
    for i, e in enumerate(j):
        coma = "," if i != l else ""
        word = e["word"]
        vert = str(e["vert"])
        p +=  '\n    {'
        p += f'\n        "word" : "{word}",'
        p += f'\n        "vert" : {vert}'
        p +=  '\n    }' + coma
    p += '\n]'
    return p

def write_json(text, path):
    json_file = open(path, "w", encoding='utf-8')
    json_file.write(text)
    json_file.close()

def get_list_dirs():
    dir_path = r'resources'
    dirs = os.listdir(dir_path)
    return [d for d in dirs if "." not in d]


if __name__ == '__main__':
    file_types = ["modelo", "interes"]
    file_types = ["interes"]
    docs = get_list_dirs()
    docs = ["caratula", "CFE", "SEGURO_DESEMPLEO",
            "SOLICITUD", "SEGURO_GENERAL", "IZZI",
            "CURP", "disposicion", "TABLA_AMORTIZACION",
            "INE_1", "SEGURO_INTEGRAL"]
    docs = ["TABLA_AMORTIZACION"]
    
    for fn in docs:
        for ft in file_types:
            path = f'resources/{fn}/{fn}_{ft}.json'
            path = f'test/{fn}_{ft}_updated.json'
            p = read_json(path)
            modify_all_verts(p, add=[[0,1],[0,1]], p=0)
            p = pprint_json(p)
            print(p)
            path = f'test/{fn}_{ft}_updated.json'
            write_json(text=p, path=path)
