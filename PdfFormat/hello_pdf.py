# coding:utf-8
# pdf 格式简单分析
import re
import zlib


def show_hex_format(data, rows, columns):
    """ 展示十六进制格式 """
    for i in range(rows):
        for j in range(columns):
            print("%02x" % (data[i*columns+j]), end=" ")
        print()


def filter_up_reverse(stream_data, columns, colors=1, bitsPerComponent=8):
    """ PNG过滤器UP方法，反转方法 """
    stream_data = bytearray(stream_data)
    xref_data = []

    data_len = len(stream_data)
    width = columns*colors*bitsPerComponent//8
    rows = data_len//(width+1)

    show_hex_format(stream_data, rows, width+1)

    cursor = 1

    # 第一行处理，跳过
    while cursor <= width:
        xref_data.append(stream_data[cursor])
        cursor += 1

    for i in range(1, rows):
        filter_type = stream_data[cursor]
        cursor += 1
        assert(filter_type == 2)

        for j in range(width):
            t = (stream_data[cursor]+stream_data[cursor-width-1]) % 256
            stream_data[cursor] = t
            xref_data.append(t)
            cursor += 1

    print("xref stream data:")
    show_hex_format(xref_data, rows, width)


pdf = open("b.pdf", "rb").read()
stream_re = re.compile(b'.*?FlateDecode.*?stream(.*?)endstream', re.S)


i = 0
for s in re.findall(stream_re, pdf):
    s = s.strip(b'\r\n')
    i += 1
    try:
        # 正常解压数据
        stream_unzip_data = zlib.decompress(s)
        stream_data = stream_unzip_data.decode("utf-8")  # errors="backslashreplace"
        print(stream_data, len(stream_data))
    except zlib.error as e:
        print("zlib解压错误")
    except UnicodeDecodeError as e:
        print(stream_unzip_data)
        print("直接解析流失败")
        if i == 3:
            print("xref strem.\npng filter 反转")
            filter_up_reverse(stream_unzip_data, 7)
        if i == 2:
            print("obj stream")
            print(stream_unzip_data)
            stream_data_r = stream_unzip_data[15:]
            print(stream_data_r)
            print("obj id:2 [0-36):", stream_data_r[:37])
            print("obj id:3 [37-187):",stream_data_r[37:188])
            print("obj id:6 [188-~):",stream_data_r[188:])
    print("-------------------------") 