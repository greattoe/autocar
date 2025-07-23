import os
import shutil

json_root = "dataset/images"
mask_output = "dataset/masks"
os.makedirs(mask_output, exist_ok=True)

for name in os.listdir(json_root):
    if name.endswith("_json"):
        json_folder = os.path.join(json_root, name)
        label_path = os.path.join(json_folder, "label.png")
        if os.path.exists(label_path):
            img_name = name.replace("_json", "") + ".png"
            dst_path = os.path.join(mask_output, img_name)
            shutil.copy(label_path, dst_path)
            print("Copied:", dst_path)

