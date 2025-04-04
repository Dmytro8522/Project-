from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__, template_folder=".")
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

data_df = pd.DataFrame()

def get_product_details(article):
    return {
        'photo': f'https://dummyimage.com/150x150/000/fff&text={article}',
        'price': f'{100 + abs(hash(article)) % 50} USD'
    }

def load_data(file_path):
    global data_df
    data_df = pd.read_excel(file_path)
    details = data_df['Артикул'].apply(get_product_details)
    data_df['Фото'] = details.apply(lambda d: d['photo'])
    data_df['Ціна'] = details.apply(lambda d: d['price'])

@app.route('/', methods=['GET', 'POST'])
def index():
    global data_df
    message = ""

    if request.method == 'POST':
        file = request.files['file']
        if file:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            load_data(file_path)
            message = "Файл успешно загружен и обработан"
    else:
        data_df = pd.DataFrame()  # <-- очищаем при GET

    # далее без изменений...
    filtered_df = data_df.copy()
    filter_gender = request.args.get('gender', None)
    filter_season = request.args.get('season', None)
    if filter_gender:
        filtered_df = filtered_df[filtered_df['СТАТЬ'] == filter_gender]
    if filter_season:
        filtered_df = filtered_df[filtered_df['СЕЗОН'] == filter_season]

    genders = sorted(data_df['СТАТЬ'].dropna().unique()) if not data_df.empty else []
    seasons = sorted(data_df['СЕЗОН'].dropna().unique()) if not data_df.empty else []
    
    records = filtered_df.to_dict(orient='records') if not filtered_df.empty else []
    return render_template('index.html', records=records, message=message, 
                           genders=genders, seasons=seasons, 
                           selected_gender=filter_gender, selected_season=filter_season)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
