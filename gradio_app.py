import gradio as gr
import requests
import tempfile

# VOICEVOX エンジン API のベース URL（デフォルトポート:50021）
VOICEVOX_API_URL = "http://localhost:50021"


def fetch_speakers():
    """/speakers から話者とスタイル一覧を取得"""
    res = requests.get(f"{VOICEVOX_API_URL}/speakers")
    res.raise_for_status()
    return res.json()

# 起動時に話者情報を読み込み
speakers_data = fetch_speakers()
# "name" はユニーク前提
speaker_map = {s["name"]: s["styles"] for s in speakers_data}


def get_style_labels(speaker_name: str):
    """話者名を受け取り "スタイル名 (ID)" ラベル一覧を返却"""
    return [f"{st['name']} ({st['id']})" for st in speaker_map[speaker_name]]


def synthesize(text: str, speaker_name: str, style_label: str) -> str:
    """VOICEVOX で音声合成し、一時 WAV ファイルのパスを返却"""
    # style_label -> ID 抽出
    style_id = int(style_label.split("(")[-1].rstrip(")"))
    print(f"style_id={style_id}, speaker_name={speaker_name}")

    # audio_query (v0.14+ は POST /audio_query?text=...&speaker=... で空 JSON)
    aq_res = requests.post(
        f"{VOICEVOX_API_URL}/audio_query",
        params={"text": text, "speaker": style_id},
        json={}
    )
    aq_res.raise_for_status()
    query = aq_res.json()

    # synthesis
    synth_res = requests.post(
        f"{VOICEVOX_API_URL}/synthesis",
        params={"speaker": style_id},
        json=query
    )
    synth_res.raise_for_status()

    # temp wav
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp.write(synth_res.content)
    tmp.close()
    return tmp.name

# === Gradio UI ===
with gr.Blocks() as iface:
    gr.Markdown("""# VOICEVOX TTS\nテキストと話者・スタイルを選択して音声を生成します。""")

    with gr.Row():
        speaker_dropdown = gr.Dropdown(
            label="話者を選択",
            choices=list(speaker_map.keys()),
            value=list(speaker_map.keys())[0]
        )
        style_dropdown = gr.Dropdown(
            label="スタイルを選択",
            choices=get_style_labels(speaker_dropdown.value),
            value=get_style_labels(speaker_dropdown.value)[0]
        )

    text_input = gr.Textbox(label="テキスト入力", lines=3, placeholder="読み上げテキストを入力")
    audio_output = gr.Audio(label="生成音声")

    # 話者変更でスタイル更新
    def update_styles(speaker):
        labels = get_style_labels(speaker)
        return gr.update(choices=labels, value=labels[0])

    speaker_dropdown.change(update_styles, inputs=speaker_dropdown, outputs=style_dropdown)

    synth_button = gr.Button("合成実行")
    synth_button.click(synthesize, inputs=[text_input, speaker_dropdown, style_dropdown], outputs=audio_output)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
