import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QPixmap
import webbrowser

# UI 파일 연결
from_class = uic.loadUiType("1페이지.ui")[0]
from_class_page2 = uic.loadUiType("2페이지.ui")[0]
from_class_page3 = uic.loadUiType("3페이지.ui")[0]
from_class_page4 = uic.loadUiType("4페이지.ui")[0]
from_class_page5 = uic.loadUiType("5페이지.ui")[0]
from_class_page6 = uic.loadUiType("6페이지.ui")[0]
from_class_page7 = uic.loadUiType('기록보기.ui')[0]

global_data = {}

# 첫 번째 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 버튼에 기능을 연결하는 코드
        self.listbutton.clicked.connect(self.button1Function)

        # YouTube 링크 버튼에 기능 연결
        self.youtubeButton.clicked.connect(self.openYoutubeLink)

        # Site 링크 버튼에 기능 연결
        self.questionButton.clicked.connect(self.openSiteLink)

        # 이미지 파일 경로
        image_path = "chno4dun.png"

        # QPixmap 객체 생성 후 QLabel에 설정
        pixmap = QPixmap(image_path)
        self.photo.setPixmap(pixmap)
        self.photo.setScaledContents(True)  # 이미지 크기에 맞게 QLabel 크기 조정

    # listbutton이 눌리면 작동할 함수
    def button1Function(self):
        before_label = self.before_label.toPlainText()  # 'toPlainText()' 사용
        after_label = self.after_label.toPlainText()  # 'toPlainText()' 사용
        self.hide()  # 현재 창 숨기기
        self.page2Window = Page2Window(before_label, after_label)  # 두 번째 창 인스턴스 생성
        self.page2Window.show()  # 두 번째 창 표시

    # YouTube 링크 열기 함수
    def openYoutubeLink(self):
        webbrowser.open('https://youtu.be/2fKh70kh9tM?si=YpHOV7VxE07BP7mA')

    # Site 링크 열기 함수
    def openSiteLink(self):
        webbrowser.open('http://www.samsunghospital.com/dept/main/index.do?DP_CODE=DM&MENU_ID=008050')

# 두 번째 화면을 띄우는데 사용되는 Class 선언
class Page2Window(QMainWindow, from_class_page2):
    def __init__(self, before_label, after_label):
        super().__init__()
        self.setupUi(self)
        self.before_label = before_label
        self.after_label = after_label

        # 달력 위젯에서 날짜를 선택할 때 호출되는 함수 연결
        self.calendarWidget.clicked.connect(self.dateClicked)
        
        # 버튼에 기능을 연결하는 코드
        self.breakfast_button.clicked.connect(self.breakfastButtonFunction)
        self.lunch_button.clicked.connect(self.lunchButtonFunction)
        self.dinner_button.clicked.connect(self.dinnerButtonFunction)
        self.latenight_button.clicked.connect(self.latenightButtonFunction)
        self.record_button.clicked.connect(self.recordButtonFunction)

        self.selected_date = self.calendarWidget.selectedDate().toString('yyyy-MM-dd')

    # 날짜가 선택되면 호출되는 함수
    def dateClicked(self, date):
        self.selected_date = date.toString('yyyy-MM-dd')
        print(f'Selected date: {self.selected_date}')

    # 각 식사 버튼이 클릭되면 작동할 함수들
    def breakfastButtonFunction(self):
        self.hide()
        self.page3Window = Page3Window(self, self.selected_date, self.before_label, self.after_label)
        self.page3Window.show()

    def lunchButtonFunction(self):
        self.hide()
        self.page4Window = Page4Window(self, self.selected_date, self.before_label, self.after_label)
        self.page4Window.show()

    def dinnerButtonFunction(self):
        self.hide()
        self.page5Window = Page5Window(self, self.selected_date, self.before_label, self.after_label)
        self.page5Window.show()

    def latenightButtonFunction(self):
        self.hide()
        self.page6Window = Page6Window(self, self.selected_date, self.before_label, self.after_label)
        self.page6Window.show()

    def recordButtonFunction(self):
        self.hide()
        self.page7Window = Page7Window(self, self.selected_date)
        self.page7Window.show()

