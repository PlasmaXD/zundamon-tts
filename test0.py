import gradio as gr
import pandas as pd

def demo_fn(text, num, flag, choice, dropdown, file, img, audio, df):
    return (
        text.upper(),             # テキスト → 大文字化
        num * 2,                  # 数値 → 2倍
        not flag,                 # 真偽値 → 反転
        f"選択: {choice}",        # ラジオ
        f"ドロップダウン: {dropdown}", 
        "あり" if file else "なし",  # ファイル有無
        img,                      # 画像そのまま
        audio,                    # 音声そのまま
        f"行数: {len(df)}"         # DataFrame 行数
    )

sample_df = pd.DataFrame({"名前": ["太郎","花子"], "年齢": [28,32]})

demo = gr.Interface(
    fn=demo_fn,
    inputs=[
        gr.Textbox(label="テキスト入力", placeholder="文字列を入力", lines=2),
        gr.Slider(label="数値スライダー", minimum=0, maximum=100, step=1, value=10),
        gr.Checkbox(label="真偽フラグ", value=True),
        gr.Radio(label="ラジオ選択", choices=["A","B","C"], value="A"),
        gr.Dropdown(label="ドロップダウン", choices=["赤","緑","青"], value="緑"),
        gr.File(label="ファイルアップロード"),
        gr.Image(label="画像入力", type="pil"),
        gr.Audio(label="音声入力", type="filepath"),
        gr.Dataframe(label="データフレーム入力", value=sample_df)
    ],
    outputs=[
        "text",
        "number",
        gr.Checkbox(label="反転真偽"),
        gr.Textbox(label="ラジオ結果"),
        gr.Textbox(label="ドロップ結果"),
        gr.Textbox(label="ファイル有無"),
        gr.Image(label="画像出力"),
        gr.Audio(label="音声出力"),
        gr.Textbox(label="DataFrame 行数")
    ],
    title="All-in-One Gradio デモ",
    description="主要コンポーネントを一度に確認できるサンプルです。"
)

if __name__ == "__main__":
    demo.launch()
