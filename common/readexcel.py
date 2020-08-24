import openpyxl


class ReadExcel(object):

    def __init__(self, filename, sheet_name):
        self.filename = filename
        self.sheet_name = sheet_name

    def open(self):
        # 获取工作簿对象
        self.wb = openpyxl.load_workbook(self.filename)
        # 选择表单
        self.sh = self.wb[self.sheet_name]

    def read_data(self):
        """读取数据"""
        self.open()
        # 按行获取表单所有格子中的数据，每一行的数据放在一个元组中
        datas = list(self.sh.rows)
        # 获取第一行的数据，作为字典的键
        title = [i.value for i in datas[0]]
        # 创建一个空列表，用例存放用例数据
        cases = []
        # 遍历除第一行之外的数据
        for i in datas[1:]:
            # 获取该行数据的值
            values = [c.value for c in i]
            # 将该行数据和title（第一行数据）打包转换为字典
            case = dict(zip(title, values))
            # 将转换的字典添加到前面创建的空列表cases中
            cases.append(case)
        return cases

    def write_data(self, row, column, value):
        """写入数据"""
        self.open()
        # 写入数据
        self.sh.cell(row=row, column=column, value=value)
        # 保存文件
        self.wb.save(self.filename)
