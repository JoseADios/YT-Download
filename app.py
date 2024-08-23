import streamlit as st
from pytube import Search
import time
import wx
from pytube.innertube import _default_clients
_default_clients["ANDROID_MUSIC"] = _default_clients["ANDROID_CREATOR"]


ytListComplete = []
# ytList = []

# get results from youtube


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


def downVideo(ytObject, itag, path):
    
    
    print('Descargando...')
    # stream = ytObject.streams.get_by_itag(itag)
    # stream.download()
    print('Video descargado')



def format_att(value, name):
    return f"{value}{name}" if value else ""


# Crear la aplicación wx antes de usar cualquier método wx
app = wx.App(False)


# titulo
st.title('You:red[Tube] Download ⬇️')

with st.form("my_form"):
    col1, col2 = st.columns([5, 1], vertical_alignment='bottom')
    searchTexkt = col1.text_input('Palabra clave o enlace', 'no me llames')
    button = col2.form_submit_button('Buscar  🔎')

st.markdown("---")


setData(searchTexkt)

x = 0

start_time = time.time()

for video in ytListComplete:

    col1, col2 = st.columns(2, vertical_alignment='center')
    seconds = time.strftime("%H:%M:%S", time.gmtime(video.length))

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

    with col2.popover("Descargar", use_container_width=True):

        folder_path = './'

        placeholder = st.empty()

        dcol1, dcol2 = st.columns(2, vertical_alignment='bottom')
        if dcol1.button('Seleccionar 📁', key=f'select{x}', use_container_width=True):
            dialog = wx.DirDialog(None, 'Seleccione una carpeta:', style=wx.DD_DEFAULT_STYLE | wx.DD_NEW_DIR_BUTTON)
            
            if dialog.ShowModal() == wx.ID_OK:
                folder_path = dialog.GetPath() # folder_path will contain the path of the folder you have selected as string
            dialog.Destroy()

        placeholder.text(folder_path)

        dcol2.button('Aceptar ⬇️', key=f'accept{x}', on_click=downVideo(video, quality.itag, folder_path) , use_container_width=True)


    col2.text(str(quality.filesize_mb) + 'Mb')

    x += 1


# Sidebar content
st.markdown("© 2024 YouTube Download.")
st.markdown('---')