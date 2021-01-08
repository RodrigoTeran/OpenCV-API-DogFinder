from flask import Flask, jsonify, request
import cv2
import imutils
import os

app = Flask(__name__)


def checkHeaders(req):
    if request.headers.get('Content-Type'):
        return True
    else:
        return False


def readImages(img1Src, img2Src, img1SrcID, img2SrcID):
    img1Array = imutils.url_to_image(img1Src)
    cv2.imwrite(img1SrcID, img1Array)

    img2Array = imutils.url_to_image(img2Src)
    cv2.imwrite(img2SrcID, img2Array)

    img1 = cv2.imread(img1SrcID, cv2.IMREAD_GRAYSCALE)
    img1 = cv2.resize(img1, (500, 500), interpolation=cv2.INTER_CUBIC)

    img2 = cv2.imread(img2SrcID, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.resize(img2, (500, 500), interpolation=cv2.INTER_CUBIC)

    orb = cv2.ORB_create(nfeatures=1000)

    keyPointsImg1, descriptorsImg1 = orb.detectAndCompute(img1, None)
    keyPointsImg2, descriptorsImg2 = orb.detectAndCompute(img2, None)

    bruteForce = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bruteForce.match(descriptorsImg1, descriptorsImg2)

    # Ordenarlo para tener los mejores primero
    matches = sorted(matches, key=lambda x: x.distance)
    porcentaje = 100 - matches[20].distance

    try:
        os.remove(img1SrcID)
        os.remove(img2SrcID)
    except:
        pass

    return porcentaje


@app.route("/", methods=["POST"])
def getCV():
    try:
        if checkHeaders(request):
            porcentaje = readImages(
                request.json["img1Src"],
                request.json["img2Src"],
                request.json["img1SrcID"],
                request.json["img2SrcID"]
            )
            return jsonify({
                "status": "success",
                "porcentaje": porcentaje
            })
        else:
            return jsonify({
                "status": "error"
            })
    except:
    	return jsonify({
            "status": "error"
        })


if __name__ == "__main__":
    app.run(debug=True, port=8080)
