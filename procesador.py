import re


def limpiar_texto(texto):
    texto = texto.upper()

    reemplazos = {
        "ELECTRICO": "ELÉCTRICO",
        "ATENCION": "ATENCIÓN",
        "INTERRUPCION": "INTERRUPCIÓN",
        "RECONEXION": "RECONEXIÓN",
        "DOMICILIO": "DOMICILIO"
    }

    for k, v in reemplazos.items():
        texto = texto.replace(k, v)

    texto = texto.replace("-", " ")
    texto = re.sub(r"\s+", " ", texto)

    return texto.strip()


def normalizar_campos(texto):
    campos = re.split(r"\t+|\s{2,}", texto)
    return [c.strip() for c in campos if c.strip()]


def extraer_numero_atencion(texto):
    m = re.findall(r"\b\d{11}\b", texto)
    return m[0] if m else ""


def extraer_suministro(texto):
    nums = re.findall(r"\b\d{8}\b", texto)
    ignorar = {"20260615", "20260616"}

    for n in nums:
        if n not in ignorar:
            return n
    return ""


def extraer_alimentador(texto):
    m = re.search(r"\bA\d{4}\b", texto)
    return m.group(0) if m else ""


def extraer_circuito(texto):

    import re

    # 1. Buscar inicio (alimentador A####)
    inicio = re.search(r"\bA\d{4}\b", texto)
    if not inicio:
        return ""

    # 2. Buscar fin (URBANO o RURAL, ambos válidos)
    fin = re.search(r"\b(URBANO|RURAL)\b", texto, re.IGNORECASE)
    if not fin:
        return ""

    # 3. Extraer bloque entre ambos
    bloque = texto[inicio.end():fin.start()]

    # 4. Buscar D#### y E#### dentro del bloque
    d = re.search(r"D\d+", bloque)
    e = re.search(r"E\d+", bloque)

    if d and e:
        return f"CIRCUITO BT {d.group(0)} DE LA SED {e.group(0)}"

    return ""


def detectar_petitorio(texto):

    import re

    # 1. Buscar fecha de inicio del caso real (usar segunda fecha si existe)
    fechas = list(re.finditer(r"\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}", texto))

    if len(fechas) >= 2:
        inicio = fechas[1].end()
    elif len(fechas) == 1:
        inicio = fechas[0].end()
    else:
        return ""

    sub = texto[inicio:]

    # 2. Cortar en flags o estructura técnica
    fin = re.search(r"(Pendiente|False\s+False|A\d{4}\b|CIRCUITO|Circuito)", sub, re.IGNORECASE)

    if fin:
        sub = sub[:fin.start()]

    # 3. Limpieza final
    sub = re.sub(r"\s+", " ", sub).strip()

    return sub
    
def construir_salida1(petitorio, suministro, boleta, alimentador, circuito):

    partes = [petitorio, suministro, boleta, alimentador, circuito]
    partes = [p for p in partes if p]

    return re.sub(r"\s+", " ", " ".join(partes)).strip()


def convertir_reiteracion(texto):

    m = re.search(r"VIA\s+WHATSAPP\s+(\d+)", texto, re.IGNORECASE)

    if not m:
        return texto

    n = int(m.group(1))

    mapa = {
        1: "1ERA REITERACIÓN",
        2: "2DA REITERACIÓN",
        3: "3RA REITERACIÓN",
        4: "4TA REITERACIÓN"
    }

    rep = mapa.get(n, f"{n}MA REITERACIÓN")

    return re.sub(r"VIA\s+WHATSAPP\s+\d+", f"VIA WHATSAPP {rep}", texto, flags=re.IGNORECASE)


def procesar_registro(texto):

    texto_original = texto
    texto_limpio = limpiar_texto(texto)

    # EXTRACCIONES (usar limpio para patrones simples)
    boleta = extraer_numero_atencion(texto_limpio)
    suministro = extraer_suministro(texto_limpio)
    alimentador = extraer_alimentador(texto_limpio)
    circuito = extraer_circuito(texto_limpio)

    # PETITORIO (OBLIGATORIO original)
    petitorio = detectar_petitorio(texto_original)
    petitorio = convertir_reiteracion(petitorio)

    # SALIDA
    salida1 = construir_salida1(
        petitorio,
        suministro,
        boleta,
        alimentador,
        circuito
    )

    salida2 = (
        "Estimados Ingenieros:\n\n"
        f"Adjunto reporte de {petitorio}, favor de coordinar con quien corresponda la atencion y el descargo.\n\n"
        "Saludos cordiales."
    )

    return salida1, salida2