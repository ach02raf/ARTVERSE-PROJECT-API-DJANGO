from django.db import models
import cv2


def compareImage(img11, img22):
    img1 = cv2.imread(img11)
    img2 = cv2.imread(img22)
    sift = cv2.SIFT_create()
    des1 = sift.detectAndCompute(img1, None)
    des2 = sift.detectAndCompute(img2, None)

    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)

    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append([m])

    if len(good_matches) > 10:
        return "true"
    else:
        return "false"
