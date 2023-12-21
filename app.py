import streamlit as st
import pandas as pd
from PIL import Image
from janome.tokenizer import Tokenizer

def set_bg_color():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #C5E1A5;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

# 背景色を設定
set_bg_color()

image = Image.open('image.png')
st.image(image, use_column_width=True)

st.write('提供されたcsvファイルに含まれる単語を解析し、出現数上位の10単語を表示します。')
st.write('顧客アンケート、社内情報など、文章の解析にご活用ください。')

# Janomeの設定
janome_tokenizer = Tokenizer()

uploaded_file = st.file_uploader('CSVを選択', type='csv')
select_pos = st.sidebar.multiselect('品詞選択', ['名詞', '固有名詞', '動詞', '形容詞', '副詞', '助詞'], ['名詞'])

def janome_parse(text):
    words = []
    for token in janome_tokenizer.tokenize(text):
        pos = token.part_of_speech.split(',')[0]  # 属性へのアクセスとして扱う
        if pos in select_pos:
            words.append(token.surface)
    return words

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    tg_col = st.selectbox('対象とする列名の選択', df.columns)
    if tg_col is not None:
        df = df.dropna()  # 欠損値がある行を削除
        input_text = df[tg_col]
        input_text = ' '.join(map(str, input_text))
        if st.button('実行'):
            words = janome_parse(input_text)

            words_df = pd.DataFrame({'Word': words})
            words_df = words_df.groupby('Word', as_index=False).size()
            words_df.sort_values('size', ascending=False, inplace=True)

            st.write('読み込んだcsvファイルの内容')
            st.dataframe(df)
            
            import matplotlib.pyplot as plt
            import japanize_matplotlib
            data = words_df.head(10)
            # グラフを作成
            fig, ax = plt.subplots()
            ax.bar(data['Word'], data['size'])

            # グラフのカスタマイズ
            plt.xlabel('単語', fontsize=14)  # X軸のラベルと文字サイズを設定
            plt.ylabel('出現回数', fontsize=14)  # Y軸のラベルと文字サイズを設定
            plt.xticks(rotation=45, fontsize=12)  # X軸のラベルを回転させて表示
            plt.yticks(fontsize=12)  # Y軸のラベルの文字サイズを設定
            plt.title('出現回数の多い上位10単語', fontsize=16)  # グラフのタイトルと文字サイズを設定

            # StreamlitにMatplotlibのグラフを表示
            st.pyplot(fig)