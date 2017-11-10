"""
Creon Plus 파이썬 주식차트 조회 예제 (edited by smilekhy)
http://money2.creontrade.com/e5/mboard/ptype_basic/plusPDS/DW_Basic_Read.aspx?boardseq=299&seq=68&page=1&searchString=&prd=&lang=&p=8833&v=8639&m=9505
"""

import sys
from PyQt5.QtWidgets import *
import win32com.client
import pandas as pd
import os

g_objCodeMgr = win32com.client.Dispatch('CpUtil.CpCodeMgr')
g_objCpStatus = win32com.client.Dispatch('CpUtil.CpCybos')


class CpStockChart:
    def __init__(self):
        self.objStockChart = win32com.client.Dispatch("CpSysDib.StockChart")

    # 차트 요청 - 기간 기준으로
    def RequestFromTo(self, code, fromDate, toDate, caller):
        print(code, fromDate, toDate)
        # 연결 여부 체크
        bConnect = g_objCpStatus.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            return False

        self.objStockChart.SetInputValue(0, code)  # 종목코드
        self.objStockChart.SetInputValue(1, ord('1'))  # 기간으로 받기
        self.objStockChart.SetInputValue(2, toDate)  # To 날짜
        self.objStockChart.SetInputValue(3, fromDate)  # From 날짜
        # self.objStockChart.SetInputValue(4, 500)  # 최근 500일치
        self.objStockChart.SetInputValue(5, [0, 2, 3, 4, 5, 8])  # 날짜,시가,고가,저가,종가,거래량
        self.objStockChart.SetInputValue(6, ord('D'))  # '차트 주기 - 일간 차트 요청
        self.objStockChart.SetInputValue(9, '1')  # 수정주가 사용
        self.objStockChart.BlockRequest()

        rqStatus = self.objStockChart.GetDibStatus()
        rqRet = self.objStockChart.GetDibMsg1()
        print("통신상태", rqStatus, rqRet)
        if rqStatus != 0:
            exit()

        len = self.objStockChart.GetHeaderValue(3)

        caller.dates = []
        caller.opens = []
        caller.highs = []
        caller.lows = []
        caller.closes = []
        caller.vols = []
        for i in range(len):
            caller.dates.append(self.objStockChart.GetDataValue(0, i))
            caller.opens.append(self.objStockChart.GetDataValue(1, i))
            caller.highs.append(self.objStockChart.GetDataValue(2, i))
            caller.lows.append(self.objStockChart.GetDataValue(3, i))
            caller.closes.append(self.objStockChart.GetDataValue(4, i))
            caller.vols.append(self.objStockChart.GetDataValue(5, i))

        print(len)

    # 차트 요청 - 최근일 부터 개수 기준
    def RequestDWM(self, code, dwm, count, caller):
        # 연결 여부 체크
        bConnect = g_objCpStatus.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            return False

        self.objStockChart.SetInputValue(0, code)  # 종목코드
        self.objStockChart.SetInputValue(1, ord('2'))  # 개수로 받기
        self.objStockChart.SetInputValue(4, count)  # 최근 500일치
        self.objStockChart.SetInputValue(5, [0, 2, 3, 4, 5, 8])  # 요청항목 - 날짜,시가,고가,저가,종가,거래량
        self.objStockChart.SetInputValue(6, dwm)  # '차트 주기 - 일/주/월
        self.objStockChart.SetInputValue(9, '1')  # 수정주가 사용
        self.objStockChart.BlockRequest()

        rqStatus = self.objStockChart.GetDibStatus()
        rqRet = self.objStockChart.GetDibMsg1()
        print("통신상태", rqStatus, rqRet)
        if rqStatus != 0:
            exit()

        len = self.objStockChart.GetHeaderValue(3)

        caller.dates = []
        caller.opens = []
        caller.highs = []
        caller.lows = []
        caller.closes = []
        caller.vols = []
        caller.times = []
        for i in range(len):
            caller.dates.append(self.objStockChart.GetDataValue(0, i))
            caller.opens.append(self.objStockChart.GetDataValue(1, i))
            caller.highs.append(self.objStockChart.GetDataValue(2, i))
            caller.lows.append(self.objStockChart.GetDataValue(3, i))
            caller.closes.append(self.objStockChart.GetDataValue(4, i))
            caller.vols.append(self.objStockChart.GetDataValue(5, i))

        print(len)

        return

    # 차트 요청 - 분간, 틱 차트
    def RequestMT(self, code, dwm, count, caller):
        # 연결 여부 체크
        bConnect = g_objCpStatus.IsConnect
        if (bConnect == 0):
            print("PLUS가 정상적으로 연결되지 않음. ")
            return False

        self.objStockChart.SetInputValue(0, code)  # 종목코드
        self.objStockChart.SetInputValue(1, ord('2'))  # 개수로 받기
        self.objStockChart.SetInputValue(4, count)  # 조회 개수
        self.objStockChart.SetInputValue(5, [0, 1, 2, 3, 4, 5, 8])  # 요청항목 - 날짜, 시간,시가,고가,저가,종가,거래량
        self.objStockChart.SetInputValue(6, dwm)  # '차트 주기 - 분/틱
        self.objStockChart.SetInputValue(7, 1)  # 분틱차트 주기
        self.objStockChart.SetInputValue(9, '1')  # 수정주가 사용
        self.objStockChart.BlockRequest()

        rqStatus = self.objStockChart.GetDibStatus()
        rqRet = self.objStockChart.GetDibMsg1()
        print("통신상태", rqStatus, rqRet)
        if rqStatus != 0:
            exit()

        len = self.objStockChart.GetHeaderValue(3)

        caller.dates = []
        caller.opens = []
        caller.highs = []
        caller.lows = []
        caller.closes = []
        caller.vols = []
        caller.times = []
        for i in range(len):
            caller.dates.append(self.objStockChart.GetDataValue(0, i))
            caller.times.append(self.objStockChart.GetDataValue(1, i))
            caller.opens.append(self.objStockChart.GetDataValue(2, i))
            caller.highs.append(self.objStockChart.GetDataValue(3, i))
            caller.lows.append(self.objStockChart.GetDataValue(4, i))
            caller.closes.append(self.objStockChart.GetDataValue(5, i))
            caller.vols.append(self.objStockChart.GetDataValue(6, i))

        print(len)

        return


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 기본 변수들
        self.dates = []
        self.opens = []
        self.highs = []
        self.lows = []
        self.closes = []
        self.vols = []
        self.times = []

        self.objChart = CpStockChart()

        # 윈도우 버튼 배치
        self.setWindowTitle("PLUS API TEST")
        nH = 20

        self.codeEdit = QLineEdit("", self)
        self.codeEdit.move(20, nH)
        self.codeEdit.textChanged.connect(self.codeEditChanged)
        self.codeEdit.setText('00660')
        self.label = QLabel('종목코드', self)
        self.label.move(140, nH)
        nH += 50

        btnchart1 = QPushButton("기간(일간) 요청", self)
        btnchart1.move(20, nH)
        btnchart1.clicked.connect(self.btnChart1_clicked)
        nH += 50

        btnchart2 = QPushButton("개수(일간) 요청", self)
        btnchart2.move(20, nH)
        btnchart2.clicked.connect(self.btnChart2_clicked)
        nH += 50

        btnChart3 = QPushButton("분차트 요청", self)
        btnChart3.move(20, nH)
        btnChart3.clicked.connect(self.btnChart3_clicked)
        nH += 50

        btnChart4 = QPushButton("틱차트 요청", self)
        btnChart4.move(20, nH)
        btnChart4.clicked.connect(self.btnChart4_clicked)
        nH += 50

        btnChart5 = QPushButton("주간차트 요청", self)
        btnChart5.move(20, nH)
        btnChart5.clicked.connect(self.btnChart5_clicked)
        nH += 50

        btnChart6 = QPushButton("월간차트 요청", self)
        btnChart6.move(20, nH)
        btnChart6.clicked.connect(self.btnChart6_clicked)
        nH += 50

        btnChart7 = QPushButton("엑셀로 저장", self)
        btnChart7.move(20, nH)
        btnChart7.clicked.connect(self.btnChart7_clicked)
        nH += 50

        btnExit = QPushButton("종료", self)
        btnExit.move(20, nH)
        btnExit.clicked.connect(self.btnExit_clicked)
        nH += 50

        self.setGeometry(300, 300, 300, nH)
        self.setCode('A000660')

    # 기간(일간) 으로 받기
    def btnChart1_clicked(self):
        if self.objChart.RequestFromTo(self.code, 20000101, 20171110, self) == False:
            exit()

    # 개수(일간) 으로 받기
    def btnChart2_clicked(self):
        if self.objChart.RequestDWM(self.code, ord('D'), 500, self) == False:
            exit()

    # 분차트 받기
    def btnChart3_clicked(self):
        if self.objChart.RequestMT(self.code, ord('m'), 500, self) == False:
            exit()

    # 틱차트 받기
    def btnChart4_clicked(self):
        if self.objChart.RequestMT(self.code, ord('T'), 500, self) == False:
            exit()

    # 주간차트
    def btnChart5_clicked(self):
        if self.objChart.RequestDWM(self.code, ord('W'), 100, self) == False:
            exit()

    # 월간차트
    def btnChart6_clicked(self):
        if self.objChart.RequestDWM(self.code, ord('M'), 100, self) == False:
            exit()

    def btnChart7_clicked(self):
        charfile = 'chart.xlsx'
        if (len(self.times) == 0):
            chartData = {'일자': self.dates,
                         '시가': self.opens,
                         '고가': self.highs,
                         '저가': self.lows,
                         '종가': self.closes,
                         '거래량': self.vols,
                         }
            df = pd.DataFrame(chartData, columns=['일자', '시가', '고가', '저가', '종가', '거래량'])
        else:
            chartData = {'일자': self.dates,
                         '시간': self.times,
                         '시가': self.opens,
                         '고가': self.highs,
                         '저가': self.lows,
                         '종가': self.closes,
                         '거래량': self.vols,
                         }
            df = pd.DataFrame(chartData, columns=['일자', '시간', '시가', '고가', '저가', '종가', '거래량'])

        df = df.set_index('일자')

        df.to_csv('stock_chart.csv')
        # create a Pandas Excel writer using XlsxWriter as the engine.
        #writer = pd.ExcelWriter(charfile, engine='xlsxwriter')
        # Convert the dataframe to an XlsxWriter Excel object.
        #df.to_excel(writer, sheet_name='Sheet1')
        # Close the Pandas Excel writer and output the Excel file.
        #writer.save()
        #os.startfile(charfile)
        return

    def codeEditChanged(self):
        code = self.codeEdit.text()
        self.setCode(code)

    def setCode(self, code):
        if len(code) < 6:
            return

        print(code)
        if not (code[0] == "A"):
            code = "A" + code

        name = g_objCodeMgr.CodeToName(code)
        if len(name) == 0:
            print("종목코드 확인")
            return

        self.label.setText(name)
        self.code = code

    def btnExit_clicked(self):
        exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()