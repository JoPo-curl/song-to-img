import json
import requests
import os
import re 
import io
import base64
import shutil
import re 
from PIL import Image, PngImagePlugin

url = "http://127.0.0.1:7860"
negative_prompt = "(worst quality, low quality:1.3), (depth of field, blurry:1.2), (greyscale, monochrome:1.1), 3D face, nose, cropped, lowres, text, jpeg artifacts, signature, watermark, username, blurry, artist name, trademark, watermark, title, (tan, muscular, loli, petite, child, infant, toddlers, chibi, sd character:1.1), multiple view, Reference sheet"


def run_prompt(prompt, song_name):
    run_image(prompt, 20, 3 ,song_name)
    run_image(prompt, 28, 3 ,song_name)
    run_image(prompt, 60, 3 ,song_name)
    run_image(prompt, 20, 6 ,song_name)
    run_image(prompt, 28, 6 ,song_name)
    run_image(prompt, 60, 6 ,song_name)
    run_image(prompt, 20, 9 ,song_name)
    run_image(prompt, 28, 9 ,song_name)
    run_image(prompt, 60, 9 ,song_name)
    run_image(prompt, 20, 12 ,song_name)
    run_image(prompt, 28, 12 ,song_name)
    run_image(prompt, 60, 12 ,song_name)

def run_image(prompt, steps, cfg, song_name):
    payload = {
        "prompt": f'{prompt}',
        "steps": f'{steps}',
        "seed": -1,
        "cfg_scale": f'{cfg}',
        "width": 768,
        "height": 512,
        "negative_prompt": f'{negative_prompt}'
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    #Steps: 60, Sampler: Euler, CFG scale: 12.0, Seed: 2609975445
    r = response.json()

    print(r)
    for i in r['images']:
        info_str = str(r["info"])
        reg_str = "Seed: \d*"
        seed_str = re.search(reg_str, info_str).group(0)
        seed_str_done = seed_str.replace(":","-")
        output_file_name = song_name+"-cfg-"+str(r["parameters"]["cfg_scale"])+"-steps-"+str(r["parameters"]["steps"])+"-seed-"+seed_str_done
        print("xxxxxx")
        print(output_file_name)
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        print("xxxxxx")
        print(f'output/{output_file_name}.png')
        image.save(f'output/{output_file_name}.png', pnginfo=pnginfo)

def load_songs(directory):
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(f):
            print(f)
            file_read = open(f, "r")    
            raw_song = file_read.read()
            run_prompt(raw_song, filename)
            file_read.close()
            shutil.move(os.path.join(directory, filename), f'lyrics/done/{filename}')

load_songs("lyrics")
