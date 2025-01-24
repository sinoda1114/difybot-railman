import discord
import requests
import json
import logging

# ログの設定：デバッグレベルで、時間、ログレベル、メッセージを表示
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Discordクライアントの設定
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Dify APIの設定
DIFY_API_KEY = 'app-3g65eiwzs18ZnT0mpEz6AwDl'
DIFY_API_ENDPOINT = 'https://api.dify.ai/v1/chat-messages'

# Botが起動したときのイベントハンドラ
@client.event
async def on_ready():
    logging.info(f'{client.user} has connected to Discord!')

# メッセージを受信したときのイベントハンドラ
@client.event
async def on_message(message):
    # 自分自身のメッセージは無視
    if message.author == client.user:
        return

    # DMチャンネルの場合、またはサーバーチャンネルでメンションがなくても応答
    if isinstance(message.channel, discord.DMChannel) or not message.author.bot:
        content = message.content.strip()

        # ボットへのメンションがある場合、それを削除
        if client.user in message.mentions:
            content = content.replace(f'<@!{client.user.id}>', '').replace(f'<@{client.user.id}>', '').strip()

        # Dify APIへのリクエストヘッダーとデータの準備
        headers = {
            'Authorization': f'Bearer {DIFY_API_KEY}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'query': content,
            'user': str(message.author.id),
            'inputs': {},
            'response_mode': 'blocking'
        }
        
        # デバッグ用のログ出力
        logging.debug(f"Sending request to: {DIFY_API_ENDPOINT}")
        logging.debug(f"Headers: {json.dumps(headers, indent=2)}")
        logging.debug(f"Data: {json.dumps(data, indent=2)}")
        
        # 'typing...'表示中にAPIリクエストを送信
        async with message.channel.typing():
            try:
                # Dify APIにリクエストを送信
                response = requests.post(DIFY_API_ENDPOINT, headers=headers, json=data)
                
                # レスポンスのデバッグ情報をログに出力
                logging.debug(f"Response status code: {response.status_code}")
                logging.debug(f"Response headers: {json.dumps(dict(response.headers), indent=2)}")
                logging.debug(f"Response content: {response.text}")
                
                # エラーチェック
                response.raise_for_status()

                # レスポンスの解析と送信
                response_data = response.json()
                if 'answer' in response_data:
                    answer = response_data['answer']
                    if answer:
                        # メッセージ送信者のメンションを追加し、「さん」をつける
                        mention = f"{message.author.mention}さん、"
                        answer_with_mention = f"{mention} {answer}"
                        
                        # 2000文字以上の場合は分割して送信
                        if len(answer_with_mention) > 2000:
                            chunks = [answer_with_mention[i:i+2000] for i in range(0, len(answer_with_mention), 2000)]
                            for i, chunk in enumerate(chunks):
                                if i == 0:
                                    await message.channel.send(chunk)
                                else:
                                    await message.channel.send(chunk)
                        else:
                            await message.channel.send(answer_with_mention)
                    else:
                        await message.channel.send(f"{message.author.mention}さん APIからの応答が空でした。")
                else:
                    logging.error(f"Unexpected API response format: {response_data}")
                    await message.channel.send(f"{message.author.mention}さん APIからの応答の形式が予期せぬものでした。")

            # エラーハンドリング
            except requests.RequestException as e:
                # APIリクエストエラーの詳細なログ出力と通知
                error_message = f"APIリクエストエラー: {str(e)}\n"
                if e.response is not None:
                    error_message += f"ステータスコード: {e.response.status_code}\n"
                    error_message += f"レスポンスヘッダー: {json.dumps(dict(e.response.headers), indent=2)}\n"
                    error_message += f"レスポンス: {e.response.text}"
                else:
                    error_message += "レスポンス: No response"
                logging.error(error_message)
                await message.channel.send(f"{message.author.mention}さん {error_message}")
            except Exception as e:
                # その他の予期せぬエラーのログ出力と通知
                logging.error(f"予期せぬエラーが発生しました: {str(e)}")
                await message.channel.send(f"{message.author.mention}さん 予期せぬエラーが発生しました: {str(e)}")

# Discordクライアントの起動
client.run('MTMzMjI3NzM3NTc2NTA1NzU0Nw.GexuAm.hOEtqlKUoC3hSUTK0K6q5bV9-INozvYLBmJpao')