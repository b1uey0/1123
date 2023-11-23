# app.py (Flask 어플리케이션)
from flask import Flask, render_template
import pandas as pd
import matplotlib.pyplot as plt
import io
import base64
from matplotlib import font_manager, rc

# 폰트 경로 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 한글 폰트 파일 경로 (Windows 기준)
font_name = font_manager.FontProperties(fname=font_path).get_name()
rc('font', family=font_name)


app = Flask(__name__)

# CSV 데이터를 DataFrame으로 로드
data = pd.read_csv('cox-violent-parsed_filt_usable.csv')

@app.route('/')
def index():
    # 성별에 따른 폭력적 재범 발생 비율 그래프
    sex_violent_recid = data.groupby('sex')['is_violent_recid'].mean()
    sex_violent_recid_plot = sex_violent_recid.plot(kind='bar', title='폭력적 재범 발생 비율 (성별)', xlabel='성별', ylabel='폭력적 재범 발생 비율')
    plt.tight_layout()
    sex_violent_recid_img = get_image(sex_violent_recid_plot)

    # 나이에 따른 재범 발생 비율 그래프
    age_recid = data.groupby('age_cat')['event'].mean()
    age_recid_plot = age_recid.plot(kind='bar', title='재범 발생 비율 (나이)', xlabel='나이 카테고리', ylabel='재범 발생 비율')
    plt.tight_layout()
    age_recid_img = get_image(age_recid_plot)

    # 인종에 따른 일반적 재범 발생 비율 그래프
    race_recid = data.groupby('race')['is_recid'].mean()
    race_recid_plot = race_recid.plot(kind='bar', title='일반적 재범 발생 비율 (인종)', xlabel='인종', ylabel='일반적 재범 발생 비율')
    plt.tight_layout()
    race_recid_img = get_image(race_recid_plot)

    # Render the HTML template with images
    return render_template('index.html', sex_violent_recid_img=sex_violent_recid_img,
                           age_recid_img=age_recid_img, race_recid_img=race_recid_img)

def get_image(plot):
    # 그래프를 이미지로 변환하여 HTML에 삽입
    img = io.BytesIO()
    plot.get_figure().savefig(img, format='png')
    img.seek(0)
    plot_img = base64.b64encode(img.getvalue()).decode()
    return f'data:image/png;base64,{plot_img}'

if __name__ == '__main__':
    app.run(debug=True)
