import cv2,os
import numpy as np
from PIL import Image
import pickle, time

start_time = time.clock()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "image")

face_cascade = cv2.CascadeClassifier("cascades/haarcascade_frontalface_alt2.xml")
recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
y_labels = []
x_train = []

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith('png') or file.endswith('jpg'):
            path = os.path.join(root, file)
            label = os.path.basename(root).replace(' ', '-').lower()
            #print(label, path)
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1
            id_ = label_ids[label]
            print(label_ids)
            #y_labels.append(label) #some number
            #x_train.append(path) #подтверждение картинки
            pil_image = Image.open(path).convert('L')
            image_array = np.array(pil_image, 'uint8')
            print(image_array)
            faces = face_cascade.detectMultiScale(image_array, 1.3, 5)

            for x,y,w,h in faces:
                roi = image_array[y:y+h, x:x+w]
                x_train.append(roi)
                y_labels.append(id_)

print(y_labels)
print(x_train)

with open('labels.pickle', 'wb') as f:
    pickle.dump(label_ids, f)

recognizer.train(x_train, np.array(y_labels))
recognizer.save('trainner.yml')
print (time.clock() - start_time, "seconds")
