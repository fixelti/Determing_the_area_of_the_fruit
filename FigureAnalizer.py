import sys
import os
import cv2
from PyQt5 import QtWidgets
from PyQt5.QtGui import QIcon,QPixmap

import qt_form

class Qt_form_interface(QtWidgets.QMainWindow, qt_form.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)
        #создание кнопки
        self.pushButton.clicked.connect(self.browse_folder)


    def browse_folder(self):
        # self.listWidget.clear()  # На случай, если в списке уже есть элементы
        # directory = QtWidgets.QFileDialog.getExistingDirectory(self, "Выберите папку")
        # # открыть диалог выбора директории и установить значение переменной
        # # равной пути к выбранной директории

        # if directory:  # не продолжать выполнение, если пользователь не выбрал директорию
        #     for file_name in os.listdir(directory):  # для каждого файла в директории
        #         self.listWidget.addItem(file_name)   # добавить файл в listWidget
        fname = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '/home')[0]


        # pixmap = QPixmap(fname)

        # self.label = QtWidgets.QLabel(self)
        # self.label.setPixmap(pixmap)
        # self.label.resize(pixmap.width(), pixmap.height())

        # self.resize(pixmap.width(), pixmap.height())

        x = FigureAnalizer(fname)
        mas1,mas2,mas3 = x.get_area()
        self.listWidget.clear()
        self.listWidget_2.clear()
        self.listWidget_3.clear()
        # self.listWidget.addItem("Количество пикселей в одном мм: "+str(mas1)+" см^2")
        # self.listWidget.addItem("Плозадь фрутков по отдельности: "+str(mas2)+" см^2")
        # self.listWidget.addItem("Суммарная площадь всех фруктов: "+str(mas3)+" см^2")
        self.listWidget.addItem(f"{mas1:.{2}f} см^2")
        for i in mas2:
            self.listWidget_2.addItem(f"{i:.{2}f} см^2")
        self.listWidget_3.addItem(f"{mas3:.{2}f} см^2")


# Создание класса
class FigureAnalizer:
    '''
        Защищенная переменная.
        Хранит в себе площадь квадрата.
    '''
    __rectangle_area = 2025
    # Функция инициализации
    def __init__(self, path):
        '''
        Функция подготовки изображения
        На вход принимает путь к изображению
        '''
        self._path = path
        self.counters, self.image, self.gray = self._prepare_image(self._path)


    @classmethod
    def _prepare_image(cls, path):
        # Прочитываем изображение
        image = cv2.imread(path)
        # Переводим изображние в RGB
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Переводим изображение в серый цвет
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Получаем бинарное представление картинки
        _, binary = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)
        # Задаем контур
        counters, _ = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        cv2.imshow("image", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        return counters, image, gray


    @property
    def _find_rectangle(self):
        '''
            Функция для поиска квадрата на изображении.
            После чего получаем его площадь в пикселях.
            И возвращаем количество мм в пикселе.(Вроде)
        '''

        area = []
        for cnt in self.counters:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            # Если находим 4 угла(квадрат), то if выполняется.
            if len(approx) == 4:
                # Рисуем контур.
                cv2.drawContours(self.image, [cnt], -1, (0, 0, 255), 2)
                # Заносим в список площадь контуров.
                area.append(int(cv2.contourArea(cnt)))
        '''
            Т.к изображение пока присутствуют помехи.
            То надо отсортировать список.
            Т.к у квадрата будет самая большая площадь.
            А также мы отдаем первый элемент(самый большой).
        '''
        a = sorted(area, reverse=True)[0]
        return int(a) / self.__rectangle_area

    def get_area(self):
        '''
        Делаем похожие действия, которые были в функции _find_rectangle()
        Только для кругов. Но попадают еще и другие фигуры.
        Требуется дальнейшая оптимизация.
        :return:
        '''
        areas = []
        for cnt in self.counters:
            approx = cv2.approxPolyDP(cnt, 0.01 * cv2.arcLength(cnt, True), True)
            if len(approx) >= 5:
                cv2.drawContours(self.image, [cnt], -1, (0, 0, 255), 2)
                areas.append(int(cv2.contourArea(cnt)))

        cv2.imshow("image", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        areass = sorted(areas, reverse=True)[0:16]

        areas_mm_list = []
        for item in areass:
            item = (item / self._find_rectangle) / 100
            areas_mm_list.append(item)
        print("Количество пикселей в одном мм: ", self._find_rectangle)
        print("Плозадь фрутков по отдельности: ", areas_mm_list)
        print("Суммарная площадь всех фруктов: ", sum(areas_mm_list))
        # self.listWidget.addItem(self._find_rectangle) 
        # self.listWidget.addItem(areas_mm_list) 
        # self.listWidget.addItem(sum(areas_mm_list)) 
        return self._find_rectangle, areas_mm_list, sum(areas_mm_list)



if __name__ == '__main__':
    # x = FigureAnalizer('img.png')
    # x.get_area()
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    window = Qt_form_interface()  # Создаём объект класса ExampleApp
    window.show()  # Показываем окно
    app.exec_()
