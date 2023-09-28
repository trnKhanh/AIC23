import fiftyone as fo
import fiftyone.zoo as foz
import fiftyone.brain as fob
import numpy as np

dataset = fo.Dataset.from_images_patt("./data/keyframes/*/*.jpg", name=None, tags=None)
session = fo.launch_app(dataset, desktop=False)

import os
import csv
import pandas as pd

info = dict()
for file in os.scandir("map-keyframes"):
    if file.name[0] == '.':
        continue
    videoId = file.name.split(".")[0]
    data = pd.read_csv(file.path)
    info[videoId] = data.to_dict()

import json
print("", end="", flush=True)
for sample in dataset:
    if "checkpoint" in sample["filepath"]:
        continue
    print(f"\r{sample['filepath']} is being processed", end="", flush=True)
    videoId, frameId = sample["filepath"].split("/")[-2:]
    videoId = videoId.split(".")[0]
    frameId = frameId.split(".")[0]
    object_file = f"./objects/{videoId}/{frameId}.json"
    frameId = int(frameId)
    sample["videoId"] = videoId
    sample["n"] = str(info[videoId]['n'][frameId-1])
    sample["frameId"] = str(info[videoId]['frame_idx'][frameId-1])
    sample["pts_time"] = str(info[videoId]['pts_time'][frameId-1])

    f = open(object_file)
    data = json.load(f)
    detections = []
    for id in range(len(data["detection_class_entities"])):
        if float(data["detection_scores"][id]) < 0.5:
            continue;
        detections.append(
            fo.Detection(
                label=data["detection_class_entities"][id],
                bounding_box=data["detection_boxes"][id],
                confidence=data["detection_scores"][id],
            )
        )
    sample["prediction"] = fo.Detections(detections=detections)
    sample.save()

embeddings = np.load("./embeddings/keyframes.npy")

results = fob.compute_visualization(
    dataset,
    embeddings=embeddings,
    seed=51,
    brain_key="img_viz"
)
print("Finish computing visualization")
image_index = fob.compute_similarity(
    dataset,
    model="clip-vit-base32-torch",
    embeddings=embeddings,
    brain_key="img_sim",
)
print("Finish computing similarity")
session.wait()