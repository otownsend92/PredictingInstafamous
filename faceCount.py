__author__ = 'jhughes'
try:
    import cPickle as pickle
except:
    import pickle
import os
import cv2
face_cascade = None
face_counts = {}

#
# Initialize our face cascade
#
def initFaceCascade():
    global face_cascade
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#
# Detects largest face and draws and returns rectangle if found and enabled, takes grayscale image of currframe
#
def getFace(gray):
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=2, flags=(cv2.CASCADE_SCALE_IMAGE | cv2.CASCADE_FIND_BIGGEST_OBJECT))
    return faces

initFaceCascade()
for fn in os.listdir('./Images/'):
    img = cv2.imread('./Images/' + fn)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = getFace(gray)
    #for (x, y, w, h) in faces:
        #cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    #cv2.imshow("face image", img)
    #cv2.waitKey(0)
    print(str(len(faces)) + " faces found in: " + str(fn))
    face_counts[fn] = len(faces)

f = open('./Images/face_counts.txt', 'w')
pickle.dump(face_counts, f)
f.close()



