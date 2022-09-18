class easyocr:
    def __init__(self, lang='ja'):
        import easyocr
        # this needs to run only once to load the model into memory
        reader = easyocr.Reader([lang], recognizer=False)
        self.reader = reader
    def getbox(self, img):
        result = self.reader.detect(img)
        return result[0][0]