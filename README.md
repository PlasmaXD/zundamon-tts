# zundamon-tts

## 概要
テキストを受け取ってVoicevox「ずんだもん」で音声合成し、WAVファイルを返すシンプルな REST API サービスです。

## エンドポイント
- `GET /health`  
  - ヘルスチェック
- `POST /synthesize`  
  - リクエスト JSON: `{ "text": "...", "speaker": 1 }`  
  - レスポンス: WAV ファイル

## 動作確認（ローカル）
```bash
# 仮想環境作成・依存インストール
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Voicevox Engine を起動 (別ターミナルで)
docker run -d -p 50021:50021 voicevox/voicevox_engine
```
# アプリ起動
```bash
python app/main.py
```

## Docker Compose

```bash
docker compose up -d
```

* `http://localhost:3000/health` にアクセスして `{"status":"ok"}` が返れば OK
* `POST http://localhost:3000/synthesize` に JSON ボディを投げて音声合成を確認

## 環境変数

* `VOICEVOX_API_URL` (省略時 `http://localhost:50021`)
* `SPEAKER_ID` (省略時 `1`: ずんだもん)


`docker compose` の停止には主に２つのコマンドがあります。

1. **コンテナを停止（停止のみ）**

   ```bash
   docker compose stop
   ```

   * 再度 `docker compose start` すれば、そのまま起動できます。

2. **コンテナ＆ネットワークを完全に停止＆削除**

   ```bash
   docker compose down
   ```
