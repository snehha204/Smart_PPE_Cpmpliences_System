"""this script creates a smaller dataset by randomly sampling images and their 
corresponding labels from the original dataset."""
import os
import random
import shutil

source = "helm"
dest = "helm_small"

train_count = 1200
val_count = 200
test_count = 200

def copy_data(split, count):
    img_src = f"{source}/images/{split}"
    lbl_src = f"{source}/labels/{split}"

    img_dst = f"{dest}/{split}/images"
    lbl_dst = f"{dest}/{split}/labels"

    os.makedirs(img_dst, exist_ok=True)
    os.makedirs(lbl_dst, exist_ok=True)

    all_files = os.listdir(img_src)

    # keep only image files
    images = []
    for f in all_files:
        if f.lower().endswith((".jpg", ".png", ".jpeg")):
            images.append(f)

    print(f"{split} total images found:", len(images))

    selected = random.sample(images, min(count, len(images)))

    copied = 0

    for img in selected:
        base = os.path.splitext(img)[0]
        label = base + ".txt"

        src_img = f"{img_src}/{img}"
        src_lbl = f"{lbl_src}/{label}"

        dst_img = f"{img_dst}/{img}"
        dst_lbl = f"{lbl_dst}/{label}"

        if os.path.exists(src_img):
            shutil.copy2(src_img, dst_img)

        if os.path.exists(src_lbl):
            shutil.copy2(src_lbl, dst_lbl)
            copied += 1

    print(f"✅ {split}: {copied} labels copied")

copy_data("train", train_count)
copy_data("valid", val_count)
copy_data("test", test_count)

print("🎉 DONE")