import dlib
from PIL import Image, ImageDraw, ImageFont
import cv2
from imutils.video import VideoStream
from imutils import face_utils, translate, rotate, resize
from playsound import playsound
from moviepy.editor import *

import numpy as np

vs = VideoStream().start()

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')

max_width = 500
frame = vs.read()
frame = resize(frame, width=max_width)

fps = vs.stream.get(cv2.CAP_PROP_FPS) # need this for animating proper duration

animation_length = fps * 8
current_animation = 0
glasses_on = fps * 6
output_frames=[]

# uncomment for fullscreen, remember 'q' to quit
# cv2.namedWindow('deal generator', cv2.WND_PROP_FULLSCREEN)
#cv2.setWindowProperty('deal generator', cv2.WND_PROP_FULLSCREEN,
#                          cv2.WINDOW_FULLSCREEN)

deal = Image.open("Assets/deals.png")
text = Image.open('Assets/text.png')

dealing = False

while True:
    frame = vs.read()

    frame = resize(frame, width=max_width)

    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = []

    rects = detector(img_gray, 0)
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    for rect in rects:
        face = {}
        shades_width = rect.right() - rect.left()

        # predictor used to detect orientation in place where current face is
        shape = predictor(img_gray, rect)
        shape = face_utils.shape_to_np(shape)

        # grab the outlines of each eye from the input image
        leftEye = shape[36:42]
        rightEye = shape[42:48]

        # compute the center of mass for each eye
        leftEyeCenter = leftEye.mean(axis=0).astype("int")
        rightEyeCenter = rightEye.mean(axis=0).astype("int")

	    # compute the angle between the eye centroids
        dY = leftEyeCenter[1] - rightEyeCenter[1]
        dX = leftEyeCenter[0] - rightEyeCenter[0]
        angle = np.rad2deg(np.arctan2(dY, dX))

        current_deal = deal.resize((shades_width, int(shades_width * deal.size[1] / deal.size[0])),
                               resample=Image.LANCZOS)
        current_deal = current_deal.rotate(angle, expand=True)
        current_deal = current_deal.transpose(Image.FLIP_TOP_BOTTOM)

        face['glasses_image'] = current_deal
        left_eye_x = leftEye[0,0] - shades_width // 4
        left_eye_y = leftEye[0,1] - shades_width // 6
        face['final_pos'] = (left_eye_x, left_eye_y)

        if dealing:
            if current_animation < glasses_on:
                current_y = int(current_animation / glasses_on * left_eye_y)
                img.paste(current_deal, (left_eye_x, current_y), current_deal)
            else:
                img.paste(current_deal, (left_eye_x, left_eye_y), current_deal)
                img.paste(text, (75, img.height-100 ), text)

    if dealing:
        current_animation += 1
        if current_animation > animation_length:
            dealing = False
            current_animation = 0
            clip = ImageSequenceClip(output_frames, fps)
            clip.write_videofile("movie.mp4", audio='Assets/dealwithit.m4a',codec='mpeg4')
            output_frames = []
        else:
            frame = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
            output_frames.append(np.asarray(img))


    cv2.imshow("Meme Generator", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

    if key == ord("d"):
        dealing = not dealing
        if dealing:
            playsound('Assets/dealwithit.m4a', 0)



cv2.destroyAllWindows()
vs.stop()
