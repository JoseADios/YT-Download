import streamlit as st
from pytube import Search
import time
import wx
from streamlit.components.v1 import html
from pytube.innertube import _default_clients
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]


ytListComplete = []
if 'downloadedList' not in st.session_state:
    st.session_state.downloadedList = []

def setData(searchKey):
    global ytListComplete
    if searchKey not in st.session_state:
        s = Search(searchKey)
        ytListComplete = s.results[:5]
        st.session_state[searchKey] = ytListComplete
    else:
        ytListComplete = st.session_state[searchKey]


def limitText(text):
    limit = 55
    if (len(text) > limit):
        return text[:limit] + '...'
    return text


def format_att(value, name):
    return f"{value}{name}" if value else ""


# configuracion de la pagina -----------
st.set_page_config(
   page_title="YT Down Client",
   page_icon="⬇️",
   layout="centered",
   initial_sidebar_state="expanded",
)


# Crear la aplicación wx antes de usar cualquier método wx
app = wx.App(False)   



# ---------------------------------------- Interfaz --------------------------------------


# titulo
st.title('You:red[Tube] Download ⬇️')

with st.form("my_form"):
    col1, col2 = st.columns([5, 1], vertical_alignment='bottom')
    searchTexkt = col1.text_input('Palabra clave o link del video')
    button = col2.form_submit_button('Buscar  🔎')

st.markdown("---")


# -------- Obtencion de los videos ---------
setData(searchTexkt)

x = 0

for video in ytListComplete:
    col1, col2 = st.columns(2, vertical_alignment='center')

    seconds = time.strftime("%H:%M:%S", time.gmtime(video.length))
    downUrl = ''

    st.markdown("---")
    # Crear un contenedor HTML para la miniatura con el tiempo del video
    video_iframe = f"""
            <a href="{video.watch_url}" target="_blank">
                <div style="position: relative; display: inline-block;">
                    <img src="{video.thumbnail_url}" style="width: 100%; height: 100%;"/>
                    <div style="position: absolute; bottom: 0; right: 0; background-color: rgba(0, 0, 0, 0.6); color: white; padding: 2px 5px; font-size: 14px;">
                        {seconds}
                    </div>
                </div>
            </a>
            """

    col1.markdown(video_iframe, unsafe_allow_html=True)
    videoTitle = '##### ' + limitText(video.title)

    col2.markdown(videoTitle, help=video.title)

    options = video.streams.fmt_streams

    quality = col2.selectbox(
        'Calidad', options, key='quality'+str(x), format_func=lambda x: f'{"📽️" if "video" == str(x.type)  else "🎼"} {x.mime_type} {format_att(getattr(x, "resolution", ""),"")} {format_att(getattr(x, "fps", ""), "fps")} {format_att(getattr(x, "abr", ""), "")}')
    
    # downUrl = video.streams.get_by_itag(quality.itag).url
    size = col2.empty()
    size.write(str(quality.filesize_mb) + 'Mb')

    if col2.button('Generar link ⬇️', key=f'accept{x}', use_container_width=True):
        col2.markdown(f'[Descargar ↗️]({video.streams.get_by_itag(quality.itag).url})')
    x += 1



st.markdown("© 2024 YouTube Download.")
st.markdown('---')