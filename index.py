from flask import Flask,render_template,jsonify,redirect, url_for,send_file
import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

app = Flask(__name__)
header = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
  'Accept-Language': 'pt-BR'
}
url = "https://store.steampowered.com/search/?filter=topsellers&ignore_preferences=1?supportedlang=brazilian"
response = requests.get(url, headers=header)

soup = BeautifulSoup(response.content, 'html.parser')
div_principal = soup.select("div#search_resultsRows > a")
mais_vendidos_preco = soup.select("div#search_resultsRows > a div.discount_final_price")
precos = []
titulos = []
titulos_texto = []
for elem in div_principal:
    preco = []
    preco.append(elem.select('div.discount_final_price'))
    if preco[0]:
        titulos.append(elem.select_one("span.title"))
for preco in mais_vendidos_preco:
    precos.append(preco.text)
for item in titulos:
    titulos_texto.append(item.text)
data = {
    'titulos': titulos_texto,
    'precos': precos
}


@app.route('/')
def index():
    return render_template("index.html", precos=precos, titulos=titulos_texto)

@app.route('/excel')
def excel():
    path = 'temp/temp_arquivo.xlsx'
    df = pd.DataFrame(data)
    df.to_excel(path, index=False)
    response = send_file(path, as_attachment=True)

    @response.call_on_close
    def cleanup():
        os.remove(path)
    return response

@app.route('/app/api')
def api():
    return jsonify(data)



app.run(host="0.0.0.0", port=10000)


