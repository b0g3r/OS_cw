from openpyxl import Workbook

from xlsxwriter import Workbook

def create_report(data):
    wb = Workbook('report.xlsx')
    ws = wb.add_worksheet()
    ws.write(0, 0, 'x')
    ws.write(0, 1, 'y')
    for x, y, r in zip(data['x'], data['y'], range(1, data['i']+1)):
        ws.write(r, 0, x)
        ws.write(r, 1, y)
    ws.write(data['i']+1, 0, data['poly'])

    ws.insert_image(0, 4, 'plot_image', {'image_data': data['plot_image']})

    ws.insert_image(0, 11, 'error_image', {'image_data': data['error_image']})
    wb.close()
