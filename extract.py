from decimal import Decimal
import fitz
from typing import List
import glob

units = ['瓶', '个', '片', '块', '包', '盒', '桶']
companies = ['深圳市嘉立创科技发展有限公司', '深圳市龙岗区维修佬电子商行']

invoice_code = ''
invoice_num = ''
supplier = ''

items: List[dict] = []


def is_float(num: str):
    try:
        float(num)
    except:
        isFloat = False
    else:
        isFloat = True
    return isFloat


def get_block_text_meta(block_text):
    float_num = []
    for i in block_text:
        i = str(i)
        if i.isdigit():
            items[-1]['number'] = i
        elif i in units:
            items[-1]['unit'] = i
        elif is_float(i):
            float_num.append(float(i))
        elif '%' in i:
            items[-1]['rate'] = i
        elif i != '' and i != items[-1]['name']:
            items[-1]['model'] = i
    tax_percent = Decimal(items[-1]['rate'][:-1]) / Decimal(100)
    if (Decimal(str(float_num[1])) * tax_percent).quantize(Decimal('0.00')) == Decimal(str(float_num[2])):
        items[-1]['univalence'] = float_num[0]
        items[-1]['amount'] = float_num[1]
        items[-1]['tax'] = float_num[2]
    else:
        float_num.sort()
        # print((Decimal(str(float_num[2])) * tax_percent).quantize(Decimal('0.00')))
        if (Decimal(str(float_num[2])) * tax_percent).quantize(Decimal('0.00')) == Decimal(str(float_num[0])):
            items[-1]['univalence'] = float_num[1]
            items[-1]['amount'] = float_num[2]
            items[-1]['tax'] = float_num[0]
        else:
            items[-1]['univalence'] = float_num[0]
            items[-1]['amount'] = float_num[2]
            items[-1]['tax'] = float_num[1]

    
    # print(float_num)


def create_item_dict(name: str) -> dict:
    return {'name': name, 'model': '', 'unit': '', 'number': '',  'univalence': '', 'amount': '', 'rate': '', 'tax': ''}

def split_multi_name_block(block_text_str:str):
    star_count = 0
    last_index = 0
    new_index = 0
    i = 0
    block_texts = []
    for char in block_text_str:
        if char == '*':
            star_count = star_count + 1
        if (star_count + 1) % 2 == 0 and star_count > 1 and (last_index != new_index or last_index == 0):
            new_index = i
            block_texts.append(block_text_str[last_index:new_index])
            last_index = new_index
        i = i + 1
    block_texts.append(block_text_str[last_index:])
    print(block_texts)
    for text in block_texts:
        text_list = text.split('\n')
        for word in text_list:
            word = str(word).strip()
            if word.count('*') == 2 and '<' not in word:
                items.append(create_item_dict(word))
                get_block_text_meta(block_text=text_list)

def get_single_invoice_data(filename):
    doc = fitz.open(filename)
    text_blocks = doc[0].get_text('blocks')

    global invoice_code, invoice_num, supplier

    for block in text_blocks:
        block_text = str(block[4]).split('\n')
        for word in block_text:
            word = str(word).strip()

            if word.isdigit():
                length = len(word)
                if length == 12 and word[0] == '0':
                    if invoice_code == '':
                        invoice_code = word
                    else:
                        if word in invoice_code:
                            continue
                        else:
                            invoice_code = invoice_code + ' ' + word
                elif length == 8:
                    if invoice_num == '':
                        invoice_num = word
                    else:
                        invoice_num = invoice_num + ' ' + word
            else:
                if word.count('*') == 2 and '<' not in word:
                    split_multi_name_block(str(block[4]))
                    # items.append(create_item_dict(word))
                    # # print(block_text)
                    # get_block_text_meta(block_text=block_text)
                    break
                elif word in companies and word not in supplier:
                    if supplier == '':
                        supplier = word
                    else:
                        supplier = supplier + ' ' + word


if __name__ == '__main__':
    pdf_file = glob.glob(pathname='*.pdf')

    for pdf in pdf_file:
        get_single_invoice_data(pdf)
    print('发票代码' + invoice_code)
    print('发票号码' + invoice_num)
    print(items)
