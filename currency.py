def formatCurrency(currencyDigits):
    '''本函数旨在将数字化的金额（不含千分符）转化为中文的大写金额'''
    maximum_number=99999999999.99
    cn_zero="零"
    cn_one="壹"
    cn_two="贰"
    cn_three="叁"
    cn_four="肆"
    cn_five="伍"
    cn_six="陆"
    cn_seven="柒"
    cn_eight="捌"
    cn_nine="玖"
    cn_ten="拾"
    cn_hundred="佰"
    cn_thousand="仟"
    cn_ten_thousand="万"
    cn_hundred_million="亿"
    cn_symbol="人民币"
    cn_dollar="圆"
    cn_ten_cent="角"
    cn_cent="分"
    cn_integer="整"
    integral=None
    decimal=None
    outputCharacters=None
    parts=None
    digits, radices, bigRadices, decimals=None,None,None,None
    zeroCount=None
    i, p, d=None,None,None
    quotient, modulus=None ,None
    currencyDigits=str(currencyDigits)
    if currencyDigits=="":
        return ""
    if float(currencyDigits)>maximum_number:
        print("转换金额过大!")
        return ""
    parts = currencyDigits.split(".")
    if len(parts)>1:
        integral = parts[0]
        decimal = parts[1]
        decimal=decimal[0:2]
        if decimal=="0" or decimal=="00":
            decimal=""
    else:
        integral=parts[0]
        decimal=""
    digits=[cn_zero,cn_one,cn_two,cn_three,cn_four,cn_five,cn_six,cn_seven,cn_eight,cn_nine]
    radices=["",cn_ten,cn_hundred,cn_thousand]
    bigRadices=["",cn_ten_thousand,cn_hundred_million]
    decimals=[cn_ten_cent,cn_cent]
    outputCharacters = ""
    if int(integral)>0:
        zeroCount = 0
        for i in range(len(integral)):
            p = len(integral) - i - 1
            d = integral[i]
            quotient = int(p / 4)
            modulus = p % 4
            if d=="0":
                zeroCount+=1
            else:
                if zeroCount>0:
                    outputCharacters += digits[0]
                zeroCount=0
                outputCharacters = outputCharacters+ digits[int(d)] + radices[modulus]
            if modulus==0 and zeroCount < 4:
                outputCharacters =outputCharacters + bigRadices[quotient]
        outputCharacters += cn_dollar
    if decimal!="":
        jiao = decimal[0]
        if jiao=="":
            jiao="0"
        try:
            fen = decimal[1]
        except:
            fen="0"
        if fen=="":
            fen="0"
        if jiao=="0" and fen=="0":
            pass
        if jiao=="0" and fen !="0":
            outputCharacters = outputCharacters + cn_zero + digits[int(fen)] + decimals[1]
        if jiao !="0" and fen=="0":
            outputCharacters =outputCharacters + digits[int(jiao)] + decimals[0]
        if jiao!="0" and fen !="0":
            outputCharacters =outputCharacters + digits[int(jiao)] + decimals[0]
            outputCharacters =outputCharacters + digits[int(fen)] + decimals[1]
    if outputCharacters == "":
        outputCharacters = cn_zero + cn_dollar
    if decimal=="":
        outputCharacters = outputCharacters+ cn_integer
    outputCharacters = outputCharacters
    return outputCharacters