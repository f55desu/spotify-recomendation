import PySimpleGUI as sg
import webbrowser
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity

import table
import dataset


headings = ['Рекомендованные треки', 'Ссылка', 'Сходство']

#=====================================================#
# Определение содержимого окна, т.е. макет
layout = [
        [sg.Button('Загрузить данные',size=(16,1), enable_events=True, key='-READ-', font='Helvetica 16'),
        sg.Checkbox('Содержит имена столбцов?', size=(20,1), key='colnames-check',default=True),
        sg.Checkbox('Удалить дупликаты?', size=(15,1), key='drop-duplicate',default=True)], 

        [sg.Button('Показать загруженные данные',size=(25,1),enable_events=True, key='-SHOW-', font='Helvetica 16',)],

        # Строка с названием загруженного датасета
        [sg.Text("", size=(50,1),key='-loaded-', pad=(5,5), font='Helvetica 14'),],
        #блок с листом названий книг
        [sg.Text("Выбор трека",size=(25,1), pad=(5,5), font='Helvetica 12'),],    
        [sg.Listbox(values=(''), key='songnames',size=(150,10),enable_events=True),],

        #блок с рекомендацией
        [sg.Text("", size=(1000,1),key='-recommendation-', pad=(5,5), font='Helvetica 14', enable_events=True)], 
        [sg.Table(values='', size=(500, 500), headings=headings, auto_size_columns=False, 
                  key='-RECTABLE-', col_widths=[35,55,15], 
                  max_col_width=500, 
                  enable_events=True, 
                  enable_click_events=True,
                  expand_x=True,
                  expand_y=True,
                  justification='left')]
        ]

# Создание окна
window = sg.Window('Spotify Recomendation System', layout, size=(1000,700), finalize=True)
colnames_checked = False
dropnan_checked = False
drop_duplicate = False
read_successful = False
chosenSongLink = ''
global edit
edit = False

# Цикл событий
while True:
    event, values = window.read()
    loaded_text = window['-loaded-']
    recommendation_text = window['-recommendation-']
    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    if event == '-READ-':
        if values['colnames-check']==True:
            colnames_checked=True
        if values['drop-duplicate']==True:
            drop_duplicate=True
        try:
            df, data, header_list, fn = table.read_table()
            read_successful = True
        except:
            pass
        if read_successful:
            loaded_text.update("Набор данных загружен: '{}'".format(fn))
            song_name = [i for i in df.song_name]
            window.Element('songnames').Update(values=song_name, )
    if event == '-SHOW-':
        if read_successful:
            table.show_table(data,header_list,fn)
        else:
            loaded_text.update("Набор данных не загружен")
    
    if event=='songnames':
        if len(values['songnames'])!=0:
            output_var = values['songnames'][0]
            chosenSongLink = df[df['song_name'] == output_var]['track_href'].values[0]
            chosenSongLink = chosenSongLink.replace('api.', 'open.')
            chosenSongLink = chosenSongLink.replace('v1/', '')
            chosenSongLink = chosenSongLink.replace('tracks', 'track')
            recommendation_text.update(f'Похожие треки с "{output_var}":')
            recommendation_text.Widget.bind("<Enter>", lambda _: recommendation_text.update(font=(None, 14, "underline")))
            recommendation_text.Widget.bind("<Leave>", lambda _: recommendation_text.update(font=(None, 14)))
            values = dataset.modif_dataset(df, output_var, 15, True)
            window.Element('-RECTABLE-').Update(values=values, )
    if event == '-recommendation-':
        webbrowser.open(chosenSongLink)
    if isinstance(event, tuple):
        if isinstance(event[2][0], int) and event[2][0] > -1:
            cell = row, col = event[2]
            print(row)
        table.edit_cell(window, '-RECTABLE-', row+1, col, justify='right')