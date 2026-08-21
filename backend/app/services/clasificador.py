from fastapi import HTTPException, status
from app.schemas.contenido import ContenidoEntrada, ContenidoSalida, CategoriaRanking, ContenidoRelacionado
from app.ml.loader import cargar_modelo
from app.ml.preprocesamiento import limpiar
from app.services.relacionados import obtener_relacionados

modelo = cargar_modelo()

TOP_K_PALABRAS_CLAVE = 4


def clasificar_contenido(entrada: ContenidoEntrada) -> ContenidoSalida:
    if modelo is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="El modelo de clasificación aún no está disponible. Intenta más tarde.",
        )

    texto_limpio = limpiar(f"{entrada.titulo} {entrada.texto}")

    proba = modelo.predict_proba([texto_limpio])[0]
    idx = proba.argmax()

    tfidf = modelo.named_steps["tfidf"]
    vector = tfidf.transform([texto_limpio])
    vocabulario = tfidf.get_feature_names_out()
    top_idx = vector.toarray()[0].argsort()[::-1][:TOP_K_PALABRAS_CLAVE]
    palabras_clave = [vocabulario[i] for i in top_idx if vector[0, i] > 0]

    orden_ranking = proba.argsort()[::-1]
    ranking_categorias = [
        CategoriaRanking(
            categoria=modelo.classes_[i],
            probabilidad=round(float(proba[i]), 2),
        )
        for i in orden_ranking
    ]

    categoria_ganadora = modelo.classes_[idx]
    relacionados_raw = obtener_relacionados(texto_limpio, categoria_ganadora)
    contenidos_relacionados = [ContenidoRelacionado(**r) for r in relacionados_raw]

    return ContenidoSalida(
        categoria=categoria_ganadora,
        probabilidad=round(float(proba[idx]), 2),
        informacion_adicional=palabras_clave,
        ranking_categorias=ranking_categorias,
        contenidos_relacionados=contenidos_relacionados,
    )