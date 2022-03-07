# image를 embedded vector로 저장
import dlib, cv2
import numpy as np

class face_register():
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor('/home/hin/YOLC/ccpApi/accounts/shape_predictor_68_face_landmarks.dat')
    facerec = dlib.face_recognition_model_v1('/home/hin/YOLC/ccpApi/accounts/dlib_face_recognition_resnet_model_v1.dat')

    def find_faces(self,img): # 주어진 6개의 image에서 얼굴을 찾음
        dets = self.detector(img, 1)

        if len(dets) == 0:
            return np.empty(0), np.empty(0), np.empty(0)
        
        rects, shapes = [], []
        shapes_np = np.zeros((len(dets), 68, 2), dtype=np.int)
        for k, d in enumerate(dets):
            rect = ((d.left(), d.top()), (d.right(), d.bottom()))
            rects.append(rect)

            shape = self.predictor(img, d)
            
            for i in range(0, 68):
                shapes_np[k][i] = (shape.part(i).x, shape.part(i).y)

            shapes.append(shape)
            
        return rects, shapes, shapes_np

    def encode_faces(self, img, shapes): # face를 embedded vector로 변환
        face_descriptors = []
        for shape in shapes:
            face_descriptor = self.facerec.compute_face_descriptor(img, shape)
            face_descriptors.append(np.array(face_descriptor))

        return np.array(face_descriptors)

    def save_faces(self, username):
        img_paths = { # 6장의 이미지의 경로 ----------------------> 서버에 저장되어 있는 이미지 경로로 >>>>>>>>>>>   수정 필요   <<<<<<<<<<<<<<<
            'invader1': '/home/hin/YOLC/ccpApi/media/face/{}/image1.jpg'.format(username),
            'invader2': '/home/hin/YOLC/ccpApi/media/face/{}/image2.jpg'.format(username),
            'invader3': '/home/hin/YOLC/ccpApi/media/face/{}/image3.jpg'.format(username),
            'invader4': '/home/hin/YOLC/ccpApi/media/face/{}/image4.jpg'.format(username),
            'invader5': '/home/hin/YOLC/ccpApi/media/face/{}/image5.jpg'.format(username),
            'invader6': '/home/hin/YOLC/ccpApi/media/face/{}/image6.jpg'.format(username),
        }

        descs = { # 6개의 image를 embedded vector로 바꾼 뒤 저장할 곳
            'invader1' : None,
            'invader2' : None,
            'invader3' : None,
            'invader4' : None,
            'invader5' : None,
            'invader6' : None
        }

        for name, img_path in img_paths.items(): # 6개의 image를 돌아가면서 embedded vector로 변환
            img_bgr = cv2.imread(img_path) # 경로를 사용해 image를 읽어줌
            img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB) # image rgb변환

            _, img_shapes, _ = self.find_faces(img_rgb) # image에서 face부분을 찾아줌
            descs[name] = self.encode_faces(img_rgb, img_shapes)[0] # 찾아낸 face부분을 embedding vector로 만들어 주고, descs에 저장함

        np.save('/home/hin/YOLC/ccpApi/accounts/img/descs.npy', descs) #descs에 저장된 6개의 embedded vector를 file로 저장. 이후 face recognition에서 사용될 예정
