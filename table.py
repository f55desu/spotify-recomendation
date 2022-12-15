import PySimpleGUI as sg
import pandas as pd
import spotify

def read_table():
    sg.set_options(auto_size_buttons=True)
    layout = [[sg.Text('Датасет (формат CSV)', size=(17, 1)),sg.InputText(),
               sg.FileBrowse(file_types=(("CSV Files", "*.csv"),("Text Files", "*.txt")))],
               [sg.Submit(), sg.Cancel()]]

    window1 = sg.Window('Добавить файл', layout)
    try:
        event, values = window1.read()
        window1.close()
    except:
        window1.close()
        return
    
    filename = values[0]
    
    if filename == '':
        return

    data = []
    header_list = []

    if filename is not None:
        fn = filename.split('/')[-1]
        try:                     
            if spotify.colnames_checked:
                df = pd.read_csv(filename, sep=',', engine='python')
                # Использует первую строку (которая должна быть именами столбцов) в качестве имен столбцов
                header_list = list(df.columns)
                # Удаляет первую строку в таблице (иначе имена заголовков и первая строка будут одинаковыми)
                data = df[1:].values.tolist()
            else:
                df = pd.read_csv(filename, sep=',', engine='python', header=None)
                # Создает имена столбцов для каждого столбца («column0», «column1» и т. д.)
                header_list = ['column' + str(x) for x in range(len(df.iloc[0]))]
                df.columns = header_list
                # Читать все остальное в список строк
                data = df.values.tolist()

            # Удаление дупликатов
            if spotify.drop_duplicate:
                df = df.drop_duplicates(subset=['song_name'])
                data = df.values.tolist()

            window1.close()
            return (df,data, header_list,fn)
        except Exception as e:
            print(e)
            sg.popup_error('Ошибка чтения файла')
            window1.close()
            return

#Показать загруженный датасет
def show_table(data, header_list, fn):    
    layout = [
        [sg.Table(values=data,
                  headings=header_list,
                  font='Helvetica',
                  pad=(25,25),
                  display_row_numbers=False,
                  auto_size_columns=True,
                  num_rows=min(25, len(data)))]
    ]

    window = sg.Window(fn, layout, grab_anywhere=False)
    event, values = window.read()
    window.close()

# Функция TKinter для отображения и редактирования ячейки таблицы
def edit_cell(window, key, row, col, justify='left'):

    global textvariable, edit
    def callback(event, row, col, text, key):
        global edit
        # event.widget gives you the same entry widget we created earlier
        widget = event.widget
        if key == 'Focus_Out':
            text = widget.get()
            print(text)
        widget.destroy()
        widget.master.destroy()
        # Get the row from the table that was edited
        values = list(table.item(row, 'values'))
        # Store new value in the appropriate row and column
        values[col] = text
        table.item(row, values=values)
        edit = False

    if spotify.edit or row <= 0:
        return

    edit = True
    # Get the Tkinter functionality for our window
    root = window.TKroot
    table = window[key].Widget
    text = table.item(row, "values")[col]

    # Return x and y position of cell as well as width and height (in TreeView widget)
    x, y, width, height = table.bbox(row, col)

    # Create a new container that acts as container for the editable text input widget
    frame = sg.tk.Frame(root)
    # put frame in same location as selected cell
    frame.place(x=x+4, y=y+377, anchor="nw", width=width, height=height)

    textvariable = sg.tk.StringVar()
    textvariable.set(text)
    entry = sg.tk.Entry(frame, textvariable=textvariable, justify=justify)
    entry.pack()

    # selects all text in the entry input widget
    entry.select_range(0, sg.tk.END)
    entry.icursor(sg.tk.END)
    entry.focus_force()
    # When you click outside of the selected widget, everything is returned back to normal
    entry.bind("<FocusOut>", lambda e, r=row, c=col, t=text, k='Focus_Out':callback(e, r, c, t, k))