
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from io import BytesIO

st.set_page_config(page_title="EMI Navigator 2.0", page_icon="🧭", layout="wide")

# ============================================================
# CONFIGURAÇÃO DO INSTRUMENTO
# ============================================================

DIMENSIONS = {
    "KNO": "Conhecimento e Transferência",
    "INO": "Inovação e Experimentação",
    "VAL": "Criação e Captura de Valor",
    "FOM": "Fomento e Financiamento",
    "INF": "Infraestrutura",
    "POL": "Políticas e Regulação",
}

QUESTIONS = {
"KNO": [
("KNO_P1", "A empresa troca e compartilha conhecimento com outras organizações.", "P"),
("KNO_V1", "A empresa participa de projetos com universidades ou centros de pesquisa.", "V"),
("KNO_V2", "A empresa troca informações com frequência com outras organizações.", "V"),
("KNO_V3", "A empresa promove ou participa de treinamentos e capacitações.", "V"),
("KNO_V4", "A empresa usa dados e conhecimento para tomar decisões.", "V"),
("KNO_V5", "A empresa possui formas organizadas de compartilhar conhecimento.", "V"),
("KNO_V6", "A empresa mantém parcerias e cooperação contínua com outras organizações.", "V"),
("KNO_R1", "A empresa costuma trabalhar de forma isolada, sem compartilhar conhecimento.", "R"),
],
"INO": [
("INO_P1", "A empresa é inovadora.", "P"),
("INO_V1", "A empresa lançou novos produtos, serviços, processos ou soluções nos últimos três anos.", "V"),
("INO_V2", "A empresa testa novas ideias antes de colocá-las em prática.", "V"),
("INO_V3", "A empresa investe em pesquisa, desenvolvimento ou testes de novas soluções.", "V"),
("INO_V4", "A empresa usa tecnologias digitais para acompanhar ou melhorar suas atividades.", "V"),
("INO_V5", "A empresa desenvolve projetos de inovação com outras organizações.", "V"),
("INO_V6", "A empresa consegue testar e colocar novas ideias em prática com rapidez.", "V"),
("INO_R1", "A empresa enfrenta muita resistência quando tenta colocar novas ideias em prática.", "R"),
],
"VAL": [
("VAL_P1", "As iniciativas da empresa geram valor para as pessoas e organizações envolvidas.", "P"),
("VAL_V1", "Os produtos, serviços ou soluções da empresa geram benefícios para clientes e parceiros.", "V"),
("VAL_V2", "Os projetos da empresa têm condições de continuar financeiramente.", "V"),
("VAL_V3", "As parcerias da empresa ajudam todos os envolvidos a gerar valor.", "V"),
("VAL_V4", "A empresa percebe ganhos financeiros, sociais ou outros benefícios nas iniciativas que realiza.", "V"),
("VAL_V5", "As soluções da empresa podem crescer e atender mais clientes ou usuários.", "V"),
("VAL_V6", "A empresa consegue atrair outras organizações interessadas em trabalhar com ela.", "V"),
("VAL_R1", "Muitas iniciativas da empresa terminam depois da fase inicial e não continuam.", "R"),
],
"FOM": [
("FOM_P1", "A empresa tem acesso a recursos e incentivos para desenvolver novas iniciativas.", "P"),
("FOM_V1", "A empresa já participou de editais, chamadas ou programas de apoio nos últimos três anos.", "V"),
("FOM_V2", "Existem recursos financeiros disponíveis para desenvolver os projetos da empresa.", "V"),
("FOM_V3", "A empresa recebe apoio de instituições públicas ou privadas para desenvolver novas iniciativas.", "V"),
("FOM_V4", "Os recursos disponíveis são suficientes para as necessidades dos projetos da empresa.", "V"),
("FOM_V5", "A empresa consegue se conectar com investidores ou instituições que oferecem recursos.", "V"),
("FOM_R1", "A falta de recursos financeiros dificulta a continuidade dos projetos da empresa.", "R"),
],
"INF": [
("INF_P1", "A infraestrutura disponível ajuda a empresa a desenvolver e colocar suas soluções em prática.", "P"),
("INF_V1", "A empresa possui uma boa infraestrutura digital para integrar e compartilhar dados.", "V"),
("INF_V2", "Os sistemas usados pela empresa conseguem trabalhar de forma integrada.", "V"),
("INF_V3", "A empresa utiliza plataformas ou sistemas digitais para melhorar suas atividades.", "V"),
("INF_V4", "A infraestrutura disponível na região atende às necessidades da empresa.", "V"),
("INF_V5", "A empresa possui acesso a espaços ou ambientes para testar novas soluções.", "V"),
("INF_R1", "A falta de infraestrutura dificulta o desenvolvimento e a implementação de novas soluções.", "R"),
],
"POL": [
("POL_P1", "As leis e regras favorecem o desenvolvimento de novas soluções.", "P"),
("POL_V1", "Existem políticas públicas que apoiam o desenvolvimento das empresas.", "V"),
("POL_V2", "As regras atuais permitem que a empresa teste e desenvolva novas ideias.", "V"),
("POL_V3", "Os programas e iniciativas de apoio têm continuidade.", "V"),
("POL_V4", "Os diferentes órgãos e setores envolvidos trabalham de forma alinhada.", "V"),
("POL_V5", "O poder público incentiva parcerias entre empresas e outras organizações.", "V"),
("POL_V6", "As regras permitem que novos produtos, serviços ou modelos de negócio sejam desenvolvidos.", "V"),
("POL_R1", "Mudanças políticas ou nas regras costumam interromper projetos da empresa.", "R"),
],
}

