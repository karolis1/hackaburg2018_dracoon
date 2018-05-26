import textract
import chardet
import re
from nltk.corpus import stopwords

STOP_WORDS = set(stopwords.words('german'))


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


def preprocess_text(text):
    text = text.lower()
    text = re.sub('\d', '', text)
    text = re.sub('[^\w]', ' ', text)
    tokens = text.split()
    tokens = [token for token in tokens if token not in STOP_WORDS]
    return ' '.join(tokens)
