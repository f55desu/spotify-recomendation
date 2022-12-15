import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity


#ИЗМЕНЕНИЕ ДАТАСЕТА И ВЫВОД РЕКОМЕНДАЦИИ ПО КНИГЕ
def modif_dataset(df, song_name, songsCount=6, get_similarity_rate=False):
    df2 = df.copy()
    df = df.drop(columns=['type', 'id', 'uri', 'analysis_url', 'Unnamed: 0', 'title', 'S', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'uri', 'analysis_url', 'duration_ms', 'time_signature', 'genre', 'Unnamed: 0', 'title'])

    genres = df2['genre'].unique()
    countOfGenres = []
    for i in range(len(genres)):
        countOfGenres.append(i)
    df2['genre'].replace(genres, countOfGenres, inplace=True)
    
    song_names = pd.DataFrame({'song_name':df2['song_name']})
    song_names.index = [i for i in range(15434)]
    df2.set_index('song_name',inplace=True)

    #Масштабирование функций
    cols = df2.columns[:4]
    clf = MinMaxScaler()
    scalled = clf.fit_transform(df2[cols])

    #Высчитывание scalled для каждого столбца
    i = 0
    for col in cols:
        df2[col] = scalled[:,i]
        i += 1

    df2 = df2.fillna(df2.mean())
    df2 = df2.drop(columns=['type', 'id', 'uri', 'track_href', 'analysis_url', 'Unnamed: 0', 'title'])

    #получения индекса трэка
    index_song = song_names.index[song_names['song_name'].eq(song_name)]
    index_song_int = index_song[0]

    #Алгоритм NearestNeighbors для получения ближайших трэков по значению
    kn = NearestNeighbors(n_neighbors=songsCount+1,metric='manhattan')
    #ERROR
    kn.fit(df2)

    #индексы, указывающие значение индекса рекомендуемых книг
    distances, indices = kn.kneighbors(df2.loc[song_names.loc[index_song_int]])
    nearest_songs = [song_names.loc[i][0] for i in indices.flatten()][1:]
    
    if not get_similarity_rate:
        return nearest_songs
    
    sim_rates = []
    links = []
    for song in nearest_songs:
        sim = cosine_similarity(df2.loc[song_names.loc[index_song_int]],[df2.loc[song]]).flatten()

        link = df[df['song_name'] == song]['track_href'].values[0]
        link = link.replace('api.', 'open.')
        link = link.replace('v1/', '')
        link = link.replace('tracks', 'track')

        links.append(link)
        sim_rates.append(sim[0])

    # Строки столбцы
    headers = {'Рекомедованные треки':nearest_songs, 'Ссылка': links, 'Сходство':sim_rates}
    recommended_songs = pd.DataFrame(headers)
    values_tab = recommended_songs.values.tolist()

    return values_tab