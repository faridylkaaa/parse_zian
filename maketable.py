import xlsxwriter
import zian

def writer(parametr):
    book = xlsxwriter.Workbook('./zian.xlsx') # создание файла эксель
    page = book.add_worksheet('Квартиры ДД') # создание таблицы в файле
    bold = book.add_format({'bold': True})
    
    page.set_column('A:A', 20)
    page.set_column('B:B', 20)
    page.set_column('C:C', 20)
    page.set_column('D:D', 20)
    page.set_column('E:E', 50)
    
    page.write('A1', 'Квартира', bold)
    page.write('B1', 'Площадь', bold)
    page.write('C1', 'Этаж', bold)
    page.write('D1', 'Цена', bold)
    page.write('E1', 'url', bold)
    

    row = 1
    column = 0
    
    for answer in parametr():
        # answer = list(answer)
        print(answer)
        page.write(row, column, answer[0])
        page.write(row, column+1, answer[1])
        page.write(row, column+2, answer[2])
        page.write(row, column+3, answer[3])
        page.write(row, column+4, answer[4])
        row += 1
        
    book.close()
    
    
writer(zian.flat)