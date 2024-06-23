import os
import json
import numpy as np
import MAP


def load_frs_score_dict_from_file(file_path):
    with open(file_path) as f:
        lines = f.readlines()

    frs_score_dict = {}
    for l in lines:
        line = l.strip()
        splitted_line = line.split("\t")
        morphed_image_name = splitted_line[0]

        if morphed_image_name in frs_score_dict:
            morphed_image_score_dict = frs_score_dict[morphed_image_name]
        else:
            morphed_image_score_dict = {}
            frs_score_dict[morphed_image_name] = morphed_image_score_dict

        subject_id = splitted_line[1]
        subject_scores = [float(s) for s in splitted_line[2:]]
        morphed_image_score_dict[subject_id] = subject_scores

    return frs_score_dict


def check_score_dict_consistency(frs_score_dict_list):
    for frs_score_dict in frs_score_dict_list[1:]:
        if frs_score_dict_list[0].keys() != frs_score_dict.keys():
            raise ValueError(
                "Error: not all files contain the scores of the same morphed images"
            )

        for morphed_image_name in frs_score_dict_list[0]:
            if set(frs_score_dict_list[0][morphed_image_name].keys()) != set(
                frs_score_dict[morphed_image_name].keys()
            ):
                raise ValueError(
                    "Error: not all files contain the same subject attempts"
                )

            for subject_id in frs_score_dict_list[0][morphed_image_name]:
                if len(frs_score_dict_list[0][morphed_image_name][subject_id]) != len(
                    frs_score_dict[morphed_image_name][subject_id]
                ):
                    raise ValueError(
                        f"Error: not all files contain the same number of scores for the morphed image {morphed_image_name} and the subject {subject_id}"
                    )


def print_map(map):
    attempt_count, frs_count = map.shape
    for frs_idx in range(frs_count):
        print("\t{}".format(frs_idx + 1), end="")
    print()

    for attempt_idx in range(attempt_count):
        print("{}".format(attempt_idx + 1), end="")
        for frs_idx in range(frs_count):
            print("\t{:.1%}".format(map[attempt_idx, frs_idx]), end="")
        print()


def save_map_to_text_file(file_path, map, morph_image_count):
    attempt_count, frs_count = map.shape
    with open(file_path, "w") as f:
        for frs_idx in range(frs_count):
            f.write("\t{}".format(frs_idx + 1))
        f.write("\n")

        for attempt_idx in range(attempt_count):
            f.write("{}".format(attempt_idx + 1))
            for frs_idx in range(frs_count):
                f.write("\t{:.1%}".format(map[attempt_idx, frs_idx]))
            f.write("\n")
        f.write("Image count:\t{}".format(morph_image_count))


def compute_map_scores(input_folder_path, output_folder_path, frs_info_file_path):
    frs_infos = json.load(open(frs_info_file_path, "r"))

    print("Log: Loading scores in progress...")
    frs_score_dict_list = []
    frs_thr_list = []
    frs_is_similarity_list = []
    for frs_name in frs_infos:
        input_file_path = os.path.join(input_folder_path, f"{frs_name}.txt")
        frs_score_dict_list.append(load_frs_score_dict_from_file(input_file_path))
        frs_thr_list.append(frs_infos[frs_name][0])
        frs_is_similarity_list.append(frs_infos[frs_name][1])
    print("Log: Loading scores finished.")

    print("Log: Score consistency check in progress...")
    check_score_dict_consistency(frs_score_dict_list)
    print("Log: Score consistency check finished.")

    print("Log: MAP computation in progress...")
    map, map_count = MAP.compute_map(
        frs_score_dict_list, frs_thr_list, frs_is_similarity_list
    )
    print("Log: MAP computation finished.")
    print("===============")
    print("MAP:")
    print_map(map)
    print("===============")

    save_map_to_text_file(
        os.path.join(output_folder_path, "MAP.txt"),
        map,
        len(frs_score_dict_list[0].keys()),
    )
    save_map_to_text_file(
        os.path.join(output_folder_path, "MAPCount.txt"),
        map_count,
        len(frs_score_dict_list[0].keys()),
    )