SCALE = {
    1: "1 — Discordo totalmente",
    2: "2 — Discordo",
    3: "3 — Nem concordo nem discordo",
    4: "4 — Concordo",
    5: "5 — Concordo totalmente",
}

def score_item(x, reverse=False):
    if reverse:
        x = 6 - x
    return ((x - 1) / 4) * 100

def maturity(score):
    if score <= 20:
        return "Emergente"
    if score <= 40:
        return "Em desenvolvimento"
    if score <= 60:
        return "Consolidado"
    if score <= 80:
        return "Avançado"
    return "Maduro"

def maturity_target(score):
    # Alvo inicial: próxima faixa de maturidade.
    if score <= 20: return 40
    if score <= 40: return 60
    if score <= 60: return 80
    if score <= 80: return 100
    return 100

def locus(dimension):
    if dimension in ["KNO", "INO", "VAL"]:
        return "Organizacional / compartilhado"
    if dimension == "FOM":
        return "Compartilhado / externo"
    if dimension == "INF":
        return "Compartilhado / ecossistema"
    return "Externo / ecossistema"

def recommendation(dimension, score, importance):
    name = DIMENSIONS[dimension]
    if score >= 75:
        return f"Preservar e usar {name} como base para apoiar outras melhorias."
    if score < 50:
        actions = {
            "KNO": "Criar rotinas de troca de conhecimento, parcerias e capacitação.",
            "INO": "Estruturar pilotos, testes e um processo contínuo de inovação.",
            "VAL": "Revisar benefícios, sustentabilidade financeira, escalabilidade e valor compartilhado.",
            "FOM": "Mapear editais, incentivos, investidores e fontes de financiamento.",
            "INF": "Identificar gargalos de infraestrutura, integração de sistemas e ambientes de teste.",
            "POL": "Mapear barreiras regulatórias, políticas de apoio e oportunidades de articulação institucional.",
        }
        return actions[dimension]
    if importance >= 4:
        return f"Priorizar uma melhoria incremental em {name} e acompanhar sua evolução."
    return f"Manter acompanhamento de {name} e buscar oportunidades de melhoria."

def build_results(answers, importance):
    rows = []
    for dim, qs in QUESTIONS.items():
        vals = []
        for code, text, typ in qs:
            x = answers.get(code)
            if x is None:
                continue
            vals.append(score_item(x, typ == "R"))
        score = np.mean(vals) if vals else np.nan
        rows.append({
            "Código": dim,
            "Dimensão": DIMENSIONS[dim],
            "Pontuação": round(score, 2),
            "Maturidade": maturity(score),
            "Alvo inicial": maturity_target(score),
            "Gap": round(max(0, maturity_target(score) - score), 2),
            "Importância": importance.get(dim, 3),
            "Prioridade": round(max(0, maturity_target(score) - score) * importance.get(dim, 3), 2),
            "Locus": locus(dim),
            "Diagnóstico": (
                "Base forte" if score >= 75
                else "Ponto de atenção" if score < 50
                else "Zona intermediária"
            ),
            "Recomendação": recommendation(dim, score, importance.get(dim, 3))
        })
    df = pd.DataFrame(rows)
    emi = df["Pontuação"].mean()
    return df, emi

def radar(df):
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=df["Pontuação"].tolist() + [df["Pontuação"].iloc[0]],
        theta=df["Código"].tolist() + [df["Código"].iloc[0]],
        fill="toself",
        name="EMI"
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0,100])),
        showlegend=False,
        height=500
    )
    return fig

