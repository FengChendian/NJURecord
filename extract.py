import fitz
units = ['瓶', '个', '片', '块', '包', '盒', '桶']
companies = ['深圳市嘉立创科技发展有限公司', '深圳市龙岗区维修佬电子商行']

invoice_code = ''
invoice_num = ''
supplier = ''

items: list[dict] = []


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
    float_num.sort()
    items[-1]['univalence'] = float_num[-2]
    items[-1]['amount'] = float_num[-1]
    items[-1]['tax'] = float_num[0]

    # print(float_num)


def create_item_dict(name: str) -> dict:
    return {'name': name, 'model': '', 'unit': '', 'number': '',  'univalence': '', 'amount': '', 'rate' : '', 'tax': ''}


def get_single_invoice_data(filename):
    doc = fitz.open(filename)
    text_blocks = doc[0].get_text('blocks')
    # print(text_blocks)

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
                    items.append(create_item_dict(word))
                    # print(block_text)
                    get_block_text_meta(block_text=block_text)
                elif word in companies and word not in supplier:
                    if supplier == '':
                        supplier = word
                    else:
                        supplier = supplier + ' ' + word


if __name__ == '__main__':
    for i in range(1, 4):
        get_single_invoice_data(str(i) + '.pdf')
    print('发票代码' + invoice_code)
    print('发票号码' + invoice_num)
    print(items)
