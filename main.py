import urllib.request
import cv2
import numpy as np
url = 'http://192.168.4.3/cam-lo.jpg'

qcd = cv2.QRCodeDetector()

def interpolatePosition():
    return 0

while True:
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    frame = cv2.imdecode(imgNp, -1)
    frame = cv2.resize(frame, (640,480))

    retval, decoded_info, points, straight_qrcode = qcd.detectAndDecodeMulti(frame)

    print(retval)
    print(decoded_info)

    #frameRotated = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    cv2.imshow('frameRotated', frame)

    if ord('q')==cv2.waitKey(10):
        exit(0)
frame.release()
cv2.destroyAllWindows()