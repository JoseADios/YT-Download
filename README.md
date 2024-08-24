# 📹 YouTube Download Project

Este proyecto permite descargar videos de YouTube utilizando `pytube` y `streamlit`. Hay dos aplicaciones principales en este proyecto:

1. **ClientDownload:** 🎯 Permite a los usuarios generar enlaces de descarga que pueden ser utilizados en el cliente.
2. **LocalDownload:** 💻 Descarga los videos directamente en la máquina local del usuario.

## 📁 Estructura del Proyecto

- `ClientDownload/app.py`: 🎯 Código para generar enlaces de descarga en el cliente.
- `LocalDownload/app.py`: 💻 Código para descargar videos localmente.

## ⚙️ Requisitos

- 🐍 Python 3.7 o superior
- 🖥️ `streamlit`, `pytube`, `wxPython`

## 🚀 Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu-usuario/tu-repositorio.git
   cd tu-repositorio
   ```

2. Instala los requisitos:
   ```bash
   pip install -r requirements.txt
   ```

## ▶️ Ejecución

### 🎯 ClientDownload

```bash
cd ClientDownload
streamlit run app.py
```

### 💻 LocalDownload

```bash
cd LocalDownload
streamlit run app.py
```

### 🛠️ Solución de Problemas

#### Error con `cipher.py`

Algunos usuarios pueden encontrar un problema con la funcionalidad de descarga de videos debido a un error en el archivo `cipher.py` dentro de la biblioteca `pytube`. Este es un problema conocido y se puede resolver modificando un patrón regex específico.

**Solución:**

1. Localiza el archivo `cipher.py` dentro de la biblioteca `pytube`.
2. Busca la función `get_throttling_function_name`.
3. Modifica el primer patrón regex en `function_patterns` para incluir un grupo de captura para el nombre del método.

Cambia esta línea:
```python
r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)'
```

El segmento final de código en `cipher.py` debería verse así:

```python
function_patterns = [
    r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)',
    r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
]
```

Esta solución ha sido probada con varios videos y debería resolver el problema. Para más detalles, puedes consultar el [issue en GitHub](https://github.com/pytube/pytube/issues/1678).


## ⚠️ Exención de Responsabilidad

Este proyecto se proporciona con fines educativos y de prueba únicamente. No está destinado para su uso en la descarga de contenido con derechos de autor de YouTube. La descarga de videos de YouTube sin el permiso del creador del contenido puede infringir los términos de servicio de YouTube y las leyes de derechos de autor. Usa este software bajo tu propia responsabilidad y asegúrate de cumplir con las leyes y regulaciones locales.

## 📜 Licencia

Este proyecto no incluye una licencia específica. Por favor, revisa y sigue las leyes y regulaciones locales antes de usar este software.
