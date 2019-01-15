import cv2
import os
import math
import logging
logging.basicConfig(level=logging.DEBUG)

Img_dir = './image'


class Point(object):
    """ 点类 """
    def __init__(self, x, y):
        self.init(x, y)

    def init(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

    def r_tuple(self, i=True):
        return (self.x, self.y)


class Rectangle(object):
    """ 矩形类 """

    def __init__(self, point_obj, w, h):
        if not isinstance(point_obj, Point):
            raise ValueError("point_obj must be Point obj")
        self._point = point_obj
        self.w = w
        self.h = h
        self.center_p = self.center()

    def center(self):
        """ 中心点 """
        temp_x = int(self._point.x + self.w/2)
        temp_y = int(self._point.y + self.h/2)
        return Point(temp_x, temp_y)

    def __repr__(self):
        return f"Rectangle( {self._point}, weight:{self.w}, height:{self.h} )"

    def scope(self, intval=False):
        """ 返回左上角和右下角坐标 """
        l = (*self._point.r_tuple(), self._point.x+self.w, self._point.y+self.h)
        if intval:
            l=[int(i) for i in l]
        return tuple(l)


class Face(object):

    def __init__(self):
        self.save_dir = './cacheUserImgResult'
        # 获取人脸识别训练数据
        # face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml')
        self.face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_alt2.xml')
        cv2.namedWindow("show", 0)

    def __del__(self):
        cv2.destroyAllWindows()

    def show(self, img, ms=0, reduce=3):
        """ 显示 """
        cv2.imshow('show', img)
        h, w = img.shape[:2]
        cv2.resizeWindow("show", w//reduce, h//reduce)
        cv2.waitKey(ms)

    def rotate_img_bad(self, img, angle):
        """ 旋转 """
        # 原图的高、宽 以及通道数
        h, w = img.shape[:2]
        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
        rotated_img = cv2.warpAffine(img, M, (w, h))
        # show(rotated_img)
        cv2.imwrite(f'./test_{angle}.png', rotated_img)
        return rotated_img

    @staticmethod
    def rotate_img(image, angle):
        # grab the dimensions of the image and then determine the
        # center
        (h, w) = image.shape[:2]
        (cX, cY) = (w // 2, h // 2)

        # grab the rotation matrix (applying the negative of the
        # angle to rotate clockwise), then grab the sine and cosine
        # (i.e., the rotation components of the matrix)
        M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)
        # print(M, type(M))
        cos = abs(M[0, 0])
        sin = abs(M[0, 1])
        # print(f"cos {cos}, sin {sin}.\t h,w:{h},{w}\tangle:{angle} \t point:{cX},{cY}")

        # compute the new bounding dimensions of the image
        nW = int((h * sin) + (w * cos))
        nH = int((h * cos) + (w * sin))

        # adjust the rotation matrix to take into account translation
        M[0, 2] += (nW / 2) - cX
        M[1, 2] += (nH / 2) - cY

        # perform the actual rotation and return the image
        rotated_img = cv2.warpAffine(image, M, (nW, nH))
        # cv2.imwrite(f'./test_{angle}.png', rotated_img)
        return rotated_img

    def check_face(self, img_gray, cascade):
        """ 检测人脸 """
        # 探测图片中的人脸
        faces = cascade.detectMultiScale(
            img_gray,
            scaleFactor=1.2,  # 每次缩减比例
            minNeighbors=5,  # 检测多次
            flags=cv2.CASCADE_SCALE_IMAGE,
            minSize=(200, 200)
        )

        logging.debug("检测到人脸区域：{}".format(faces))
        return faces

    def mark_face(self, img, faces, angle=0):
        """ 标记人脸 """
        logging.info("mark face")

        iy, ix = img.shape[:2]
        for x, y, w, h in faces:
            # 人脸区域标记
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            self.show(img, 400)

            if angle%90 == 0:
                # 90° 裁剪图片
                logging.debug("90° 裁剪图片")
                logging.debug(f"{ix}, {iy}, {x}, {y}, {w}, {h}")

                length2 = min(ix, iy)

                # 如果人脸太小，放大区域但又不超过图片长度
                length = int(w*2.5)
                length = min(length2, length)
                logging.debug(f"length: {length2} {length}")

                ow = length-w
                ow1 = ow//2
                oh = length-h
                oh1 = oh//2

                y1, y2 = y-oh1, y+h+oh1
                x1, x2 = x-ow1, x+w+ow1

                # 检测图片溢出
                logging.debug(f"{y1}, {y2}, {x1}, {x2}")
                if y1 < 0:
                    logging.debug('裁剪：1 顶部溢出')
                    y1 = 0
                    y2 = length
                if y2 > iy:
                    logging.debug('裁剪：2 底部溢出')
                    y2 = iy
                    y1 = iy-length
                if x1 < 0:
                    logging.debug('裁剪：3 左侧溢出')
                    x1 = 0
                    x2 = length
                if x2 > ix:
                    logging.debug('裁剪：4 右侧溢出')
                    x2 = ix
                    x1 = ix-length
                # 裁剪标记
                cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
            else:
                # 非90°裁剪图片
                logging.debug(f"{angle}°裁剪图片")
                # 1. 求A点坐标
                origin_h, origin_w = self.img_bgr.shape[:2]

                # 旋转角度取的ab ad边不同
                if angle%180<90:
                    logging.debug("<90")
                    ab = origin_h
                    ad = origin_w
                else:
                    logging.debug(">90")
                    ab = origin_w
                    ad = origin_h

                # 角度修正
                angle=90-angle%90

                #op = ix
                #ap = math.cos(math.radians(angle)) * ab
                #oa = op-ap
                oa = math.sin(math.radians(angle)) * ad
                A = Point(oa, 0)
                logging.debug(f"ab={ab}, ad={ad}, oa={oa}, {A}")

                # 2. 人脸中心Z坐标
                face_rect = Rectangle(Point(x, y), w, h)
                z = face_rect.center_p

                logging.debug(f"face {face_rect} center point is {z}")
                # 3. Z到AB、AD距离
                k = math.tan(math.radians(angle))  # tan(α)
                k2 = -1/k  # 垂直
                logging.info(f"k1 = {k}, k2 = {k2}")
                z_ab_len = abs(k*z.x-z.y-oa*k)/math.sqrt(k**2+1)
                z_ad_len = abs(k2*z.x-z.y-oa*k2)/math.sqrt(k2**2+1)
                logging.debug(f"z-ab len is {z_ab_len}, z-ad len is {z_ad_len}")

                # 4. 距离四边最小距离
                h1 = z_ab_len
                h2 = z_ad_len
                h3 = ad-h1
                h4 = ab-h2
                min_len = min(h1, h2, h3, h4) # radius
                logging.debug(f"face around len is {h1} {h2} {h3} {h4}, min:{int(min_len)}")

                # 4.1 圆形标注，辅助验证作用
                # cv2.line(img, (0,0), (80, 100), (0,255,0))
                for r in (h1, h2, h3, h4):
                    r = int(r)
                    if int(min_len) == r:
                        # 目标外接圆
                        cv2.circle(img, z.r_tuple(), r, (255, 0, 0), 3)
                    else:
                        # 其他圆
                        cv2.circle(img, z.r_tuple(), r, (0, 0, 255), 2)

                # 5. 圆内正方形
                square_len_half = min_len/math.sqrt(2)
                square = Rectangle(
                    Point(z.x-square_len_half, z.y-square_len_half),
                    square_len_half*2,
                    square_len_half*2
                )

                # 5.1 标注正方形
                logging.debug(f"square is {square}")
                x1, y1, x2, y2 = square.scope(True)
                # 裁剪标记
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 0), 3)

            self.show(img, 0, 2)
            logging.debug(f"final scope: {y1}, {y2}, {x1}, {x2}")
            img2 = img[y1:y2, x1:x2]

            self.show(img2)
            return img2

    def run(self, img_name):
        # 读取图片，灰度转换
        self.img_bgr = cv2.imread(os.path.join(Img_dir, img_name))
        self.img_gray = cv2.cvtColor(self.img_bgr, cv2.COLOR_BGR2GRAY)

        # 旋转图片
        find = False
        for angle in range(0, 360, 10):

            logging.debug(f"angle: {angle}")
            if angle > 0:
                img_bgr_r = self.rotate_img(self.img_bgr, angle)
                img_gray_r = self.rotate_img(self.img_gray, angle)
            else:
                img_bgr_r = self.img_bgr
                img_gray_r = self.img_gray

            self.show(img_bgr_r, 100)

            faces = self.check_face(img_gray_r, self.face_cascade)

            if not isinstance(faces, tuple):
                logging.info("find face")
                img_final = self.mark_face(img_bgr_r, faces, angle)
                find = True
                break

        if not find:
            logging.info("未找到人脸，使用原图")
            img_final = self.img_bgr

        self.show(img_final, 200)
        cv2.imwrite(os.path.join(self.save_dir, img_name), img_final)


if __name__ == '__main__':
    file_list = os.listdir(Img_dir)
    face = Face()
    for i in range(len(file_list)):
        file_name = file_list[i]
        logging.info("处理图片{0}/{1}: {2}".format(i+1, len(file_list), file_name))
        face.run(file_name)

