import streamlit as st
from pytube import Search
import time


class SearchVideos:
    def __init__(self):
        self.ytList = []

    def setData(self, searchKey):
        if searchKey not in st.session_state:
            s = Search(searchKey)
            self.ytList = s.results[:5]
            st.session_state[searchKey] = self.ytList
        else:
            self.ytList = st.session_state[searchKey]

    def getObjects(self):
        return self.ytList


# instancia de la clase
objSearch = SearchVideos()

# titulo
st.title('You:red[Tube] Download ⬇️')


with st.form("my_form"):
    searchTexkt = st.text_input('Search', 'Hoy')
    button = st.form_submit_button('Buscar')

objSearch.setData(searchTexkt)


def limitText(text):
    limit = 100
    if (len(text) > limit):
        return text[:limit] + '...'
    return text


def downVideo(x):
    print('Descargando '+str(x))


# crear una funcion para crear el elemento de video
def showVideos(results):
    for x in range(len(results)):
        with st.container(height=220, border=True):
            res = results[x]
            col1, col2 = st.columns(2, vertical_alignment='center')

            seconds = time.strftime("%H:%M:%S", time.gmtime(res.length))
            # Crear un contenedor HTML para la miniatura con el tiempo del video
            video_iframe = f"""
            <a href="{res.watch_url}" target="_blank">
                <div style="position: relative; display: inline-block;">
                    <img src="{res.thumbnail_url}" style="width: 100%; height: 100%;"/>
                    <div style="position: absolute; bottom: 0; right: 0; background-color: rgba(0, 0, 0, 0.6); color: white; padding: 2px 5px; font-size: 14px;">
                        {seconds}
                    </div>
                </div>
            </a>
            """
            col2.text(res.streams)

            col1.markdown(video_iframe, unsafe_allow_html=True)
            videoTitle = '##### ' + limitText(res.title)
            col2.markdown(videoTitle)

            if col2.button('Descargar ⬇️', key='btnDown'+str(x)):
                downVideo(x)
                

results = objSearch.getObjects()

showVideos(results)