# 각 식사 페이지를 띄우는데 사용되는 Class 선언
class Page3Window(QMainWindow, from_class_page3):
    def __init__(self, parent, selected_date, before_label, after_label):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.selected_date = selected_date
        self.before_label = before_label
        self.after_label = after_label

        # 저장 버튼에 기능을 연결하는 코드
        self.savebutton.clicked.connect(self.saveButtonFunction)
        # 뒤로가기 버튼에 기능을 연결하는 코드
        self.backbutton.clicked.connect(self.backButtonFunction)

        # QLabel 위젯에 텍스트 설정
        self.text_4.setText(self.before_label)
        self.text_5.setText(self.after_label)

    def saveButtonFunction(self):
        global global_data
        if self.selected_date not in global_data:
            global_data[self.selected_date] = {}
        global_data[self.selected_date]["breakfast"] = self.collectDataToSave()
        self.hide()
        self.parent.show()

    def backButtonFunction(self):
        self.hide()
        self.parent.show()

    def collectDataToSave(self):
        data = {
            "식전 혈당": self.applyColorHighlight(self.text_1.toPlainText(), 70, 180),
            "식후 혈당": self.applyColorHighlight(self.text_2.toPlainText(), 70, 250),
            "식사 내용": self.text_3.toPlainText(),
        }
        return data

    def applyColorHighlight(self, value, low_threshold, high_threshold):
        try:
            value = float(value)
        except ValueError:
            return value  # 숫자가 아닐 경우 그대로 반환

        if value <= low_threshold:
            return f'<span style="background-color: yellow;">{value}</span>'
        elif value >= high_threshold:
            return f'<span style="background-color: red; color: white;">{value}</span>'
        return str(value)


class Page4Window(QMainWindow, from_class_page4):
    def __init__(self, parent, selected_date, before_label, after_label):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.selected_date = selected_date
        self.before_label = before_label
        self.after_label = after_label

        # 저장 버튼에 기능을 연결하는 코드
        self.savebutton.clicked.connect(self.saveButtonFunction)
        # 뒤로가기 버튼에 기능을 연결하는 코드
        self.backbutton.clicked.connect(self.backButtonFunction)

        # QLabel 위젯에 텍스트 설정
        self.text_4.setText(self.before_label)
        self.text_5.setText(self.after_label)

    def saveButtonFunction(self):
        global global_data
        if self.selected_date not in global_data:
            global_data[self.selected_date] = {}
        global_data[self.selected_date]["lunch"] = self.collectDataToSave()
        self.hide()
        self.parent.show()

    def backButtonFunction(self):
        self.hide()
        self.parent.show()

    def collectDataToSave(self):
        data = {
            "식전 혈당": self.applyColorHighlight(self.text_1.toPlainText(), 70, 180),
            "식후 혈당": self.applyColorHighlight(self.text_2.toPlainText(), 70, 250),
            "식사 내용": self.text_3.toPlainText(),
        }
        return data

    def applyColorHighlight(self, value, low_threshold, high_threshold):
        try:
            value = float(value)
        except ValueError:
            return value  # 숫자가 아닐 경우 그대로 반환

        if value <= low_threshold:
            return f'<span style="background-color: yellow;">{value}</span>'
        elif value >= high_threshold:
            return f'<span style="background-color: red; color: white;">{value}</span>'
        return str(value)


class Page5Window(QMainWindow, from_class_page5):
    def __init__(self, parent, selected_date, before_label, after_label):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.selected_date = selected_date
        self.before_label = before_label
        self.after_label = after_label

        # 저장 버튼에 기능을 연결하는 코드
        self.savebutton.clicked.connect(self.saveButtonFunction)
        # 뒤로가기 버튼에 기능을 연결하는 코드
        self.backbutton.clicked.connect(self.backButtonFunction)

        # QLabel 위젯에 텍스트 설정
        self.text_4.setText(self.before_label)
        self.text_5.setText(self.after_label)

    def saveButtonFunction(self):
        global global_data
        if self.selected_date not in global_data:
            global_data[self.selected_date] = {}
        global_data[self.selected_date]["dinner"] = self.collectDataToSave()
        self.hide()
        self.parent.show()

    def backButtonFunction(self):
        self.hide()
        self.parent.show()

    def collectDataToSave(self):
        data = {
            "식전 혈당": self.applyColorHighlight(self.text_1.toPlainText(), 70, 180),
            "식후 혈당": self.applyColorHighlight(self.text_2.toPlainText(), 70, 250),
            "식사 내용": self.text_3.toPlainText(),
        }
        return data

    def applyColorHighlight(self, value, low_threshold, high_threshold):
        try:
            value = float(value)
        except ValueError:
            return value  # 숫자가 아닐 경우 그대로 반환

        if value <= low_threshold:
            return f'<span style="background-color: yellow;">{value}</span>'
        elif value >= high_threshold:
            return f'<span style="background-color: red; color: white;">{value}</span>'
        return str(value)


