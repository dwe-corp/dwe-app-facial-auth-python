import cv2
import os
import face_recognition
import argparse
from src.utils import save_encodings, load_encodings

def enroll(name, samples_dir='samples', num_samples=5, model='hog'):
    os.makedirs(samples_dir, exist_ok=True)
    cam = cv2.VideoCapture(0)
    count = 0
    encs = []
    while count < num_samples:
        ret, frame = cam.read()
        if not ret:
            break
        rgb = frame[:, :, ::-1]
        locs = face_recognition.face_locations(rgb, model=model)
        if len(locs) == 1:
            enc = face_recognition.face_encodings(rgb, locs)[0]
            encs.append(enc)
            count += 1
            cv2.imwrite(os.path.join(samples_dir, f"{name}_{count}.jpg"), frame)
            print(f"Captured {count}/{num_samples}")
        cv2.imshow('enroll', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release(); cv2.destroyAllWindows()
    return encs

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--num', type=int, default=5)
    args = parser.parse_args()
    encs = enroll(args.name, num_samples=args.num)
    encs_old, names_old = load_encodings('src/models/encodings.pickle')
    encs_all = encs_old + encs
    names_all = names_old + [args.name]*len(encs)
    save_encodings(encs_all, names_all, 'src/models/encodings.pickle')
    print('Enrollment complete')
