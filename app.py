import streamlit as st
from pytube import Search
import time


class SearchVideos:
    def __init__(self):
        self.ytListComplete = []
        self.ytList = []

    # get results from youtube
    def setData(self, searchKey):
        if searchKey not in st.session_state:
            s = Search(searchKey)
            self.ytListComplete = s.results
            st.session_state[searchKey] = self.ytListComplete
        else:
            self.ytListComplete = st.session_state[searchKey]

        self.formatList()

    # set only needed properties
    def formatList(self):
        video_data = []

        for video in self.ytListComplete[:5]:
            video_info = {
                'video_id': video.video_id,
                'title': video.title,
                'thumbnail_url': video.thumbnail_url,
                'length': video.length,  # Duración en segundos
                'watch_url': video.watch_url,
                'streams': video.streams,
            }
            video_data.append(video_info)
        self.ytList = video_data

    def getObjects(self):
        return self.ytList

    def getDownOptions(self):
        options = []
        count = 0

        for video in self.ytList:
            st = {}
            streamList = []
            for stream in video['streams'].fmt_streams:
                streamList.append(stream)
            
            count = count + 1
            options.append(streamList)
        
        return options


# instancia de la clase
objSearch = SearchVideos()

# titulo
st.title('You:red[Tube] Download ⬇️')


with st.form("my_form"):
    col1, col2 = st.columns([5, 1], vertical_alignment='bottom')
    searchTexkt = col1.text_input('Palabra clave o enlace', 'tomorrow')
    button = col2.form_submit_button('Buscar  🔎')

objSearch.setData(searchTexkt)


def limitText(text):
    limit = 55
    if (len(text) > limit):
        return text[:limit] + '...'
    return text


def downVideo(x):
    print('Descargando '+str(x))

def format_att(value, name):
    return f"{value} {name}" if value else ""

# crear una funcion para crear el elemento de video
def showVideos(results):
    optionsByVideo = objSearch.getDownOptions()
    
    for x in range(len(results)):
        with st.container(height=220, border=True):
            res = results[x]
            col1, col2 = st.columns(2, vertical_alignment='center')

            options = optionsByVideo[x]

            # for op in options:
            #     print(f'Opcion: {op}')

            seconds = time.strftime("%H:%M:%S", time.gmtime(res['length']))
            # Crear un contenedor HTML para la miniatura con el tiempo del video
            video_iframe = f"""
            <a href="{res['watch_url']}" target="_blank">
                <div style="position: relative; display: inline-block;">
                    <img src="{res['thumbnail_url']}" style="width: 100%; height: 100%;"/>
                    <div style="position: absolute; bottom: 0; right: 0; background-color: rgba(0, 0, 0, 0.6); color: white; padding: 2px 5px; font-size: 14px;">
                        {seconds}
                    </div>
                </div>
            </a>
            """

            col1.markdown(video_iframe, unsafe_allow_html=True)
            videoTitle = '##### ' + limitText(res['title'])

            col2.markdown(videoTitle, help=res['title'])
            
            quality = col2.selectbox(
                'Calidad', options, key='quality'+str(x), format_func= lambda x: f'{x.mime_type} {format_att(getattr(x, "resolution", ""),"")} {format_att(getattr(x, "fps", ""), "fps")} {format_att(getattr(x, "abr", ""), "")}')
            
            if col2.button('Descargar', key='btnDown'+str(x)):
                downVideo(x)


results = objSearch.getObjects()

showVideos(results)
