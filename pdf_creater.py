import json
import os

from weasyprint import HTML


def __load_json_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def __format_date(date_str: str) -> str:
    months = {
        1: 'января',
        2: 'февраля',
        3: 'марта',
        4: 'апреля',
        5: 'мая',
        6: 'июня',
        7: 'июля',
        8: 'августа',
        9: 'сентября',
        10: 'октября',
        11: 'ноября',
        12: 'декабря'
    }
    
    try:
        day, month, year = map(int, date_str.split('.'))
        month_name = months[month]
        return f"{day} {month_name} {year} г."
    except (ValueError, KeyError) as e:
        raise ValueError(f"Некорректный формат даты: {date_str}") from e


STYLE_CSS = f"""
<style>
    * {{ -webkit-font-smoothing: antialiased; box-sizing: border-box; }}
    body {{
        font-family: 'Geologica', 
        sans-serif; font-size: 14px; 
        line-height: 12.2px; 
        margin: 496px 84px 308px 231px; /* Отступы для содержимого */
    }}
    @page {{
        size: 1191px 1684px;
        margin: 0;
        background-image: url("file://{os.path.abspath('background.png')}");
		background-position: center;
		background-repeat: no-repeat;
	}}
    .content {{
        padding-right: 30px;
        padding-left: 30px;
        padding-top: 32px;
        padding-bottom: 20px;
  transform: scaleY(1.3);        /* Вытягиваем по вертикали на 30% */
  transform-origin: top;      /* Точка трансформации — центр */
  display: block;   
    }}
    .receiver h1 {{
        font-size: 44px;
        color: #2d3a67;
        text-align: center;
        margin-bottom: 20px;
    }}
    .receiver h1.surname {{
        font-size: 52px;
        font-weight: bold;
        margin-bottom: 32px;
    }}

    .sender_container {{
        display: flex;
        justify-content: space-between;
        margin-top: 50px;
    }}    

    .sender h1 {{
        font-size: 38px;
        color: #2d3a67;
        text-align: left;
        margin-bottom: 20px;
    }}
    .sender h1.surname {{
        font-size: 42px;
        font-weight: bold;
        margin-bottom: 32px;
    }}

    h4 {{
        color: #2d3a67;
        text-align: center;
        font-size: 18px;
        margin-bottom: 20px;
    }}
    p {{
        font-size: 20px;
        line-height: 1.2;
        margin-bottom: 20px;
    }}
    .sender p {{
        font-size: 16px;
        color: #2d3a67;
    }}
    .congratulations_text {{
        text-align: center;
    }}
    .sender {{
        text-align: left;
    }}
    .date {{
        font-size: 20px;
        text-align: center;
        margin-top: 12px;
    }}
    .signature {{
        text-align: center;
        flex: 1; /* 🚀 Занимает ВСЁ свободное пространство */
    }}
    .signature img {{
        text-align: center;
    }}

    .surname-line {{
        display: flex;
        align-items: center;
        gap: 10px; /* небольшой отступ между фамилией и полосой (по желанию) */
        margin-bottom: 8px;
    }}

    .yellow-stripe {{
        flex: 1;
        height: 4px;
        background-color: #FFD700; 
        min-width: 30px; 
        align-self: center;
        transform: translateY(-12px); 
    }}
</style>
"""


def generate_html_report(data):
    images_paths = []
    gender = "Уважаемый" if data["recipient"]["gender"] == "male" else "Уважаемая"
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>ОТЧЕТ ДЕЯТЕЛЬНОСТИ ДЕПУТАТА ЛДПР</title>
        <link href="https://fonts.googleapis.com/css2?family=Geologica:wght@400;500;600&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&display=swap" rel="stylesheet">
        <link href="https://cdnjs.cloudflare.com/ajax/libs/meyer-reset/2.0/reset.min.css" rel="stylesheet">
        {STYLE_CSS}
    </head>
    <body>
        <div class="content">
            <h4>{gender}</h4>
            <div class="receiver">
                <h1 class="surname">{data["recipient"]["lastName"]}</h1>
                <h1>{data["recipient"]["firstName"]} {data["recipient"]["middleName"]}!</h1>
            </div>
            <div class="congratulations_text">
                <p>От души поздравляем васс профессиональным праздником!<br>
                Без вашего благородного труда невозможно представить<br>
                стабильную и сильную Россию.</p>
                <br>
                <p>Пусть каждый рабочий день приносит вам<br>
                уважение граждан нашей страны, стабильность и достаток.</p>
                <br>
                <p>Желаем вам поддержки, любви близких,<br>
                здоровья и уверенности в будущем.<br>
                С праздником! Спасибо за труд! ЛДПР — за тех,<br>
                кто работает. За сильную страну. За вас.<br></p>
            </div>
            <div class="sender_container">
                <div class="signature">
                <img src="{data['sender']['signature']}">
                    <div class="date">{__format_date(data['date'])}</div>
                </div>
                <div class="sender">
                    <div class="surname-line">
                        <h1 class="surname">{data['sender']['lastName']}</h1>
                        <div class="yellow-stripe"></div>
                    </div>
                    <h1 class="name">{data['sender']['firstName']} {data['sender']['middleName']}</h1>
                    <p>Председатель партии ЛДПР,<br>глава фракции ЛДПР в Государственной Думе<br>Федерального Собрания Российской Федерации<p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content, images_paths


def generate_pdf_report(json_data, output_filename, debug=False):
    html_content, images_paths = generate_html_report(json_data)

    try:
        HTML(string=html_content).write_pdf(output_filename)
        if debug:
            with open("debug.html", "w", encoding="utf-8") as f:
                f.write(html_content)
    finally:
        for image_path in images_paths:
            if os.path.exists(image_path):
                os.remove(image_path)

if __name__ == "__main__":
    input_file = "data_example.json"
    output_file = "example.pdf"

    json_data = __load_json_data(input_file)
    generate_pdf_report(json_data, output_file, True)


