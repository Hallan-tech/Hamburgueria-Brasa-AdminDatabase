"""Monta a página de cada nível: pergunta, gráfico e tabela."""
import streamlit as st

from src.db import consulta, mensagem_erro
from src.graficos import desenhar
from src.perguntas import NIVEIS, por_nivel, resposta


def escrever(texto):
    # No Streamlit, dois "$" no mesmo texto viram fórmula de matemática.
    st.markdown(texto.replace("$", "\\$"))


def mostrar_pergunta(p):
    with st.container(border=True):
        escrever(f"#### Q{p['numero']}. {p['titulo']}")
        escrever(p["enunciado"])
        st.caption("Conceitos: " + ", ".join(p["conceitos"]))
        colunas = ", ".join(p["colunas_esperadas"])
        sql = resposta(p)

        if sql == "":
            st.info(f"Ainda não respondida. Escreva a consulta em Q{p['numero']} no arquivo src/respostas.py. "
                    f"Colunas do resultado: {colunas}")
            with st.expander("Dica"):
                escrever(p["dica"])
            return

        try:
            tabela = consulta(sql)
        except Exception as erro:
            st.error("Erro ao executar a consulta: " + mensagem_erro(erro=erro))
            st.code(sql, language="sql")
            return

        if tabela.empty:
            st.warning("A consulta não trouxe nenhuma linha. Confira os filtros do WHERE.")

        faltando = [c for c in p["colunas_esperadas"] if c not in tabela.columns]
        if faltando:
            st.warning(f"O resultado precisa ter as colunas {colunas}. Use AS para dar esses nomes. "
                       f"Colunas que vieram: {', '.join(tabela.columns)}")
        else:
            desenhar(tabela, p["visual"], p["moeda"])

        if p["visual"]["tipo"] != "metricas" or faltando:
            formato = {c: st.column_config.NumberColumn(format="R$ %.2f") for c in p["moeda"]}
            st.dataframe(tabela, hide_index=True, column_config=formato)


def mostrar_nivel(nivel):
    titulo, descricao = NIVEIS[nivel]
    st.title(titulo)
    st.write(descricao)
    perguntas = por_nivel(nivel)
    feitas = len([p for p in perguntas if resposta(p) != ""])
    st.progress(feitas / len(perguntas), text=f"{feitas} de {len(perguntas)} respondidas neste nível")
    for p in perguntas:
        mostrar_pergunta(p)
