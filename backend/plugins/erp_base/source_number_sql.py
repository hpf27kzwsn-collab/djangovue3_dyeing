"""将已登记的原色号提取算法展开为查询表达式，不安装数据库函数。"""
from functools import lru_cache
import unicodedata
from sqlglot import parse_one


@lru_cache(maxsize=1)
def character_classes():
    double=[];digits=[]
    for number in range(128,65536):
        char=chr(number)
        encoded=char.encode('gbk',errors='replace')
        if len(encoded)==2:
            double.append(number)
            if unicodedata.normalize('NFKC',char) in '0123456789':digits.append(char)
    ranges=[];start=previous=double[0]
    for number in double[1:]:
        if number!=previous+1:
            ranges.append(chr(start) if start==previous else chr(start)+'-'+chr(previous))
            start=number
        previous=number
    ranges.append(chr(start) if start==previous else chr(start)+'-'+chr(previous))
    return '['+''.join(ranges)+']','[0-9'+''.join(digits)+']'


def expression(value,width):
    double,digits=character_classes()
    # 先保留输入的前100个CP936字节，再累计数字的输出字节；截断的半个双字节字符不输出。
    # 不可编码字符在原varchar转换中为一个问号，只占一个输入字节，不属于数字。
    return parse_one(f"""CASE WHEN ({value}) IS NULL THEN NULL ELSE COALESCE((
        SELECT STRING_AGG(n.ch,'' ORDER BY n.ord) FROM (
            SELECT c.ch,c.ord,SUM(c.bytes) OVER(ORDER BY c.ord) AS output_bytes FROM (
                SELECT ch,ord,CASE WHEN ch ~ '{double}' THEN 2 ELSE 1 END AS bytes,
                    SUM(CASE WHEN ch ~ '{double}' THEN 2 ELSE 1 END) OVER(ORDER BY ord) AS input_bytes
                FROM UNNEST(STRING_TO_ARRAY(CAST(({value}) AS TEXT),NULL)) WITH ORDINALITY AS characters(ch,ord)
            ) c WHERE c.input_bytes<=100 AND c.ch ~ '{digits}'
        ) n WHERE n.output_bytes<={width}
    ),'') END""",read='postgres')
