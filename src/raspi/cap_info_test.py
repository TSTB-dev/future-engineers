# ここにコードを書いてね :-)
import cv2
cap = cv2.VideoCapture(0)
print(cap.get(cv2.CAP_PROP_GAIN))
ret, frame = cap.read()
cv2.imshow("Frame", frame)
if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
