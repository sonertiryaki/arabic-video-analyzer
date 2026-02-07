import cv2

def extract_frames(video):

    cap = cv2.VideoCapture(video)
    frames = []
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if count % 30 == 0:
            name = f"frame{count}.jpg"
            cv2.imwrite(name, frame)
            frames.append(name)

        count += 1

    return frames
