import cv2
import numpy as np

"""
REFER: https://hub.packtpub.com/opencv-detecting-edges-lines-shapes/
"""


def _draw_contours(img, cnts):  # conts = contours
    img = np.copy(img)
    img = cv2.drawContours(img, cnts, -1, (0, 255, 0), 2)
    return img


def _draw_min_rect_circle(img, cnts):  # conts = contours
    img = np.copy(img)

    for cnt in cnts:
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)  # blue

        min_rect = cv2.minAreaRect(cnt)  # min_area_rectangle
        min_rect = np.int0(cv2.boxPoints(min_rect))
        cv2.drawContours(img, [min_rect], 0, (0, 255, 0), 2)  # green

        (x, y), radius = cv2.minEnclosingCircle(cnt)
        # center and radius of minimum enclosing circle
        center, radius = (int(x), int(y)), int(radius)
        img = cv2.circle(img, center, radius, (0, 0, 255), 2)  # red
    return img


def CalcMoveOffsetSimple(image_path, max_offset=280):
    image = cv2.imread(image_path)
    ratio = max_offset/image.shape[1]
    gray = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2GRAY)
    # ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    thresh = cv2.Canny(gray, 128, 255)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    # Normally the contour with max area matchs small slider
    contours_area = [cv2.contourArea(c) for c in contours]
    contour_match = contours[np.argmax(contours_area)]
    x, y, w, h = cv2.boundingRect(contour_match)
    return int(x*ratio)


def CalcMoveOffset(origin_path, template_path, max_offset=280):
    origin_img = cv2.imread(origin_path, 0)
    template_img = cv2.imread(template_path, 0)

    # crop image
    # print(template_img)
    template_img_arr = np.copy(template_img)
    template_pos = np.where(template_img_arr > 0)
    x_t, x_b = np.min(template_pos[0]), np.max(template_pos[0])
    y_t, y_b = np.min(template_pos[1]), np.max(template_pos[1])

    template_img = template_img[x_t:x_b, y_t:y_b]
    top_left, _ = match_template(origin_img, template_img)

    ratio = max_offset/origin_img.shape[1]
    return int(top_left[0]*ratio)


def match_template(origin, template):
    w, h = template[::-1].shape
    # All the 6 methods for comparison in a list
    # methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
    #             'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    method = cv2.TM_SQDIFF_NORMED
    # Apply template Matching
    res = cv2.matchTemplate(origin, template, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    return top_left, bottom_right


if __name__ == '__main__':
    res = CalcMoveOffset("origin.png", "./temlate.png", 280)
    print(res)
