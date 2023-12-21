from fastapi import FastAPI, File, UploadFile
import pandas as pd
from collections import Counter
from io import BytesIO
from janome.tokenizer import Tokenizer

app = FastAPI()

# Janomeの初期化
janome_tokenizer = Tokenizer()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile):
    # アップロードされたファイルの内容を非同期に読み込む
    contents = await file.read()
    # バイト文字列をメモリ上のファイルとして扱う
    df = pd.read_csv(BytesIO(contents))
    texts = df['comment'].tolist()

    # テキストデータの解析と単語の出現頻度計算
    word_counts = Counter()
    for text in texts:
        # Janomeを使用してテキストを単語に分割
        words = [token.surface for token in janome_tokenizer.tokenize(text)]
        for word in words:
            word_counts[word] += 1

    # 出現頻度上位10単語を取得
    top_words = word_counts.most_common(10)

    return {"top_words": top_words}