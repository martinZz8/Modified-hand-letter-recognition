import io
from os import listdir, mkdir
from os.path import dirname, isfile, isdir, join, exists
import subprocess


def main():
    # -- Defining folder names -- (these folder have to be created!)
    IMAGES_FN = join(dirname(__file__), "data", "images")
    SKELETONS_FN = join(dirname(__file__), "data", "skeletons")

    # Get inside folder names
    folder_names = [f for f in listdir(IMAGES_FN) if isdir(join(IMAGES_FN, f))]

    for fn_idx, folder_name in enumerate(folder_names):
        print(f"{fn_idx+1} of {len(folder_names)}")
        print(f"Processing folder: {folder_name} ...")

        # Determine files inside specific dir
        inner_folder_name = join(IMAGES_FN, folder_name)
        file_names = [f for f in listdir(inner_folder_name) if isfile(join(inner_folder_name, f))]
        file_names = list(filter(lambda x: (".png" in x) or (".jpg" in x) or (".jpeg" in x) or (".bmp" in x), file_names))

        # Create output folder in "data/skeletons" directory
        output_letter_folder = join(SKELETONS_FN, folder_name)

        if not exists(output_letter_folder):
            mkdir(output_letter_folder)

        # Process each file individually
        for idx, file_name in enumerate(file_names):
            print(f"{idx+1}) Processing file: {file_name} ...")
            # Get file_name without extension
            splitted_file_name = file_name.split(".")
            file_name_wo_ext = ".".join(splitted_file_name[0:(len(splitted_file_name)-1)])

            # Determine input image path and output skeleton path
            input_file_path = join(inner_folder_name, file_name)
            output_file_path = join(output_letter_folder, file_name_wo_ext + ".txt")

            # Run OpenPose exec
            path_to_exec = join(dirname(dirname(__file__)), "Python-eval-all", "single-classify", "functions", "skeletons", "OpenPose", "GetOpenPoseSkeleton.exe")
            cwd = dirname(path_to_exec)

            ls_output = subprocess.Popen([path_to_exec, input_file_path, output_file_path], cwd=cwd)
            ls_output.communicate()  # Will block for 30 seconds


if __name__ == "__main__":
    main()
    print("-- END OF 'main.py' SCRIPT --")
