import sys
from ComputeMAP import compute_map_scores


def main():
    args = sys.argv[1:]

    if len(args) != 3:
        print(
            "Error: Incorrect number of arguments.\nUsage:  ComputeMAP <input_folder_path> <output_folder_path> <frs_info_file_path>"
        )
        exit(1)

    input_folder_path = args[0]
    output_folder_path = args[1]
    frs_info_file_path = args[2]

    compute_map_scores(input_folder_path, output_folder_path, frs_info_file_path)


if __name__ == "__main__":
    main()
