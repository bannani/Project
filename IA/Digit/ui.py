import sys
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter, QPen, qRed, QColor
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel
import numpy
import numpy as np
from skimage.transform import resize
from PIL import Image , ImageOps
import utils
import matplotlib
from sklearn.metrics import accuracy_score

class ImageLabel(QLabel):
    def image(self):
        qImage = self.pixmap().toImage()
        print(type(qImage))
        qImage.save('input.png')
        img=Image.open('input.png')
        #img = ImageOps.invert(img)
        img = img.convert('L')
        img = numpy.asarray(img)
        return img

    def setImage(self, img):
        qImage = QImage(img.shape[1], img.shape[0], QImage.Format_RGB888)

        for j in range(qImage.height()):
            for i in range(qImage.width()):
                gray = img[j][i]
                qImage.setPixelColor(i, j, QColor(gray, gray, gray))

        qPixmap = QPixmap(qImage)
        self.setPixmap(qPixmap)

class DigitLabel(ImageLabel):
    def __init__(self):
        super().__init__()

        self.x_old = 300
        self.y_old = 500

        self.factor = 255
        #10

        #self.size = 300
        self.qPenSize = 20

        self.resetImage()

    def resetImage(self):
        image = numpy.zeros((300, 500), dtype="int32")
        self.setImage(image)

    def mousePressEvent(self, event):
        self.x_old = event.x()
        self.y_old = event.y()

    def mouseMoveEvent(self, event):
        qPen = QPen(QColor(255, 255, 255), self.qPenSize, Qt.SolidLine)

        qPainter = QPainter()
        qPainter.begin(self.pixmap())
        qPainter.setPen(qPen)
        qPainter.drawLine(self.x_old, self.y_old, event.x(), event.y())
        qPainter.end()

        self.update()

        self.x_old = event.x()
        self.y_old = event.y()

# def scaning(m):
#     l=[0]*300
#     n=0
#     test=0
#     posin=0
#     nbr=
#     print(m)
#     for i in range(0,500):
#         print (m[i,:].shape)
#         if l!=list(m[i,:][:]) :
#             if test==0:
#                 n=n+1
#                 test=1
#                 posin=i
#         else:
#             if test==1:
#                 test=0
#                 x=resize(m[posin:i+1,:].T,(8,8),anti_aliasing=True)
#                 x = utils.format_x(x)
#                 nx,ny=x.shape
#                 matplotlib.image.imsave("chifre"+str(n)+".png", x)
#                 x2=x.reshape(1,nx*ny)
#                 y = model.predict(x2)
#     print (n)        
def build(model,y_test,x_test):
    
    def classify(event=None):
       
        nonlocal digit_label, proba_label_predict,proba_label_score
        proba_label_score.setText(str(round(accuracy_score(y_test,model.predict(x_test)),3)))
        img = digit_label.image()
        m=img.T
        l=[0]*300
        n=0
        test=0
        posin=0
        nbr=""
        
        for i in range(0,500):
            
            if l!=list(m[i,:][:]) :
                if test==0:
                    n=n+1
                    test=1
                    posin=i
            else:
                if test==1:
                    test=0
                    print ([[0]*5]*5)
                    h=np.concatenate(([[0]*50]*m[posin-1:i+1,:].shape[1],np.concatenate((m[posin-1:i+1,:].T,[[0]*50]*m[posin-1:i+1,:].shape[1]),axis=1)),axis=1)
                    x=resize(h,(8,8),anti_aliasing=True)
                    x = utils.format_x(x)
                    nx,ny=x.shape
                    matplotlib.image.imsave("test.png", h)
                    x2=x.reshape(1,nx*ny)
                    y = model.predict(x2)
                    nbr=nbr+str(y[0])
        print (nbr)
        proba_label_predict.setText(nbr)        
        # print(img.T.shape)
        # x=resize(img,(8,8),anti_aliasing=True)
        # x = utils.format_x(x)

        # nx,ny=x.shape
        # matplotlib.image.imsave('after_resize.png', x)
        # x2=x.reshape(1,nx*ny)
        # y = model.predict(x2)
        # if numpy.max(x2)==0:
        #     proba_label_predict.setText("*")
        # else:
        #     proba_label_predict.setText(str(y[0]))
    def reset():
        nonlocal digit_label

        digit_label.resetImage()

        classify()

    app = QApplication(sys.argv)

    digit_grid = QGridLayout()

    digit_label = DigitLabel()
    digit_label.mouseReleaseEvent = classify
    digit_grid.addWidget(digit_label, 0, 0, utils.NUM_PROCESS_STEPS, 1, Qt.AlignCenter)
    reset_button = QPushButton("Reset")
    reset_button.clicked.connect(reset)

    classif_grid = QGridLayout()
    class_label = QLabel("prediction : ")
    class_label1 = QLabel("Score     : ")
    class_label.setStyleSheet("background-color : orange ; padding: 2px 4px")
    class_label1.setStyleSheet("background-color : orange ; padding: 2px 4px")
    classif_grid.addWidget(class_label,0, 0, Qt.AlignCenter)
    classif_grid.addWidget(class_label1,1, 0, Qt.AlignCenter)
    proba_label_predict = QLabel()
    proba_label_score = QLabel()
    proba_label_predict.setStyleSheet("background-color : orange ; padding: 2px 4px")
    proba_label_predict.setStyleSheet("background-color : orange ; padding: 2px 4px")
    classif_grid.addWidget(proba_label_predict,0, 1, Qt.AlignCenter)
    classif_grid.addWidget(proba_label_score,1, 1, Qt.AlignCenter)

    reset()

    grid = QGridLayout()
    grid.addLayout(digit_grid, 0, 0)
    grid.addWidget(reset_button, 1, 0)
    grid.addLayout(classif_grid, 2, 0)

    w = QWidget()
    w.setWindowTitle("Digit classifier")
    w.setLayout(grid)
    w.show()

    sys.exit(app.exec_())
