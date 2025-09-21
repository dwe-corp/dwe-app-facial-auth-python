import cv2

class HaarDetector:
    """Detector de faces usando Haar Cascade do OpenCV."""

    def __init__(self, cascade_path, scaleFactor=1.1, minNeighbors=5, minSize=(30,30)):
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        if self.face_cascade.empty():
            raise ValueError(f"Não foi possível carregar o arquivo Haar Cascade: {cascade_path}")
        self.scaleFactor = scaleFactor
        self.minNeighbors = minNeighbors
        self.minSize = tuple(minSize)

    def detect(self, gray_frame):
        """Detecta faces na imagem em tons de cinza."""
        faces = self.face_cascade.detectMultiScale(
            gray_frame,
            scaleFactor=self.scaleFactor,
            minNeighbors=self.minNeighbors,
            minSize=self.minSize
        )
        return faces
