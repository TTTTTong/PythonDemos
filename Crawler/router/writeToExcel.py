import time
import xlwt


class write:
    def __init__(self):
        self.work = xlwt.Workbook(encoding='utf-8')
        self.sheet = self.work.add_sheet('router_user_list', cell_overwrite_ok=True)

        self.sheet.col(0).width = 256 * 20
        self.sheet.col(1).width = 256 * 20
        self.sheet.col(2).width = 256 * 20
        self.sheet.col(5).width = 256 * 30

        # 设置内容在单元格中居中
        alignment = xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        self.style = xlwt.XFStyle()
        self.style.alignment = alignment

        self.sheet.write(0, 0, '用户', self.style)
        self.sheet.write(0, 1, 'IP', self.style)
        self.sheet.write(0, 2, 'MAC', self.style)
        self.sheet.write(0, 3, '下载速度', self.style)
        self.sheet.write(0, 4, '上传速度', self.style)
        self.sheet.write(0, 5, '时间', self.style)

        # 起始行
        self.index = 1

    def writeAction(self, result):

        now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.sheet.write(self.index, 0, result[0], self.style)
        self.sheet.write(self.index, 1, result[1], self.style)
        self.sheet.write(self.index, 2, result[2], self.style)
        self.sheet.write(self.index, 3, result[3], self.style)
        self.sheet.write(self.index, 4, result[4], self.style)
        self.sheet.write(self.index, 5, now, self.style)
        self.index += 1

        self.work.save('router_user_list.xls')