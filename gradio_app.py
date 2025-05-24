import gradio as gr
import requests
import tempfile

# VOICEVOX API のエンドポイント
# Flask アプリの /synthesize を指す
VOICEVOX_API_URL = "http://localhost:3000/synthesize"


def synthesize(text: str) -> str:
    """
    テキストを受け取り、ずんだもん音声で WAV ファイルを返す。
    :param text: 読み上げたい日本語テキスト
    :return: 一時的に保存した WAV ファイルのパス
    """
    payload = {"text": text, "speaker": 1}
    res = requests.post(VOICEVOX_API_URL, json=payload)
    if res.status_code != 200:
        raise RuntimeError(f"Synthesis failed: {res.text}")

    # 一時ファイルに書き出して返す
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    tmp.write(res.content)
    tmp.close()
    return tmp.name


# Gradio UI 定義
iface = gr.Interface(
    fn=synthesize,
    inputs=gr.Textbox(label="テキスト入力", lines=3, placeholder="ここに読み上げたいテキストを入力"),
    outputs=gr.Audio(label="生成音声"),
    title="Zundamon TTS",
    description="テキストを VOICEVOX のずんだもん（speaker_id=1）で音声合成します。"
)

if __name__ == "__main__":
    # ローカルホストの 7860 ポートで起動
    iface.launch(server_name="0.0.0.0", server_port=7860)
