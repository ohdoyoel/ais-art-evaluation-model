import json
import os, shutil
from io import BytesIO
from PIL import Image

with open('/mnt/c/Users/ohdoy/workspace/ais-art-evaluation-model/data/google_arts_renaissance_5060.json', 'r') as f:
    json_data = json.load(f)

# print(json_data)

### GPT2

os.system("pip install streamlit==0.84.1")
os.system('pip install Pillow')
os.system('pip install jax[cpu]')
os.system('pip install flax')
os.system('pip install transformers')
os.system('pip install huggingface_hub')
os.system('pip install googletrans==4.0.0-rc1')
os.system('pip install protobuf==3.20')

import jax
from transformers import FlaxVisionEncoderDecoderModel, ViTFeatureExtractor, AutoTokenizer
from huggingface_hub import hf_hub_download

# create target model directory
model_dir = './models/'
os.makedirs(model_dir, exist_ok=True)

files_to_download = [
    "config.json",
    "flax_model.msgpack",
    "merges.txt",
    "special_tokens_map.json",
    "tokenizer.json",
    "tokenizer_config.json",
    "vocab.json",
    "preprocessor_config.json",
]

# copy files from checkpoint hub:
for fn in files_to_download:
    file_path = hf_hub_download("ydshieh/vit-gpt2-coco-en-ckpts", f"ckpt_epoch_3_step_6900/{fn}")
    shutil.copyfile(file_path, os.path.join(model_dir, fn))

model = FlaxVisionEncoderDecoderModel.from_pretrained(model_dir)
feature_extractor = ViTFeatureExtractor.from_pretrained(model_dir)
tokenizer = AutoTokenizer.from_pretrained(model_dir)

max_length = 16
num_beams = 4
gen_kwargs = {"max_length": max_length, "num_beams": num_beams}

@jax.jit
def generate(pixel_values):
    output_ids = model.generate(pixel_values, **gen_kwargs).sequences
    return output_ids

def caption_gpt2():
    img = Image.open('data/tmp.jpg')
    if img.mode != "RGB":
        img = img.convert(mode="RGB")
    print("a")
    pixel_values = feature_extractor(images=img, return_tensors="np").pixel_values
    print(pixel_values)
    output_ids = generate(pixel_values)
    print(output_ids)
    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    print(preds)
    preds = [pred.strip() for pred in preds]
    print(preds)

    return preds[0]








for i in range(1):
    # print(json_data[i]['img_url'])
    url = "https:" + json_data[i]['img_url']
    os.system("curl " + url + " > data/tmp.jpg")
    cap_g = caption_gpt2()
    # img = Image.open()

