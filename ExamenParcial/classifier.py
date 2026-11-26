import cv2
import threading
import time
import numpy as np
from logger_parcial import Logger


class Classifier:
    def __init__(self, src=0, name="Classifier_1"):
        try:
            self.name = name
            self.src = src
            self.ret = None
            self.frame = None
            self.frame_classify = None
            self.frame_empacar = None
            self.frame_perforar = None
            self.frame_refabricar = None
            self.contours = None
            self.stopped = False
            self.loggerReport = Logger(name)
            self.loggerReport.logger.info("Init constructor RunCamera")
            self.pieza_en_frame = False
            self.numero_piezas = 0
            self.piezas_empaque = 0
            self.piezas_perforado = 0
            self.piezas_fabricacion = 0
            self.lock = threading.Lock()
        except Exception as e:
            self.loggerReport.logger.error("Error in RunCamera: " + str(e))
        except Exception as e:
            self.loggerReport.logger.error("Error in RunCamera: " + str(e))

    def start(self):
        try:
            self.stream = cv2.VideoCapture(self.src)
            self.fps = self.stream.get(cv2.CAP_PROP_FPS)
            if self.fps <= 0:  # Handle cases where FPS might not be available or valid
                self.fps = 30  # Default to a common FPS if not found
                self.loggerReport.logger.warning(
                    f"Could not determine FPS for {self.src}. Defaulting to {self.fps}."
                )
            else:
                self.loggerReport.logger.info(f"Video FPS: {self.fps}")
            time.sleep(1)
            self.ret, self.frame = self.stream.read()
            if self.stream.isOpened():
                self.loggerReport.logger.info("Creating Camera thread")
                self.cam_thread = threading.Thread(
                    target=self.get, name=self.name, daemon=True
                )
                self.cam_thread.start()
            else:
                self.loggerReport.logger.warning("Camera not initialized")

        except Exception as e:
            self.loggerReport.logger.error("Error starting camera thread: " + str(e))

    def stop(self):
        self.loggerReport.logger.info("Stopping camera thread and releasing resources")
        self.stopped = True
        if hasattr(self, "cam_thread") and self.cam_thread.is_alive():
            self.cam_thread.join(timeout=2)  # Wait for the thread to finish
        if hasattr(self, "stream") and self.stream.isOpened():
            self.stream.release()

    def get(self):
        delay_between_frames = 1.0 / self.fps
        self.loggerReport.logger.info(
            "Starting thread, time between frames is %f" % (delay_between_frames)
        )
        while not self.stopped:
            start_time = time.time()
            ret, frame = self.stream.read()
            if not ret:
                break

            # Use the lock to safely update the shared frame.
            with self.lock:
                self.ret = ret
                self.frame = frame

            processing_time = time.time() - start_time
            sleep_time = delay_between_frames - processing_time
            if sleep_time > 0:
                time.sleep(sleep_time * 2)

    def processFrame(self):
        frame_copy = None
        with self.lock:
            if not self.ret or self.frame is None:
                return None
            frame_copy = self.frame.copy()

        self.contours = frame_contours(frame_copy)
        valid_contours = self.filterContours()
        if self.pieza_en_frame and not self.pieza_procesada:
            self.classify(valid_contours, frame_copy)
            self.pieza_procesada = True
        return frame_copy, valid_contours

    def getContours(self):
        self.contours = frame_contours(self.frame)

    def filterContours(self) -> list:
        if len(self.contours) == 0:
            self.pieza_en_frame = False
            return []
        valid_contours = [cnt for cnt in self.contours if cv2.contourArea(cnt) > 10000]
        if len(valid_contours) == 0:
            self.pieza_en_frame = False
            return valid_contours
        contour_limits = []
        for cnt in valid_contours:
            x, y, w, h = cv2.boundingRect(cnt)
            contour_limits.append(x)
        if (self.pieza_en_frame) or min(contour_limits) < 500:
            return valid_contours
        self.numero_piezas += 1
        self.pieza_en_frame = True
        self.pieza_procesada = False
        self.loggerReport.logger.info("Pieza en frame")
        return valid_contours

    def classify(self, contours, frame):
        if len(contours) != 1:
            self.piezas_empaque += 1
            self.loggerReport.logger.info("Pieza a empacar")
            self.frame_empacar = frame
        else:
            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # red (160, 20)
            # yellow (20,40)
            # green (40, 90)
            # blue (90, 120)
            # purple (120, 160)

            red = [0, 20, "red"]
            yellow = [20, 40, "yellow"]
            green = [40, 90, "green"]
            blue = [90, 120, "blue"]
            purple = [120, 160, "purple"]
            color_th = [red, yellow, green, blue, purple]
            num_color = 0
            for i in color_th:
                frame_bin_hsv = binaryHSV(frame_hsv, i[0], i[1], 0, 200, 40, 120)
                if np.count_nonzero(frame_bin_hsv) > 50000:
                    num_color += 1
            if num_color > 1:
                self.piezas_fabricacion += 1
                self.loggerReport.logger.info("Pieza a refabricar")
                self.frame_refabricar = frame
            else:
                self.loggerReport.logger.info("Pieza a perforar")
                self.piezas_perforado += 1
                self.frame_perforar = frame

        # frame_hsv_th = frame_hsv.copy()
        # frame_hsv_th[frame_bin_hsv == 255] = [110, 200, 255]
        # frame_th_bgr = cv2.cvtColor(frame_hsv_th, cv2.COLOR_HSV2BGR)
        for cnt in self.filterContours():
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)
        self.frame_classify = frame


def binary(image, method=0, Umin=0, Umax=255):
    if method == 0:
        ret, imgBinary = cv2.threshold(image, Umin, 255, cv2.THRESH_BINARY)
    else:
        imgBinary = cv2.inRange(image, Umin, Umax)
    return imgBinary


def binaryHSV(image, minH=0, maxH=255, minS=0, maxS=255, minV=0, maxV=255):
    imgBinary = cv2.inRange(image, (minH, minS, minV), (maxH, maxS, maxV))
    return imgBinary


def frame_contours(frame):
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_bin = binary(frame_gray, method=0, Umin=5)
    frame_filtered = filter_frame(frame_bin)

    contours, _ = cv2.findContours(frame_bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    return contours


def filter_frame(frame_bin):
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (50, 50))
    mask_open = cv2.morphologyEx(frame_bin, cv2.MORPH_OPEN, kernel)
    return mask_open


def main():
    video_source = "./video_2.mp4"
    classifier = Classifier(src=video_source)
    classifier.start()

    cv2.namedWindow("Video Classifier", cv2.WINDOW_NORMAL)

    try:
        while True:
            frame, _ = classifier.processFrame()

            if frame is None:
                time.sleep(0.01)
                continue

            # Display the frame with annotations.

            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            frame_bin = binary(frame_gray, method=0, Umin=5)
            frame_filtered = filter_frame(frame_bin)
            frame_filtered_color = cv2.cvtColor(frame_filtered, cv2.COLOR_GRAY2BGR)

            for cnt in classifier.filterContours():
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 5)

            if classifier.frame_classify is not None:
                cv2.imshow("Video Classifier", classifier.frame_classify)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        classifier.stop()
        cv2.destroyAllWindows()
        print(classifier.numero_piezas)
        print(classifier.piezas_empaque)
        print(classifier.piezas_perforado)
        print(classifier.piezas_fabricacion)


if __name__ == "__main__":
    main()
