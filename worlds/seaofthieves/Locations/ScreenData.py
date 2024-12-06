import typing

#from thefuzz import fuzz
# import cv2


class ScreenData:

    def __init__(self, text_group: typing.Optional[typing.List[str]] = None,
                 cascade_classifier_xml: typing.Optional[str] = None):
        self.text_group = text_group if text_group is not None else []
        for i in range(len(self.text_group)):
            self.text_group[i] = self.text_group[i].lower()

        self.cascade_classifier_xml = cascade_classifier_xml
        # self.classifier = cv2.CascadeClassifier(self.cascade_classifier_xml) if self.cascade_classifier_xml is not None else None

    def hasMatch(self, text: str = None, image=None):
        if text is not None and self.__hasTextMatch(text):
            return True
        if image is not None and self.__hasImageMatch(image):
            return True
        return False

    def __hasTextMatch(self, txt: str):
        return False
        # if txt == '':
        #     return False
        # for text_str in self.text_group:
        #     score: int = fuzz.partial_ratio(txt, text_str)
        #     if score > 90:
        #         return True
        #
        # return False

    def __hasImageMatch(self, image_scr) -> bool:
        return False
        # if self.cascade_classifier_xml is None:
        #     return False
        #
        # retvalue = False
        #
        # numpy_image = cv2.imread("temp_hand.png")
        # identified_rects = self.classifier.detectMultiScale(numpy_image, 1.01, 20)
        #
        #
        # # Iterating through rectangles of detected faces
        # for (x, y, w, h) in identified_rects:
        #     retvalue = True
        #     cv2.rectangle(numpy_image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #
        # if retvalue:
        #     bigger = cv2.resize(numpy_image, (800,800))
        #     cv2.imshow('Detected faces', bigger)
        #
        #     cv2.waitKey(0)
        #     print("Bang")
        #
        # return False
