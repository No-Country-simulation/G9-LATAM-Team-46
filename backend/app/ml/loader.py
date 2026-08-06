def cargar_modelo():
    """
    Mock temporal. Cuando Persona 5 me entregue el modelo real (.joblib),
    esta función la reemplazo por la carga real:

    import joblib
    modelo = joblib.load("ruta/al/modelo.joblib")
    return modelo
    """
    return "modelo_mock_temporal"