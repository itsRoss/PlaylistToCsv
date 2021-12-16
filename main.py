import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


def main():
    # leggo l'id client e l'id client secret
    with open(r"C:\Users\nbada\PycharmProjects\playlistToCsv\credentials.txt") as f:
        [clientId, clientSecret] = f.read().split("\n")
        f.close()

    # connessione con l'api di spotify
    credentials = SpotifyClientCredentials(client_id=clientId, client_secret=clientSecret)
    sp = spotipy.Spotify(auth_manager=credentials)

    # recupero il link della playlist
    linkPlaylist = input("Inserire il link della playlist che si vuole salvare: ")
    playlist = sp.playlist(linkPlaylist)

    # recupero il numero delle canzoni all'interno della playlist
    num_canzoni = playlist["tracks"]["total"]

    # array che contiene la lista delle tracce nella plylist
    tracks = playlist["tracks"]

    # array che contiene gli items
    items = tracks["items"]

    # se la playlist ha più di cento tracce estendo items
    while tracks['next']:
        tracks = sp.next(tracks)
        items.extend(tracks['items'])

    # creo delle liste che conterranno le informazioni che mi servono
    lista_canzoni = getSongs(items, num_canzoni)
    lista_album = getAlbum(items, num_canzoni)
    lista_artisti = getArtist(items, num_canzoni)

    # prendo in input il nome del file da salvare
    nomeFile = input("Inserire il nome del file in cui si vuole salvare il risultato: ")

    # scrivo nel file csv le informazioni
    writeCsv(nomeFile, lista_canzoni, lista_album, lista_artisti)


# metodo per recuperare le canzoni all'interno di arr
def getSongs(arr, numCanzoni):
    i = 0
    lista = []
    while i < numCanzoni:
        canzone = arr[i]["track"]["name"]
        lista.append(canzone)

        i += 1
    return lista


# metodo per recuperare il nome dell'album della canzone
def getAlbum(arr, numCanzoni):
    i = 0
    lista = []
    while i < numCanzoni:
        album = arr[i]["track"]["album"]["name"]
        lista.append(album)

        i += 1
    return lista


# metodo che recupera gli artisti per ogni canzone
def getArtist(arr, numCanzoni):
    i = 0
    artists = ""
    res = []
    while i < numCanzoni:
        for k in arr[i]["track"]["artists"]:
            artists += k["name"] + " "
        res.append(artists)
        artists = ""
        i = i + 1

    return res


# metodo che scrive le informazioni corrette nel file csv
def writeCsv(nome_file, canzoni, album, artisti):

    intestazione = ["Nome traccia", "Album", "Artisti"]
    dati = list(zip(canzoni, album, artisti))
    rows = dati

    with open("%s.csv" % nome_file, 'w', newline='') as f:
        write = csv.writer(f)
        write.writerow(intestazione)
        write.writerows(rows)


if __name__ == "__main__":
    main()