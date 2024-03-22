import os
import shutil

import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from supervisely.imaging.color import get_predefined_colors
from supervisely.io.fs import (
    file_exists,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
)
from tqdm import tqdm

import src.settings as s


def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:
    # Possible structure for bbox case. Feel free to modify as you needs.

    dataset_path = "/home/alex/DATASETS/TODO/ArSL21L"
    train_path = "/home/alex/DATASETS/TODO/ArSL21L/data/train.txt"
    val_path = "/home/alex/DATASETS/TODO/ArSL21L/data/val.txt"
    batch_size = 30
    images_ext = ".jpg"
    ann_ext = ".txt"

    def create_ann(image_path):
        labels = []

        # image_np = sly.imaging.image.read(image_path)[:, :, 0]
        img_height = 416  # image_np.shape[0]
        img_wight = 416  # image_np.shape[1]

        ann_path = image_path.replace("images", "labels").replace(images_ext, ann_ext)

        if file_exists(ann_path):
            with open(ann_path) as f:
                content = f.read().split("\n")

                for curr_data in content:
                    if len(curr_data) != 0:
                        curr_data = list(map(float, curr_data.split(" ")))
                        obj_class = idx_to_class[curr_data[0]]

                        left = int((curr_data[1] - curr_data[3] / 2) * img_wight)
                        right = int((curr_data[1] + curr_data[3] / 2) * img_wight)
                        top = int((curr_data[2] - curr_data[4] / 2) * img_height)
                        bottom = int((curr_data[2] + curr_data[4] / 2) * img_height)
                        rectangle = sly.Rectangle(top=top, left=left, bottom=bottom, right=right)
                        label = sly.Label(rectangle, obj_class)
                        labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)

    classes_names = [
        "ain",
        "al",
        "aleff",
        "bb",
        "dal",
        "dha",
        "dhad",
        "fa",
        "gaaf",
        "ghain",
        "ha",
        "haa",
        "jeem",
        "kaaf",
        "khaa",
        "la",
        "laam",
        "meem",
        "nun",
        "ra",
        "saad",
        "seen",
        "sheen",
        "ta",
        "taa",
        "thaa",
        "thal",
        "toot",
        "waw",
        "ya",
        "yaa",
        "zay",
    ]

    idx_to_class = {}

    obj_classes = [
        sly.ObjClass(name, sly.Rectangle, color)
        for name, color in zip(classes_names, get_predefined_colors(len(classes_names)))
    ]

    for idx, obj_class in enumerate(obj_classes):
        idx_to_class[idx] = obj_class

    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(obj_classes=list(idx_to_class.values()))
    api.project.update_meta(project.id, meta.to_json())

    for split_path in [train_path, val_path]:

        ds_name = get_file_name(split_path)

        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        with open(split_path) as f:
            content = f.read().split("\n")

        images_pathes = [
            os.path.join(dataset_path, im_subpath) for im_subpath in content if len(im_subpath) > 1
        ]

        images_pathes = [im_path for im_path in images_pathes if file_exists(im_path)]

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_pathes))

        for images_pathes_batch in sly.batched(images_pathes, batch_size=batch_size):
            images_names_batch = [
                get_file_name_with_ext(image_path) for image_path in images_pathes_batch
            ]

            img_infos = api.image.upload_paths(dataset.id, images_names_batch, images_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            anns = [create_ann(image_path) for image_path in images_pathes_batch]
            api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(images_names_batch))

    return project