# ============================================================
# INTERFACE
# ============================================================

st.title("🧭 EMI Navigator 2.0")
st.caption("Diagnóstico de maturidade, forças, dores, prioridades e roadmap de melhoria.")

with st.sidebar:
    st.header("Navegação")
    page = st.radio(
        "Etapa",
        ["1. Empresa", "2. Questionário EMI", "3. Diagnóstico", "4. Prioridades", "5. Roadmap", "6. Exportar"]
    )
    st.divider()
    st.info(
        "O EMI é o núcleo de mensuração. As camadas de diagnóstico, prioridade e roadmap "
        "são extensões do protótipo e precisam ser validadas empiricamente."
    )

if "company" not in st.session_state:
    st.session_state.company = {}
if "answers" not in st.session_state:
    st.session_state.answers = {}
if "importance" not in st.session_state:
    st.session_state.importance = {d: 3 for d in DIMENSIONS}

if page == "1. Empresa":
    st.header("1. Informações da empresa")
    st.write("Preencha as informações básicas antes de responder ao instrumento.")
    c1, c2 = st.columns(2)
    with c1:
        st.session_state.company["Empresa"] = st.text_input("Nome da empresa", value=st.session_state.company.get("Empresa",""))
        st.session_state.company["Setor"] = st.text_input("Setor de atuação", value=st.session_state.company.get("Setor",""))
    with c2:
        st.session_state.company["Cidade"] = st.text_input("Cidade/região", value=st.session_state.company.get("Cidade",""))
        st.session_state.company["Perfil"] = st.selectbox(
            "Perfil",
            ["Empresa", "Startup", "Indústria", "Serviço", "Tecnologia", "Outro"],
            index=0
        )
    st.success("Informações salvas nesta sessão.")
    st.markdown("### Próximo passo")
    st.write("Acesse **2. Questionário EMI** no menu lateral.")

elif page == "2. Questionário EMI":
    st.header("2. Questionário EMI")
    st.write("Escala de 1 a 5. Os itens reversos são tratados automaticamente no cálculo.")
    progress = 0
    total = sum(len(qs) for qs in QUESTIONS.values())

    for dim, qs in QUESTIONS.items():
        with st.expander(f"{dim} — {DIMENSIONS[dim]}", expanded=True):
            for code, text, typ in qs:
                current = st.session_state.answers.get(code, 3)
                st.session_state.answers[code] = st.radio(
                    f"{code}: {text}",
                    options=[1,2,3,4,5],
                    index=current-1,
                    format_func=lambda x: SCALE[x],
                    horizontal=True,
                    key=f"answer_{code}"
                )
                if typ == "R":
                    st.caption("Item reverso — a pontuação será invertida no cálculo.")

    st.divider()
    st.header("Importância para a empresa")
    st.write("Esta pergunta é complementar ao EMI e será usada apenas para priorização.")
    for dim in DIMENSIONS:
        st.session_state.importance[dim] = st.slider(
            f"Quanto é importante melhorar **{dim} — {DIMENSIONS[dim]}** para sua empresa hoje?",
            1, 5, st.session_state.importance.get(dim, 3),
            format="%d"
        )
    st.success("Questionário preenchido. Vá para **3. Diagnóstico**.")

elif page == "3. Diagnóstico":
    st.header("3. Diagnóstico")
    if len(st.session_state.answers) < sum(len(qs) for qs in QUESTIONS.values()):
        st.warning("Responda todas as perguntas antes de analisar o diagnóstico.")
    else:
        df, emi = build_results(st.session_state.answers, st.session_state.importance)
        st.session_state.results = df
        st.session_state.emi = emi

        c1,c2,c3 = st.columns(3)
        c1.metric("EMI", f"{emi:.1f}/100")
        c2.metric("Maturidade geral", maturity(emi))
        c3.metric("Dimensões fortes", int((df["Pontuação"] >= 75).sum()))

        st.plotly_chart(radar(df), use_container_width=True)

        st.subheader("Mapa das dimensões")
        st.dataframe(
            df[["Código","Dimensão","Pontuação","Maturidade","Diagnóstico","Gap","Locus"]],
            use_container_width=True,
            hide_index=True
        )

        st.subheader("🟢 Base forte")
        strong = df[df["Pontuação"] >= 75]
        if len(strong):
            for _, r in strong.iterrows():
                st.success(f"{r['Código']} — {r['Dimensão']}: {r['Pontuação']:.1f}/100")
        else:
            st.info("Nenhuma dimensão atingiu o limiar provisório de 75 pontos.")

        st.subheader("🔴 Dores / pontos críticos")
        pain = df[df["Pontuação"] < 50].sort_values("Prioridade", ascending=False)
        if len(pain):
            for _, r in pain.iterrows():
                st.error(f"{r['Código']} — {r['Dimensão']}: {r['Pontuação']:.1f}/100 | {r['Locus']}")
        else:
            st.info("Nenhuma dimensão ficou abaixo do limiar provisório de 50 pontos.")

