# Copyright (C) 2022  Tiernan8r
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Based on code originally from
# https://pyimagesearch.com/2014/09/01/build-kick-ass-mobile-document-scanner-just-5-minutes/

import sys

import cv2
import imutils

from transform import four_point_transform

# from skimage.filters import threshold_local



def scan(path):
    image = read_image(path)
    image, orig, ratio = reshape(image)
    edged = detect_edges(image)
    screen_contours = find_contours(edged)
    warped = perspective_transform(image, screen_contours, orig, ratio)

    show_result(orig, warped)


def read_image(path):
    image = cv2.imread(path)

    return image


def reshape(image):
    # compute the ratio of the old height
    # to the new height, clone it, and resize it
    ratio = image.shape[0] / 500.0
    orig = image.copy()
    image = imutils.resize(image, height=500)

    return image, orig, ratio


def detect_edges(image):
    # convert the image to greyscale, blur it, and find edges
    # in the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
    # show the original image and the edge detected image
    print("STEP 1: Edge Detection")
    # cv2.imshow("Image", image)
    img_stat = cv2.imwrite("./out/image.JPEG", image)
    print("input image written successfully:", img_stat)
    # cv2.imshow("Edged", edged)
    img_stat = cv2.imwrite("./out/edged.JPEG", edged)
    print("edged image written successfully:", img_stat)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return edged


def find_contours(edged):
    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:5]

    screenCnt = None
    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break

    if screenCnt is None:
        print("Contours not found!")
        sys.exit(1)

    return screenCnt


def perspective_transform(image, screenCnt, orig, ratio):
    # show the contour (outline) of the piece of paper
    print("STEP 2: Find contours of paper")
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    # cv2.imshow("Outline", image)
    cv2.imwrite("out/outline.JPEG", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # apply the four point transform to obtain a top-down
    # view of the original image
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    # convert the warped image to greyscale, then threshold it
    # to give it that 'black and white' paper effect
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    # T = threshold_local(warped, 11, offset=10, method="gaussian")
    # warped = (warped > T).astype("uint8") * 255

    return warped


def show_result(orig, warped):
    # show the original and scanned images
    print("STEP 3: Apply perspective transform")
    # cv2.imshow("Original", imutils.resize(orig, height = 650))
    cv2.imwrite("out/original.JPEG", imutils.resize(orig, height=650))
    # cv2.imshow("Scanned", imutils.resize(warped, height = 650))
    cv2.imwrite("out/scanned.JPEG", imutils.resize(warped, height=650))
    # cv2.waitKey(0)
