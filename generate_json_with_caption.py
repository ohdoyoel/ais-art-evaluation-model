import json
import os
from io import BytesIO
from PIL import Image

with open('/mnt/c/Users/ohdoy/workspace/ais-art-evaluation-model/data/google_arts_renaissance_5060.json', 'r') as f:
    json_data = json.load(f)

# print(json_data)

### GPT2



def caption_gpt2():
    img = Image.open('data/tmp.jpg')
    if img.mode != "RGB":
        img = img.convert(mode="RGB")
    pixel_values = feature_extractor(images=img, return_tensors="np").pixel_values
    output_ids = generate(pixel_values)
    preds = tokenizer.batch_decode(output_ids, skip_special_tokens=True)
    preds = [pred.strip() for pred in preds]

    return preds[0]








for i in range(1):
    # print(json_data[i]['img_url'])
    url = "https:" + json_data[i]['img_url']
    os.system("curl " + url + " > data/tmp.jpg")
    cap_g = caption_gpt2()
    # img = Image.open()

