import os
import cv2 as cv
import numpy as np
import mediapipe as mp
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils
def train():
# folder titles of training images
    people = ["me", "not me"]
    # get path to haar cascade and images
    DIR =r'Face Recognition App\images, training'
    features = []
    labels = []
    with mp_face_detection.FaceDetection(
        model_selection=1, min_detection_confidence=0.5) as face_detection:
    # go through folders
        for filename in people:
            path = os.path.join(DIR, filename)
            label = people.index(filename)
            # go through images within folder
            for img in os.listdir(path):
                # turn images into numeric arrays
                img_path = os.path.join(path, img)
                img_array = cv.imread(img_path)
                # handle errors in imread
                if img_array is None:
                    continue
                img_array.flags.writeable = False
                img_array = cv.cvtColor(img_array, cv.COLOR_BGR2RGB)
                results = face_detection.process(img_array)
                    # Draw the face detection annotations on the image.
                img_array.flags.writeable = True
                img_array = cv.cvtColor(img_array, cv.COLOR_RGB2BGR)
                img_height, img_width, _ = img_array.shape
                gray = cv.cvtColor(img_array, cv.COLOR_BGR2GRAY)
                if results.detections:
                    for detection in results.detections:   
                        mp_drawing.draw_detection(img_array, detection)
                        x = int(min(detection.location_data.relative_bounding_box.xmin, 1) * img_width)
                        y = int(min(detection.location_data.relative_bounding_box.ymin, 1) * img_height)
                        x_max = int(min(detection.location_data.relative_bounding_box.xmin + detection.location_data.relative_bounding_box.width, 1) * img_width)
                        y_max = int(min(detection.location_data.relative_bounding_box.ymin + detection.location_data.relative_bounding_box.height, 1) * img_height)
                        faces_crop = gray[y:y_max,x:x_max]
                        if 0 in faces_crop.shape:
                            continue
                        features.append(faces_crop)
                     # append classification
                        labels.append(label)
        features = np.array(features, dtype='object')
        labels = np.array(labels)
        # create model for face classification
        face_recognizer = cv.face.LBPHFaceRecognizer_create()
        # train model
        face_recognizer.train(features,labels)
        # save model data
        face_recognizer.save('face_trained.yml')
        np.save('features.npy', features)
        np.save('labels.npy', labels)