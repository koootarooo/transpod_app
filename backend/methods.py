import tempfile
from flask import Flask
from flask_mail import Mail
from dotenv import load_dotenv
import os
from faster_whisper import WhisperModel
from flask_mail import Message
import openai
import pysbd
from gtts import gTTS
import boto3

# 環境変数のロード
load_dotenv()

# メール設定
mail = Mail()

# openai設定
class GPT3:
    def __init__(self):
        openai.api_key = os.environ.get('OPENAI_API_KEY')

    def generate_text(self, prompt):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']

gpt3 = GPT3()

def transcription(file):
    openai.api_key = os.environ.get('OPENAI_API_KEY')
    audio_file= open(file.name,"rb")
    response = openai.Audio.transcribe("whisper-1", audio_file)
    transcript = response["text"]
    print(transcript)
    return transcript

def sentence_segmentation(text):
    print(text)
    seg_en = pysbd.Segmenter(language="en", clean=False)
    sentenced_text = seg_en.segment(text)
    print(sentenced_text)
    return sentenced_text

def translate_loop(sentenced_text, transcript, MAX_COUNT):
    textsum = ""
    translated_texts = ""
    if len(transcript) >= MAX_COUNT:
        for line in sentenced_text[:-1]:
            if len(textsum) < MAX_COUNT:
                textsum += line
            else:
                print("translate")
                print(textsum)
                prompt = "以下の文章を日本語に翻訳してください。" + textsum
                result = gpt3.generate_text(prompt)
                print(result)
                translated_texts +=  result
                textsum = ""
        print("last")
        textsum += sentenced_text[-1]
        prompt = "以下の文章を日本語に翻訳してください。" + textsum
        translated_texts +=  gpt3.generate_text(prompt)
    else:
        for line in sentenced_text:
            textsum += line
        prompt = "以下の文章を日本語に翻訳してください。" + textsum
        translated_texts +=  gpt3.generate_text(prompt)
    return translated_texts

def text_to_speech(translated_text):
    message = translated_text
    print(message)
    fp = tempfile.NamedTemporaryFile(suffix=".mp3")
    gTTS(message, lang='ja').write_to_fp(fp)
    return fp

def translate(file):  
    MAX_COUNT = 3000
    transcript = transcription(file)
    sentenced_text = sentence_segmentation(transcript)
    translated_text = translate_loop(sentenced_text, transcript, MAX_COUNT)
    speech_file = text_to_speech(translated_text)
    return speech_file

def save_s3(file,file_name):
    s3 = boto3.resource('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'), aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
    bucket = s3.Bucket('transpod')
    Filepath = file.name
    Key = f'translated/{file_name}'
    bucket.upload_file(Filepath, Key)


def download():
    s3 = boto3.resource('s3', aws_access_key_id=os.environ.get('AWS_ACCESS_KEY'), aws_secret_access_key=os.environ.get('AWS_SECRET_KEY'))
    response = s3.meta.client.get_object(Bucket="transpod", Key="musk_news.mp3")
    data= response['Body'].read()
    print('data')
    # downloaded_file = bucket.download_file('test/test.mp3', 'test.mp3')
    # print("download")
    # print(downloaded_file)
    return 'done'
    
def send_mail():        
    msg = Message('Test Mail', recipients=['iikotaro3@yahoo.co.jp'])
    msg.body = "SECRET KEY was loaded successfully"
    mail.send(msg)
    return 'sent'


# def gpt():
#     gpt3 = GPT3()
#     textsum = "I'm honored to be with you today for your commencement from one of the finest universities in the world."
#     prompt = "以下の文章を日本語に翻訳してください。" + textsum
#     result = gpt3.generate_text(prompt)
#     return result
