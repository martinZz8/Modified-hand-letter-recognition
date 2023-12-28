# Standard imports
import sys
import cv2
import mediapipe as mp
from os.path import dirname, join as joinpath

sys.path.append(dirname(dirname(__file__)))
from exceptions.ErrorInputFileExtension import ErrorInputFileExtension
from exceptions.ErrorLandmarkDetection import ErrorLandmarkDetection


def hasFileNameProperExtension(fileName: str,
                               properFileExtensions: list[str]):
    isProper = False

    for fileExt in properFileExtensions:
        if fileExt in fileName:
            isProper = True
            break

    return isProper


# Note! use try...except block while running this function and want to skip images from which skeletons couldn't be determined
# Custom exceptions to handle: "ErrorInputFileExtension", "ErrorLandmarkDetection"
def getMediaPipeSk(input_image_file_path: str,
                   is_save_image_with_skeleton: bool = False,
                   is_draw_skeleton: bool = False):
    # -- Determine if "inputFileName" has proper extension --
    splitted_image_file_path = input_image_file_path.split("\\")
    input_file_name = splitted_image_file_path[len(splitted_image_file_path)-1]
    can_continue = hasFileNameProperExtension(input_file_name, [".png", ".jpg", ".jpeg", ".bmp"])

    if not can_continue:
        raise ErrorInputFileExtension("Input file doesn't have proper extension. Supported extensions: ['.png', '.jpg', '.jpeg', '.bmp']")

    # -- Constants definitions --
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands
    # 21 fingers enums (each has '.name' and '.value' property)
    list_of_fingers_enums = [
        mp_hands.HandLandmark.WRIST,
        mp_hands.HandLandmark.THUMB_CMC,
        mp_hands.HandLandmark.THUMB_MCP,
        mp_hands.HandLandmark.THUMB_IP,
        mp_hands.HandLandmark.THUMB_TIP,
        mp_hands.HandLandmark.INDEX_FINGER_MCP,
        mp_hands.HandLandmark.INDEX_FINGER_PIP,
        mp_hands.HandLandmark.INDEX_FINGER_DIP,
        mp_hands.HandLandmark.INDEX_FINGER_TIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_MCP,
        mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_DIP,
        mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
        mp_hands.HandLandmark.RING_FINGER_MCP,
        mp_hands.HandLandmark.RING_FINGER_PIP,
        mp_hands.HandLandmark.RING_FINGER_DIP,
        mp_hands.HandLandmark.RING_FINGER_TIP,
        mp_hands.HandLandmark.PINKY_MCP,
        mp_hands.HandLandmark.PINKY_PIP,
        mp_hands.HandLandmark.PINKY_DIP,
        mp_hands.HandLandmark.PINKY_TIP
    ]

    # -- General Options --
    is_save_skeleton_data = True  # (default: True)
    # is_save_image_with_skeleton = False  # (default: False)
    # is_draw_skeleton = False  # (default: False)

    # -- Algorithm options --
    static_image_mode = True  # (default: False)
    max_num_hands = 1  # (default: 2)
    min_detection_confidence = 0.5  # value in range [0; 1] (default: 0.5)
    detection_confidence_bottom_cap = 0.2
    model_complexity = 1  # 0 or 1 (default 1)

    # -- Defining folder names -- (these folder have to be created!)
    # IMAGES_FN = joinpath(
    #     dirname(
    #         dirname(
    #             dirname(
    #                 dirname(__file__)
    #             )
    #         )
    #     ),
    #     "input"
    # )
    IMAGES_FN = "\\".join(splitted_image_file_path[0:len(splitted_image_file_path)-1])

    SKELETONS_FN = joinpath(dirname(__file__), "outputTemp")

    # -- Starting proper script for points determination --
    # Perform it until skeleton is properly recognized - every time recognition fails, reduce 'min_detection_confidence' by 0.1 up to 0.0
    output_txt_file_path = ""
    processSkeletonRecognition = True

    with mp_hands.Hands(
            static_image_mode=static_image_mode,
            max_num_hands=max_num_hands,
            min_detection_confidence=min_detection_confidence,
            model_complexity=model_complexity
    ) as hands:
        # Get file_name without extension
        splitted_file_name = input_file_name.split(".")
        file_name_wo_ext = ".".join(splitted_file_name[0:(len(splitted_file_name)-1)])

        # Read an image, flip it around y-axis for correct handedness output (see above).
        input_file_path = joinpath(IMAGES_FN, input_file_name)
        image = cv2.flip(cv2.imread(input_file_path), 1)

        # Convert the BGR image to RGB before processing.
        converted_color_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        while processSkeletonRecognition:
            results = hands.process(converted_color_image)

            # Print handedness, determine shape of image and copy the image
            # print('Handedness:', results.multi_handedness)
            if not results.multi_hand_landmarks:
                print(f"Warning: No hand landmarks! 'min_detection_confidence'={min_detection_confidence}\nDecreasing value by 0.1")
                min_detection_confidence -= 0.1

                if min_detection_confidence < detection_confidence_bottom_cap:
                    raise ErrorLandmarkDetection(f"Error: Couldn't recognize hand landmark at 'min_detection_confidence'>={detection_confidence_bottom_cap}")

                # continue
            else:
                processSkeletonRecognition = False
                print(f"Got {len(results.multi_hand_landmarks[0].landmark)} points")

        image_height, image_width, _ = image.shape
        annotated_image = image.copy()

        # Save points for each hand
        for idx1, hand_landmarks in enumerate(results.multi_hand_landmarks):
            # Determine hand type ("Left", "Right")
            hand_type = results.multi_handedness[idx1].classification[0].label

            # Create 21x2 list
            hand_skeleton_points = [[0] * 2 for i in range(21)]

            # Fill hand_skeleton_points list
            for idx2, finger_enum in enumerate(list_of_fingers_enums):
                hand_skeleton_points[idx2][0] = round(hand_landmarks.landmark[finger_enum].x * image_width, 2)
                hand_skeleton_points[idx2][1] = round(hand_landmarks.landmark[finger_enum].y * image_height, 2)
            # print(f"hand_skeleton_points: {hand_skeleton_points}")

            # Draw landmarks
            if is_save_image_with_skeleton:
                mp_drawing.draw_landmarks(
                    annotated_image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style()
                )

            # Write hand skeleton data to .txt file
            if is_save_skeleton_data:
                # Form path for file
                output_txt_file_path = joinpath(SKELETONS_FN, file_name_wo_ext)

                if idx1 > 0:
                    output_txt_file_path += str(idx1)
                output_txt_file_path += ".txt"

                # Create file and save data to it
                with open(output_txt_file_path, mode="w", encoding="utf-8") as f:
                    for idx2, finger_point in enumerate(hand_skeleton_points):
                        for idx3, finger_point_coord in enumerate(finger_point):
                            val_to_save = str(finger_point_coord)
                            if idx3 != (len(finger_point) - 1):
                                val_to_save += " "
                            f.write(val_to_save)
                        if idx2 != (len(hand_skeleton_points) - 1):
                            f.write("\n")

        # Write image with landmarks
        if is_save_image_with_skeleton:
            output_image_file_path = joinpath(SKELETONS_FN, file_name_wo_ext + "_skeleton." + splitted_file_name[1])
            cv2.imwrite(output_image_file_path, cv2.flip(annotated_image, 1))

        # Draw hand world landmarks
        if results.multi_hand_world_landmarks and is_draw_skeleton:
            for hand_world_landmarks in results.multi_hand_world_landmarks:
                mp_drawing.plot_landmarks(hand_world_landmarks, mp_hands.HAND_CONNECTIONS, azimuth=5)
    print("End of 'getMediaPipeSk.py' function")

    return output_txt_file_path
