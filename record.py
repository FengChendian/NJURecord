import extract
import datetime
from decimal import Decimal
import currency
import glob
import glob

pdf_file = glob.glob(pathname='*.pdf')

for pdf in pdf_file:
    extract.get_single_invoice_data(pdf)
# print('发票代码' + extract.invoice_code)
# print('发票号码' + extract.invoice_num)
# print(extract.items)

f = open('入库单.xml', 'r', encoding='utf-8')
content = f.readlines()

f_new = open('入库单—已填写.xml', 'w', encoding='utf-8')


def replace_xml_content(old: str, new: str):
    content[-1] = content[-1].replace(old, new)


replace_xml_content('发票代码替换', extract.invoice_code)
replace_xml_content('发票号替换', extract.invoice_num)
replace_xml_content('购置日期替换', str(
    (datetime.datetime.now() - datetime.timedelta(days=15)).strftime("%Y-%m-%d")))
replace_xml_content('入库日期替换', str(
    datetime.datetime.now().strftime("%Y-%m-%d")))
replace_xml_content('供应商替换', str(extract.supplier))

replace_dict: dict[str:str] = {
    'name': '材料',
    'model': '规格',
    'unit': '单位',
    'number': '数量',
    'univalence': '单价',
    'amount': '金额'
}
i = 0
sum = Decimal('0')
for item in extract.items:
    i = i + 1
    if i >= 5:
        print('超出最大可填写行数，请减少发票数量')
        break
    sum = sum + Decimal(str(item['amount'])) + Decimal(str(item['tax']))
    for key in item.keys():
        if key in replace_dict.keys():
            replace_xml_content(replace_dict[key] + str(i), str(item[key]))

# 将多余部分替换为空
for i in range(i + 1, 5):
    for value in replace_dict.values():
        # print(value + str(i))
        replace_xml_content(value + str(i), '')    

# print('合计数字：' + str(sum))
# print('合计中文：' + currency.formatCurrency(sum))

replace_xml_content('合计数字', str(sum))
replace_xml_content('合计中文', currency.formatCurrency(sum))

# 写入
for line in content:
    f_new.write(line)

f.close()
f_new.close()
