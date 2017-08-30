from docx import Document
import os, time

source_list = []
for root, dirs, files in os.walk('E:\git\qlik\qv_master\engine\src'):
    for file in files:
        if file.endswith('.cpp'):
            source_list.append((root, file))

file_cnt = len(source_list)
#file_cnt = 20

row_per_file = 3
col_per_file = 6
row_cnt = file_cnt * row_per_file + 1

document = Document()

table = document.add_table(rows=row_cnt, cols=col_per_file)
table.style = 'Table Grid'

#write the header:

table.cell(0, 0).text = '№ пп'
table.cell(0, 1).text = 'Имя файла'
table.cell(0, 2).text = 'Дата создания'
table.cell(0, 3).text = 'Длина, байт'
table.cell(0, 4).text = 'КС (алгоритм ВКС)'
table.cell(0, 5).text = 'Выполняемая функция'


for i in range(file_cnt):
    path, name = source_list[i]

    # write path into merged cell
    path_cell = table.cell(i*row_per_file + 3, 0)
    path_cell.merge(table.cell(i*row_per_file + 3, col_per_file-1))
    path_cell.text = "Каталог %s" % (path)
    #file name cell
    name_cell = table.cell(i*row_per_file + 2, 0)
    name_cell.merge(table.cell(i*row_per_file + 2, 2))
    name_cell.text = 'итого: файлов - 1'

    #basic info row
    table.cell(i*row_per_file + 1, 0).text = "%d" % (i + 1)
    table.cell(i*row_per_file + 1, 1).text = name
    (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(os.path.join(path, name))
    table.cell(i*row_per_file + 1, 2).text = time.ctime(ctime)
    table.cell(i*row_per_file + 1, 3).text = 'length'
    table.cell(i*row_per_file + 1, 4).text = 'checksum'
    table.cell(i*row_per_file + 1, 5).text = 'description'

    if i % 10 == 0:
        print("%d / %d" % (i, file_cnt))

document.save('C:/Users/jzs/OneDrive - QlikTech Inc/FSTEK/test.docx')



