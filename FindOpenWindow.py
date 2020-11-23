import cv2
import numpy as np


def align(img1, img2, src, dst):  # make img2 (src) align to img1 (dst)
    height = img2.shape[0]
    width = img2.shape[1]
    m = cv2.getPerspectiveTransform(src, dst)
    result = cv2.warpPerspective(img2, m, (width, height))
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
    ret1, gray1 = cv2.threshold(gray1, 110, 255, cv2.THRESH_BINARY)  # binarization
    ret2, gray2 = cv2.threshold(gray2, 110, 255, cv2.THRESH_BINARY)
    img = gray1 - gray2
    less_than_0 = (img < 0)
    img[less_than_0] = 0
    flag = (img == 0).astype(int)
    return img, flag


def get_mode(array):
    temp = np.concatenate(array.reshape(1, -1))
    counts = np.bincount(temp)
    return np.argmax(counts)


WindowOpen = cv2.imread('WindowOpen.jpg')
WindowClosed = cv2.imread('WindowClosed.jpg')
Copy = WindowOpen.copy()
HEIGHT = WindowOpen.shape[0]
WIDTH = WindowOpen.shape[1]
OrigB, OrigG, OrigR = cv2.split(WindowOpen)

src1 = np.float32([[245, 322], [359, 275], [386, 812], [720, 1104]])
dst1 = np.float32([[116, 319], [236, 272], [254, 826], [591, 1114]])
detection1, flag1 = align(WindowOpen, WindowClosed, src1, dst1)

src2 = np.float32([[265, 890], [379, 844], [436, 915], [373, 1130]])
dst2 = np.float32([[126, 907], [249, 859], [307, 933], [239, 1155]])
detection2, flag2 = align(WindowOpen, WindowClosed, src2, dst2)

src3 = np.float32([[451, 253], [449, 355], [525, 183], [602, 345]])
dst3 = np.float32([[331, 259], [327, 363], [409, 194], [484, 360]])
detection3, flag3 = align(WindowOpen, WindowClosed, src3, dst3)

src4 = np.float32([[264, 969], [264, 1003], [343, 959], [343, 993]])
dst4 = np.float32([[126, 988], [124, 1024], [208, 977], [210, 1014]])
detection4, flag4 = align(WindowOpen, WindowClosed, src4, dst4)

src5 = np.float32([[436, 916], [582, 1010], [437, 952], [575, 1055]])
dst5 = np.float32([[308, 932], [457, 1024], [309, 967], [449, 1071]])
detection5, flag5 = align(WindowOpen, WindowClosed, src5, dst5)

DETECTION = detection1.copy()
FLAG = (flag1 + flag2 + flag3 + flag4 + flag5).astype(bool)
DETECTION[FLAG] = 0
temp = WindowOpen.copy()
contours, hierarchy = cv2.findContours(DETECTION, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for i in range(0, len(contours)):
    x, y, w, h = cv2.boundingRect(contours[i])
    if (w > 5) and (h > 6) and (w < 20) and (h < 30):
        cv2.rectangle(temp, (x, y), (x + w, y + h), (0, 0, 255), 20)

Blue, Green, Red = cv2.split(temp)
for i in range(0, HEIGHT):
    for j in range(0, WIDTH):
        if (Blue[i, j] == 0) and (Green[i, j] == 0) and (Red[i, j] == 255):
            Blue[i, j] = 255
            Green[i, j] = 255
        else:
            Blue[i, j] = 0
            Green[i, j] = 0
            Red[i, j] = 0
Region = cv2.merge([Blue, Green, Red])
Region = cv2.cvtColor(Region, cv2.COLOR_BGR2GRAY)
contours, hierarchy = cv2.findContours(Region, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for i in range(0, len(contours)):
    x, y, w, h = cv2.boundingRect(contours[i])
    array = OrigR[y:y + h, x:x + w]
    if get_mode(array) < 100:
        if (w > 50) and (w < 70) and (h > 50) and (h < 70):
            cv2.rectangle(Copy, (x, y), (x + w, y + h), (0, 0, 255), 2)

cv2.imshow('BinaryImg', DETECTION)
cv2.imshow('OpenWindow', Copy)
cv2.waitKey(0)
cv2.destroyAllWindows()