class Page6Window(QMainWindow, from_class_page6):
    def __init__(self, parent, selected_date, before_label, after_label):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.selected_date = selected_date
        self.before_label = before_label
        self.after_label = after_label

        # 저장 버튼에 기능을 연결하는 코드
        self.savebutton.clicked.connect(self.saveButtonFunction)
        # 뒤로가기 버튼에 기능을 연결하는 코드
        self.backbutton.clicked.connect(self.backButtonFunction)

        # QLabel 위젯에 텍스트 설정
        self.text_4.setText(self.before_label)
        self.text_5.setText(self.after_label)

    def saveButtonFunction(self):
        global global_data
        if self.selected_date not in global_data:
            global_data[self.selected_date] = {}
        global_data[self.selected_date]["latenight"] = self.collectDataToSave()
        self.hide()
        self.parent.show()

    def backButtonFunction(self):
        self.hide()
        self.parent.show()

    def collectDataToSave(self):
        data = {
            "식전 혈당": self.applyColorHighlight(self.text_1.toPlainText(), 70, 180),
            "식후 혈당": self.applyColorHighlight(self.text_2.toPlainText(), 70, 250),
            "식사 내용": self.text_3.toPlainText(),
        }
        return data

    def applyColorHighlight(self, value, low_threshold, high_threshold):
        try:
            value = float(value)
        except ValueError:
            return value  # 숫자가 아닐 경우 그대로 반환

        if value <= low_threshold:
            return f'<span style="background-color: yellow;">{value}</span>'
        elif value >= high_threshold:
            return f'<span style="background-color: red; color: white;">{value}</span>'
        return str(value)


# 기록 보기 페이지
class Page7Window(QMainWindow, from_class_page7):
    def __init__(self, parent, selected_date):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.selected_date = selected_date

        # 선택한 날짜를 레이블에 표시
        self.date_label.setText(self.selected_date)

        # 데이터 표시 함수 호출
        self.updateRecord(global_data.get(self.selected_date, {}))

        # 뒤로가기 버튼에 기능 연결
        self.backbutton.clicked.connect(self.backButtonFunction)

        # 사진을 QLabel에 설정
        self.setPhotos()

    def setPhotos(self):
        image_path_2 = "으쌰.png"  # photo_2에 넣을 이미지 파일 경로
        image_path_3 = "식사.png"  # photo_3에 넣을 이미지 파일 경로

        pixmap_2 = QPixmap(image_path_2)
        pixmap_3 = QPixmap(image_path_3)

        self.photo_2.setPixmap(pixmap_2)
        self.photo_2.setScaledContents(True)  # 이미지 크기에 맞게 QLabel 크기 조정

        self.photo_3.setPixmap(pixmap_3)
        self.photo_3.setScaledContents(True)  # 이미지 크기에 맞게 QLabel 크기 조정

    def updateRecord(self, data):
        breakfast_data = data.get("breakfast", {})
        lunch_data = data.get("lunch", {})
        dinner_data = data.get("dinner", {})
        latenight_data = data.get("latenight", {})

        self.breakfast_text.setText(f'식전 혈당: {breakfast_data.get("식전 혈당", "")}<br>'
                                    f'식후 혈당: {breakfast_data.get("식후 혈당", "")}<br>'
                                    )

        self.lunch_text.setText(f'식전 혈당: {lunch_data.get("식전 혈당", "")}<br>'
                                f'식후 혈당: {lunch_data.get("식후 혈당", "")}<br>'
                                )

        self.dinner_text.setText(f'식전 혈당: {dinner_data.get("식전 혈당", "")}<br>'
                                 f'식후 혈당: {dinner_data.get("식후 혈당", "")}<br>'
                                 )

        self.latenight_text.setText(f'혈당: {latenight_data.get("식전 혈당", "")}<br>'
                                    )

        # 운동 내용
        self.breakfast_text2.setText(f' {breakfast_data.get("식사 내용", "")}\n'
                                    )

        self.lunch_text2.setText(f' {lunch_data.get("식사 내용", "")}\n'
                                )

        self.dinner_text2.setText(f' {dinner_data.get("식사 내용", "")}\n'
                                 )

        self.latenight_text2.setText(f' {latenight_data.get("식사 내용", "")}\n'
                                    )

    def backButtonFunction(self):
        self.hide()
        self.parent.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = WindowClass()
    myWindow.show()
    app.exec_()
