import cv2

# LOAD
img = cv2.imread("image.jpg")

print("Shape:", img.shape)

cv2.imshow("Image", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# RESIZE
img = cv2.imread("image.jpg")
resized = cv2.resize(img, (224, 224))
print(resized.shape)

# GRAYSCALE
img = cv2.imread("image.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

cv2.imshow("Gray", gray)
cv2.waitKey(0)
cv2.destroyAllWindows()

# THRESHOLD
img = cv2.imread("image.jpg", 0)

_, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)

cv2.imshow("Threshold", thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

# FACE DETECTION
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

img = cv2.imread("image.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.1, 4)

for (x, y, w, h) in faces:
    cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)

cv2.imshow("Faces", img)
cv2.waitKey(0)
cv2.destroyAllWindows()