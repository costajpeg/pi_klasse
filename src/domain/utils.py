import unicodedata
import re


def normalizar_texto(texto: str) -> tuple[str, str, list[str]]:
    """
    Normaliza o texto:
    - sem_acento: minúsculas e sem acentos
    - sem_repeticao: remove repetições consecutivas de letras (ex: 'rr' -> 'r')
    - palavras: lista de palavras individuais normalizadas
    """
    if not texto:
        return "", "", []

    nfkd = unicodedata.normalize("NFKD", str(texto))
    sem_acento = "".join([c for c in nfkd if not unicodedata.combining(c)]).lower().strip()
    sem_repeticao = re.sub(r"(.)\1+", r"\1", sem_acento)
    palavras = sem_acento.split()

    return sem_acento, sem_repeticao, palavras


def corresponde_busca(termo_busca: str, *campos: str) -> bool:
    """
    Verifica se o termo de busca corresponde aos campos pesquisados.
    Permite busca por correspondência de termos não contíguos (ex: 'thais paixao' casa com 'Thais dos Santos Paixão').
    Também ignora maiúsculas/minúsculas, acentos e repetições de letras.
    """
    busca_limpa = (termo_busca or "").strip()
    if not busca_limpa:
        return True

    b_norm, b_comp, b_palavras = normalizar_texto(busca_limpa)
    if not b_palavras:
        return True

    textos_alvo = []
    palavras_alvo = []
    for c in campos:
        cn, cc, cp = normalizar_texto(c)
        if cn:
            textos_alvo.append(cn)
            palavras_alvo.extend(cp)

    texto_completo = " ".join(textos_alvo)
    texto_comprimido = re.sub(r"(.)\1+", r"\1", texto_completo)

    # 1. Correspondência exata da frase completa
    if b_norm in texto_completo or b_comp in texto_comprimido:
        return True

    # 2. Correspondência de cada palavra digitada (em qualquer ordem ou posição)
    todas_palavras_presentes = True
    for p in b_palavras:
        p_comp = re.sub(r"(.)\1+", r"\1", p)
        # Verifica se 'p' está no texto completo ou se alguma palavra do alvo contém ou inicia com 'p'
        if (
            p in texto_completo
            or p_comp in texto_comprimido
            or any(alvo.startswith(p) or p in alvo for alvo in palavras_alvo)
        ):
            continue
        else:
            todas_palavras_presentes = False
            break

    return todas_palavras_presentes

