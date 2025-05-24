from flask import Flask, request, send_file, jsonify
import requests
import io
import os

app = Flask(__name__)

# 環境変数 VOICEVOX_API_URL を使うか、デフォルトを localhost:50021 に
VOICEVOX_API_URL = os.getenv("VOICEVOX_API_URL", "http://localhost:50021")
SPEAKER_ID = int(os.getenv("SPEAKER_ID", 1))  # 1: ずんだもん

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

@app.route("/synthesize", methods=["POST"])
def synthesize():
    """
    リクエスト JSON:
    {
      "text": "読み上げたい日本語テキスト",
      "speaker": 1  # 任意、デフォルトは ENV または 1
    }
    レスポンス: wav バイナリ
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "text を指定してください"}), 400

    text = data["text"]
    speaker = data.get("speaker", SPEAKER_ID)

    # 1. audio_query を取得
    params = {"text": text, "speaker": speaker}
    res1 = requests.post(f"{VOICEVOX_API_URL}/audio_query", params=params)
    if res1.status_code != 200:
        return jsonify({"error": "audio_query に失敗しました"}), 500
    audio_query = res1.json()

    # 2. synthesis を実行
    res2 = requests.post(
        f"{VOICEVOX_API_URL}/synthesis",
        params=params,
        json=audio_query
    )
    if res2.status_code != 200:
        return jsonify({"error": "synthesis に失敗しました"}), 500

    # 3. バイナリを返却
    buf = io.BytesIO(res2.content)
    buf.seek(0)
    return send_file(
        buf,
        mimetype="audio/wav",
        as_attachment=True,
        download_name="output.wav"
    )

if __name__ == "__main__":
    # デバッグモード on port 3000
    app.run(host="0.0.0.0", port=3000, debug=True)
