import gradio as gr
import pandas as pd

# サンプル DataFrame
sample_df = pd.DataFrame({
    "名前": ["太郎", "花子"],
    "年齢": [28, 32]
})

# イベント駆動用のコールバック関数

def greet(name):
    return f"こんにちは、{name}さん！"

def live_feedback(text):
    return f"入力中: {text}"

def echo_components(*args):
    # 入力コンポーネントの値をそのまま文字列化して返却
    return [str(arg) for arg in args]

# Blocks API でまとめたアプリ
with gr.Blocks() as demo:
    gr.Markdown("# Gradio 全機能デモ")

    # 1. 代表的なコンポーネント例
    gr.Markdown("## 代表的なコンポーネント例\n" 
                "ショートカット vs コンポーネントインスタンス を両方配置しています。")
    with gr.Row():
        # ショートカットに相当 (内部では Textbox, Slider, etc. が生成される)
        text_short = gr.Textbox(label='ショートカット: "text" 相当', lines=1)
        slider_short = gr.Slider(label='ショートカット: "slider" 相当', minimum=0, maximum=5, step=1, value=2)
        number_short = gr.Number(label='ショートカット: "number" 相当', value=7)

    with gr.Row():
        # Component インスタンスで詳細指定
        text_inst = gr.Textbox(label='インスタンス: gr.Textbox()', placeholder='詳細なラベルや行数設定が可能', lines=2)
        slider_inst = gr.Slider(label='インスタンス: gr.Slider()', minimum=10, maximum=50, step=5, value=20)
        checkbox_inst = gr.Checkbox(label='インスタンス: gr.Checkbox()', value=True)

    with gr.Row():
        radio_inst = gr.Radio(label='インスタンス: gr.Radio()', choices=["A","B","C"], value="B")
        dropdown_inst = gr.Dropdown(label='インスタンス: gr.Dropdown()', choices=["赤","緑","青"], value="緑")
        file_inst = gr.File(label='インスタンス: gr.File()')

    with gr.Row():
        image_inst = gr.Image(label='インスタンス: gr.Image()', type='pil')
        audio_inst = gr.Audio(label='インスタンス: gr.Audio()', type='filepath')
        df_inst = gr.Dataframe(label='インスタンス: gr.Dataframe()', value=sample_df)

    # 処理ボタンと出力
    output_echo = gr.Textbox(label='各コンポーネントの値を文字列化して返却')
    btn_echo = gr.Button('エコー実行')
    btn_echo.click(
        fn=echo_components,
        inputs=[
            text_short, slider_short, number_short,
            text_inst, slider_inst, checkbox_inst,
            radio_inst, dropdown_inst, file_inst,
            image_inst, audio_inst, df_inst
        ],
        outputs=output_echo
    )

    # 2. イベント駆動型の詳細 (Blocks API)
    gr.Markdown("## イベント駆動型デモ (Blocks API)")
    with gr.Row():
        name_input = gr.Textbox(label='名前入力 for greet()')
        greet_btn = gr.Button('挨拶')
        greet_output = gr.Textbox(label='挨拶結果')
    greet_btn.click(fn=greet, inputs=name_input, outputs=greet_output)

    feedback = gr.Textbox(label='ライブ入力フィードバック')
    name_input.change(fn=live_feedback, inputs=name_input, outputs=feedback)

    # タブとアコーディオンでレイアウト制御例
    with gr.Tabs():
        with gr.Tab('詳細'):
            gr.Markdown('ここは詳細タブの中身です。')
        with gr.Tab('設定'):
            with gr.Accordion('追加設定を開く', open=False):
                gr.Markdown('ここにアコーディオンで隠せる設定内容を記載します。')

# アプリ起動
if __name__ == '__main__':
    demo.launch()
