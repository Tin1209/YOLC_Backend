# 라즈베리파이로 받은 image에서 blink detection이후 저장된 6장의 embedded vector를 사용해 face recognition 진행
import cv2, dlib
import numpy as np
from imutils import face_utils
from keras.models import load_model
from .face_registration import *
import base64
from PIL import Image
from io import BytesIO

class Want_enter():

    IMG_SIZE = (34,26)
    blink_detection = False
    face_recognition = True
    prev_l, prev_r = [], []
    steps, blink_l, blink_r, blink_count = 0, 0, 0, 0
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('/home/hin/YOLC/ccpApi/accounts/shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('/home/hin/YOLC/ccpApi/accounts/dlib_face_recognition_resnet_model_v1.dat')
    descs = np.load('/home/hin/YOLC/ccpApi/accounts/img/descs.npy', allow_pickle=True)[()] # 6장의 정답 image들에 대한 embedded vector가 저장된 파일
    model = load_model('/home/hin/YOLC/ccpApi/accounts/models/2018_12_17_22_58_35.h5')



    def crop_eye(img, eye_points):
        x1, y1 = np.amin(eye_points, axis=0)
        x2, y2 = np.amax(eye_points, axis=0)
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

        w = (x2 - x1) * 1.2
        h = w * IMG_SIZE[1] / IMG_SIZE[0]

        margin_x, margin_y = w / 2, h / 2

        min_x, min_y = int(cx - margin_x), int(cy - margin_y)
        max_x, max_y = int(cx + margin_x), int(cy + margin_y)

        eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(int)

        eye_img = gray[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]

        return eye_img, eye_rect

    def check_face(self,img_list):
        steps = 0
        for img_ori in img_list:
            img_ori = Image.open(BytesIO(base64.b64decode(img_ori)))
            img_ori = np.array(img_ori)
            img_ori = cv2.resize(img_ori, dsize=(0, 0), fx=0.5, fy=0.5)
            img = img_ori.copy()

            if self.blink_detection:    
                print("blink")
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                faces = self.detector(gray)
                steps += 1

                for face in faces:
                    shapes = predictor(gray, face) # detect face from camera
                    shapes = face_utils.shape_to_np(shapes) # change form into numpy

                    eye_img_l, eye_rect_l = crop_eye(gray, eye_points=shapes[36:42]) # find left eyes and crop
                    eye_img_r, eye_rect_r = crop_eye(gray, eye_points=shapes[42:48]) # find rigth eyes and crop

                    eye_img_l = cv2.resize(eye_img_l, dsize=IMG_SIZE) # resize eyes
                    eye_img_r = cv2.resize(eye_img_r, dsize=IMG_SIZE) # resize eyes
                    eye_img_r = cv2.flip(eye_img_r, flipCode=1) # flip right eyes, so it can fit in model to predict whether the eyes are open
                    eye_input_l = eye_img_l.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.
                    eye_input_r = eye_img_r.copy().reshape((1, IMG_SIZE[1], IMG_SIZE[0], 1)).astype(np.float32) / 255.

                    self.pred_l = self.model.predict(eye_input_l)
                    self.pred_r = self.model.predict(eye_input_r)

                    state_l = 'O' if pred_l > 0.1 else 'X'
                    state_r = 'O' if pred_r > 0.1 else 'X'

                    if len(prev_l) < 10:
                        self.prev_l.append(state_l)
                        self.prev_r.append(state_r)
                        self.steps -= 1
                    else: 
                        for count in range(9):
                            if self.prev_l[count] != self.prev_l[count + 1]:
                                self.blink_l += 1
                            if self.prev_r[count] != self.prev_r[count + 1]:
                                self.blink_r += 1
                        if self.blink_l > 1 and self.blink_r > 1:
                            print('Eye blink is estimated!')
                            self.prev_l, self.prev_r = ['O'], ['O']
                            self.blink_l, self.blink_r = 0, 0
                            self.steps = 0
                            self.blink_count += 1
                            if self.blink_count == 5:
                                print('Eye blink is estimated five times! You are human')
                                print('Now I will recognize your face')
                                self.blink_detection = False
                                self.face_recognition = True
                        elif self.steps == 20:
                            print('Eye blink isn\'t estimated! Please blink your eyes')
                        elif self.steps == 40:
                            print('Eye blink isn\'t estimated! You are Image, I think!') 
                            self.steps = 0     
                            self.blink_count = 0

                        self.prev_l.pop(0)
                        self.prev_r.pop(0)

            elif self.face_recognition: # 얼굴인식 시작
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

                faces = self.detector(img_rgb, 1) # cv2 로 변환후 넣어주기
                checks = [] # 화면에 얼굴이 여러개일 경우, 여러 사람 중에 정답 얼굴과 일치하는 사람이 있을 경우를 위해 설정함

                for k, d in enumerate(faces): # 라즈베리파이로 확인한 camera에 보이는 사람 얼굴 수
                    shape = self.predictor(img_rgb, d)
                    face_descriptor = self.facerec.compute_face_descriptor(img_rgb, shape)

                    last_found = {'dist': 0.6, 'color': (0,0,255)}
                    dist_mean = 0

                    for _, saved_desc in self.descs.items(): # 6개의 embedded vector들에 대해 camera로 받은 image의 embedded vector와 distance를 계산
                        dist = np.linalg.norm([face_descriptor] - saved_desc, axis=1)

                        dist_mean += dist

                    if dist_mean / len(dist_mean) < last_found['dist']: # 6개의 embedded vector와 camera로 받은 image의 embedded vector의 distance의 평균이 threshold보다 작으면
                        last_found = {'dist': dist, 'color': (255,255,255)}
                        checks.append(1)                          # check에 1을 추가 -----------------------> 라즈베리파이에서 받은 얼굴이랑 6장의 정답 얼굴이랑 일치할 경우
                    else:
                        checks.append(0)                          # check에 0을 추가 ------------------> 라즈베리파이에서 받은 얼굴이랑 6장의 정답 얼굴이랑 일치하지 않을 경우

                final = sum(checks)                           # 라즈베리파이에서 3개의 얼굴을 검출했다면, checks값은 길이가 3인 one-hot vector임. 그 중 주인장이 존재하면 셋 중 하나는 1일것
                if final == 0:                                # 셋 다 0일 경우: 즉, 라즈베리파이에서 검출한 얼굴들이 전부 정답 얼굴이 아닐 경우 => check가 0, 즉 문을 열면 안됨!
                    check = 0
                else:
                    check = 1                                   # 셋 중에 0이 아닌 값이 존재할 경우, 즉 라즈베리파이에서 검출한 얼굴들 중 정답 얼굴이 존재할 경우 => check가 1, 즉, 문을 열어야 함
                return check
