import os
import json
import time
import jmespath
from draw import draw_image

def read_json(path):
    f = open(path, encoding='utf-8')
    data = json.load(f)
    f.close()
    return data

def get_verts(path):
    verts  = read_json(path)
    return [w["vert"] for w in verts]

def flat(j):
    return jmespath.search("@[]", j)

def get_list_dirs():
    dir_path = r'resources'
    dirs = os.listdir(dir_path)
    return [d for d in dirs if "." not in d]

if __name__ == '__main__':    
    while True:
        dir_path = r'test'
        file_types = [".json", ".jpg", ".py"]
        dirs = os.listdir(dir_path)
        dirs = [d for d in dirs if ".json" in d]
        
        documentos = get_list_dirs()
        file_types = ["modelo", "interes"]
        for doc in documentos:
            try:
                modelo, interes = [get_verts(f'{dir_path}/{doc}_{ft}_updated.json') 
                                    for ft in file_types]
                draw_image(path=f'resources/{doc}/{doc}.jpg', modelo=modelo, interes=interes,
                        show=False, save=f'test/{doc}_test.jpg')
                print(doc)
            except Exception as e:
                print(e)
        time.sleep(3)