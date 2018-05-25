import textract
import chardet


def extract_text(filename):
    if filename.endswith('.txt'):
        with open(filename, 'rb') as f:
            rawdata = f.read()
            result = chardet.detect(rawdata)
            charenc = result['encoding']
            if 'UTF' not in charenc:
                return rawdata.decode('latin1')
            else:
                return rawdata.decode(charenc)
    else:
        return textract.process(filename).decode()
