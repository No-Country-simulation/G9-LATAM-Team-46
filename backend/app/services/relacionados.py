from app.ml.dataset_loader import cargar_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

TOP_K_RELACIONADOS = 3


def obtener_relacionados(texto_usuario: str, categoria: str) -> list[dict]:
    dataset = cargar_dataset()
    if dataset is None:
        return []

    subset = dataset[dataset["categoria"] == categoria].reset_index(drop=True)
    if subset.empty:
        return []

    corpus = (subset["titulo"].fillna("") + " " + subset["texto"].fillna("")).tolist()

    vectorizer = TfidfVectorizer(max_features=20000)
    matriz = vectorizer.fit_transform(corpus)
    vector_usuario = vectorizer.transform([texto_usuario])

    similitudes = cosine_similarity(vector_usuario, matriz)[0]
    top_idx = similitudes.argsort()[::-1][:TOP_K_RELACIONADOS]

    return [
        {
            "titulo": subset.iloc[i]["titulo"],
            "texto": subset.iloc[i]["texto"],
        }
        for i in top_idx
    ]