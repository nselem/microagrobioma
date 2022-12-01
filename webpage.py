from distutils import filelist
import json
import os
from datetime import date

import pandas as pd
import plotly
import plotly.graph_objs as go
from io import BytesIO
from zipfile import ZipFile
from flask import Flask, render_template, request, redirect, Response, send_from_directory, send_file
from flask import url_for
from flask_material import Material
from plotly.graph_objs import Layout
from datetime import date
from libraries.processQueue import workQueue
from models.downloads import GetFilesForDownload
#from wsgiref.types import FileWrapper
#import models.downloads
#import models


app = Flask(__name__)
Material(app)

pathData = 'uploadedData'

process = workQueue()
process.start()

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if 'submit_button_network' in request.form.keys():
            if request.form['submit_button_network'] == 'byFile':
                runIdBase = date.today().strftime("%Y%m%d")
                fileOfTheDay = 1
                runId = runIdBase + '-' + str(fileOfTheDay)
                while os.path.exists(os.path.join(pathData, runId+'.biom')):
                    runId = runIdBase + '-' + str(fileOfTheDay)
                    fileOfTheDay += 1
                f = request.files['file']
                f.save( os.path.join(pathData, runId + '.biom'))
                f.close()
            if request.form['submit_button_network'] == 'byRunId':
                runId = request.form['runId']
            process.addTask(runId)
            return render_template('results.html', runId = runId)

                # send_file(os.path.join(pathData,request.form['downloadFileName']), attachment_filename="miDescarga.biom")
    #         # validate fasta file
    #         if fastaCheck != 'Valid':
    #             return render_template("home.html", errorMsg=fastaCheck)
    #         return render_template('resultsHapmod.html', table_df=df, plot0=graficas[0], plot1=graficas[1],
    #                                plot2=graficas[2], table_html=df_html)

    return render_template("home.html")



@app.route("/getResultCSV")
def getPlotCSV():
    csv = request.args.get('table_df')  #
    return Response(
        csv,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=myplot.csv"})


@app.route('/', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save(uploaded_file.filename)
    #    return render_template('results.htnml', sequence="archivo!")
    redirect(url_for('home'))



@app.route('/downloads', methods=['POST','GET'])
def downloads():
    if request.method == 'POST':
        if 'download_button_single' in request.form.keys():
            if request.form['download_button_single']=='download_button_single':
                #return send_from_directory(directory=pathData, path=request.form['downloadFileName'], as_attachment=True)
                return send_file(os.path.join(pathData,request.form['downloadFileName']), as_attachment=True)
        if 'download_button_table' in request.form.keys():
            # request.form.keys() gives dict_keys(['["20221020-1.biom","20221020-3.biom"]'])
            #listFiles = list(request.form.keys())[0].replace('[','').replace('"','').replace(']','').split(',')
            dummy = request.form['label_selected_files']
            listFiles = request.form['label_selected_files'].replace('[','').replace('"','').replace(']','').split(',')
            stream = BytesIO()
            with ZipFile(stream, 'w') as zf:
                for file in listFiles:
                    zf.write(os.path.join(pathData,file), os.path.basename(file))
            stream.seek(0)
            return send_file( stream, as_attachment=True , download_name='archive.zip',  mimetype='text/plain')


    df = GetFilesForDownload(pathData)
    df.insert(0,'','')
    df_html = df.to_html(index=False).replace('class="dataframe"', 'id=tableFileList_html class="display table nowrap responsive"')
    return render_template("downloads.html", tableFileList_html=df_html)

@app.route('/results', methods=['GET', 'POST'])
def results(sequence, plot):
    return render_template("resultsHapmod.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/modelExplanation')
def modelExplanation():
    return render_template("modelExplanation.html")

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
# http://127.0.0.1:5000/
# http://0.0.0.0:5000/