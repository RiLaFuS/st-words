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

st.write('## SAKURAとは')
st.write('お客様の声を簡単に解析するSAKURAは、テキストファイル（CSV 形式）をブラウザからアップロードすることで、AI 機能を用いた文章の自動解析が可能なサービスです。口コミやアンケート、問合せなどから注目すべきキーワードを探します。')
st.write('顧客ニーズの調査や自社課題の解決、サービス改善などにお役立てください。')

# Janomeの設定
janome_tokenizer = Tokenizer()

uploaded_file = st.file_uploader('↓ 今すぐ解析 ↓ （csvファイルをアップロードしてください。）', type='csv')
select_pos = st.sidebar.multiselect('↓ 解析したい品詞を選択していただけます。', ['名詞', '固有名詞', '動詞', '形容詞', '副詞', '助詞'], ['名詞'])

def janome_parse(text):
    words = []
    for token in janome_tokenizer.tokenize(text):
        pos = token.part_of_speech.split(',')[0]  # 属性へのアクセスとして扱う
        if pos in select_pos:
            words.append(token.surface)
    return words

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    tg_col = st.selectbox('csvファイルが読み込めました。次に解析したい列名を選択し、「実行」をクリックしてください。 ', df.columns)
    if tg_col is not None:
        df = df.dropna()  # 欠損値がある行を削除
        input_text = df[tg_col]
        input_text = ' '.join(map(str, input_text))
        if st.button('実行'):
            words = janome_parse(input_text)

            words_df = pd.DataFrame({'Word': words})
            words_df = words_df.groupby('Word', as_index=False).size()
            words_df.sort_values('size', ascending=False, inplace=True)

            st.write('アップロードされたcsvファイルの内容は以下です。')
            st.dataframe(df)
            
            import matplotlib.pyplot as plt
            import japanize_matplotlib
            data = words_df.head(20)
            # グラフを作成
            fig, ax = plt.subplots()
            ax.bar(data['Word'], data['size'])

            # グラフのカスタマイズ
            plt.xlabel('単語', fontsize=14)  # X軸のラベルと文字サイズを設定
            plt.ylabel('出現回数', fontsize=14)  # Y軸のラベルと文字サイズを設定
            plt.xticks(rotation=45, fontsize=12)  # X軸のラベルを回転させて表示
            plt.yticks(fontsize=12)  # Y軸のラベルの文字サイズを設定
            plt.title('出現頻度が高い20個の「キーワード」', fontsize=16)  # グラフのタイトルと文字サイズを設定

            # StreamlitにMatplotlibのグラフを表示
            st.pyplot(fig)
            st.write('↓ 出現頻度が高い「キーワード」と出現回数の表')
            st.dataframe(data)

            st.write('解析が全て終了しました。またのご利用を心よりお待ちしております。')
