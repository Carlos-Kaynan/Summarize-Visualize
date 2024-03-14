import google.generativeai as genai
from openai import OpenAI
import streamlit as st


def resumo_descricao(model, arquivo, qtd_topicos):
  comando_resumo = 'resuma desse texto: '
  comando_descricao = ('descreva esse resumo como uma imagem: ')

  resumo = model.generate_content({comando_resumo + arquivo})

  with st.container():
    st.markdown("## Resumo")
    st.write(resumo.text)

  descricao = model.generate_content({comando_descricao + resumo.text})

  with st.container():
    st.markdown("## Descrição")
    st.write(descricao.text)

  return descricao


def gerar_imagens(descricao, OPENAI_API_KEY):
  client = OpenAI(api_key = OPENAI_API_KEY)

  response = client.images.generate(
    model="dall-e-3",
    prompt = descricao.text,
    size="1024x1024",
    quality="standard",
    n = 1,
  )

  image_url = response.data[0].url

  st.image(image_url, caption="Imagem", use_column_width=True)


def main():
    st.title("Summarize & Visualize")
    st.markdown('Automatizando Sumarização de Textos e Geração de Imagens')
    st.divider()

    with st.sidebar:
        st.title('Chaves das APIs')
        GOOGLE_API_KEY = st.text_input('| Gemini |', type='password')
        OPENAI_API_KEY = st.text_input('| OpenAI |', type='password')

        qtd_topicos = st.slider('Escolha a quantidade de topicos', 1, 10)

    genai.configure(api_key=GOOGLE_API_KEY)  
    model = genai.GenerativeModel('gemini-pro')

    uploaded_file = st.file_uploader("Escolha um arquivo de texto", type=["txt"])

    if uploaded_file is not None:
        arquivo = uploaded_file.getvalue().decode("utf-8")
      
        descricao = resumo_descricao(model, arquivo, str(qtd_topicos)) 
        
        gerar_imagens(descricao, OPENAI_API_KEY)
    else:
        st.error("Nenhum arquivo foi carregado.")

if __name__ == "__main__":
    main()
