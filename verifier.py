import cv2
import numpy as np
from PIL import Image


class Verifier:
    @staticmethod
    def is_holiday(img) -> bool:
        """Returns True if the current schedule is a holiday
        Takes in PIL RGB image"""
        #img = np.array(img)
        #img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        #holiday_imgs = [cv2.imread(f"img/conge.png"), cv2.imread(f"img/conge2.png")] # (model of holiday weeks)
        #for holiday_img in holiday_imgs:
        #    diff = Verifier.__compare_images(img, holiday_img)
        #    if diff < 10:
        #        return True
        if img == "F": # We just look if the HTML is "F", meaning the week is a holiday
            return True
        return False
        
    @staticmethod
    def __compare_images(img1, img2) -> float:
        """Returns the difference between two images"""
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff**2)
        err /= float(img1.shape[0] * img1.shape[1])
        return err