elif page == "4. Prioridades":
    st.header("4. Prioridades de intervenção")
    if "results" not in st.session_state:
        st.warning("Execute primeiro o diagnóstico.")
    else:
        df = st.session_state.results.copy().sort_values("Prioridade", ascending=False)
        st.write("Prioridade provisória = **Gap × Importância**.")
        st.dataframe(
            df[["Código","Dimensão","Pontuação","Alvo inicial","Gap","Importância","Prioridade","Locus"]],
            use_container_width=True,
            hide_index=True
        )

        st.subheader("Top prioridades")
        top = df.head(3)
        for i, (_, r) in enumerate(top.iterrows(), 1):
            st.markdown(f"### {i}. {r['Dimensão']}")
            st.write(
                f"**Situação:** {r['Pontuação']:.1f}/100 ({r['Maturidade']})  \n"
                f"**Gap:** {r['Gap']:.1f} pontos  \n"
                f"**Importância:** {r['Importância']}/5  \n"
                f"**Locus:** {r['Locus']}"
            )
            st.info(r["Recomendação"])

        st.caption(
            "Os limiares e a fórmula de priorização são regras iniciais do protótipo, "
            "não resultados estatisticamente validados."
        )

elif page == "5. Roadmap":
    st.header("5. Roadmap de melhoria")
    if "results" not in st.session_state:
        st.warning("Execute primeiro o diagnóstico.")
    else:
        df = st.session_state.results.copy().sort_values("Prioridade", ascending=False)
        strong = df[df["Pontuação"] >= 75]

        st.subheader("Estratégia")
        st.write(
            "A lógica do roadmap é **usar as bases fortes existentes para apoiar as dimensões prioritárias**, "
            "considerando também o locus de ação."
        )

        periods = [
            ("0–3 meses", df.head(2)),
            ("3–6 meses", df.iloc[2:4]),
            ("6–12 meses", df.iloc[4:6]),
        ]

        for period, subset in periods:
            st.markdown(f"## {period}")
            if subset.empty:
                st.write("Sem ações definidas.")
                continue
            for _, r in subset.iterrows():
                st.markdown(f"### {r['Código']} — {r['Dimensão']}")
                st.write(f"**Prioridade:** {r['Prioridade']:.1f} | **Locus:** {r['Locus']}")
                st.write(f"**Ação sugerida:** {r['Recomendação']}")
                if len(strong):
                    s = strong.iloc[0]
                    if s["Código"] != r["Código"]:
                        st.write(
                            f"**Base que pode apoiar:** {s['Código']} — {s['Dimensão']} "
                            f"({s['Pontuação']:.1f}/100)."
                        )

        st.divider()
        st.subheader("🔄 Reavaliação")
        st.write(
            "Após a implementação das ações, reaplicar o diagnóstico e comparar o EMI, "
            "as seis dimensões, os gaps e as prioridades com a avaliação anterior."
        )

elif page == "6. Exportar":
    st.header("6. Exportar diagnóstico")
    if "results" not in st.session_state:
        st.warning("Execute primeiro o diagnóstico.")
    else:
        df = st.session_state.results.copy()
        company = st.session_state.company

        st.subheader("Resumo")
        st.write(f"**Empresa:** {company.get('Empresa','Não informado')}")
        st.write(f"**EMI:** {st.session_state.emi:.1f}/100")
        st.write(f"**Maturidade:** {maturity(st.session_state.emi)}")

        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Diagnostico")
            pd.DataFrame([company]).to_excel(writer, index=False, sheet_name="Empresa")
            answers_df = pd.DataFrame(
                [{"Codigo": k, "Resposta": v} for k,v in st.session_state.answers.items()]
            )
            answers_df.to_excel(writer, index=False, sheet_name="Respostas")
        output.seek(0)

        st.download_button(
            "⬇️ Baixar diagnóstico em Excel",
            data=output,
            file_name="diagnostico_emi_navigator.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
