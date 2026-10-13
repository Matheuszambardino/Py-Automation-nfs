import os
import xml.etree.ElementTree as ET
import pandas as pd
import subprocess
import sys

ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

# Ler os campos 
def get_text(element, path, default="N/A"):
    node = element.find(path, ns)
    if node is None or node.text is None:
         return default 
    return node.text.strip()

def get_float(element, path, default=0.0):
    valor = get_text(element, path, str(default))
    try:
        return float(valor) 
    except ValueError:
        return default

# Ler nfe individual
def ler_xml_nfe(caminho_xml):
    try:
        tree = ET.parse(caminho_xml)
        root = tree.getroot()
        nome_arquivo = os.path.basename(caminho_xml)

        inf_nfe = root.find('.//nfe:infNFe', ns)
        chave_nfe = "N/A"

        if inf_nfe is not None:
             chave_nfe = inf_nfe.attrib.get("id", "")
             if chave_nfe.startswith("NFe"):
                  chave_nfe = chave_nfe[3:]

        n_nf = get_text(root, './/nfe:nNF')  
        serie = get_text(root, './/nfe:serie')
        nat_op = get_text(root, './/nfe:natOp')
        data_emissao = get_text(root, './/nfe:ide/nfe:dEmi')
        emitente = get_text(root, './/nfe:emit/nfe:xNome')
        cnpj_emitente = get_text(root, './/nfe:emit/nfe:CNPJ')
        valor_total = get_float(root, './/nfe:total/nfe:ICMSTot/nfe:vNF')

        itens = []
        for item in root.findall('.//nfe:det', ns):
            numero_item = item.attrib.get("nItem", "?")
            produto = get_text(item, './/nfe:prod/nfe:xProd')
            codigo_produto = get_text(item, './/nfe:prod/nfe:cProd')
            ncm = get_text(item, './/nfe:prod/nfe:NCM')
            cfop = get_text(item, './/nfe:prod/nfe:CFOP')
            unidade = get_text(item, './/nfe:prod/nfe:uCom')
            quantidade = get_float(item, './/nfe:prod/nfe:qCom')
            valor_unitario = get_float(item, './/nfe:prod/nfe:vUnCom')
            valor_item = get_float(item, './/nfe:prod/nfe:vProd')

            itens.append({
                "item": numero_item,
                "produto": produto,
                "codigo_produto": codigo_produto,
                "ncm": ncm,
                "cfop": cfop,
                "unidade": unidade,
                "quantidade": quantidade,
                "valor_unitario": valor_unitario,
                "valor_total": valor_item,
            })
        return {
            "arquivo": nome_arquivo,
            "chave_nfe": chave_nfe,
            "numero_nota": n_nf,
            "serie": serie,
            "data_emissao": data_emissao,
            "operacao": nat_op,
            "cnpj_emitente": cnpj_emitente,
            "emitente": emitente,
            "valor_total": valor_total,
            "itens": itens
        }
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_xml}' não foi encontrado.")
        return None
    except ET.ParseError:
        print(f"Erro: O arquivo '{caminho_xml}' não é um XML válido.")
        return None
    except ValueError as e:
        print(f"Erro ao converter valor para float: {e}")
        return None

# Ler a pasta 
def ler_pasta_xml(caminho_pasta):
    notas = []
    if not os.path.exists(caminho_pasta):
        print(f"Aviso: A pasta '{caminho_pasta}' não foi encontrada.")
        return notas
        
    for arquivo in os.listdir(caminho_pasta):
        if arquivo.endswith(".xml"):
             caminho_completo = os.path.join(caminho_pasta, arquivo)
             nota = ler_xml_nfe(caminho_completo)
             if nota is not None: 
                  notas.append(nota)
    return notas

# Excel
def exportar_excel(notas):
    linhas = []
    for nota in notas:
        for item in nota["itens"]:
            linhas.append({
                "Número Nota": nota["numero_nota"],
                "Emitente": nota["emitente"],
                "Operação": nota["operacao"],
                "Produto": item["produto"],
                "Quantidade": item["quantidade"],
                "Valor Unitário": item["valor_unitario"],
                "Valor Item": item["valor_total"],
                "Valor Total Nota": nota["valor_total"]
            })
   
    df = pd.DataFrame(linhas)

    # Garante que o arquivo seja salvo na mesma pasta onde este script está localizado
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    caminho_saida = os.path.join(diretorio_script, "notas_fiscais.xlsx")

    df.to_excel(caminho_saida, index=False)
    print(f"Arquivo Excel gerado com sucesso em: {caminho_saida}")

    # Abre o arquivo automaticamente dependendo do sistema operacional
    try:
        if sys.platform == "win32":
            os.startfile(caminho_saida)
        elif sys.platform == "darwin":  # macOS
            subprocess.run(["open", caminho_saida])
        else:  # Linux
            subprocess.run(["xdg-open", caminho_saida])
    except Exception as e:
        print(f"Não foi possível abrir o arquivo automaticamente: {e}")

# Programa
if __name__ == "__main__":
    # Garante que a pasta de XMLs também seja buscada a partir do local do script (caso queira)
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    pasta = os.path.join(diretorio_script, "xmls_teste")
    
    notas = ler_pasta_xml(pasta)
    print("=" * 60)
    print(f"Total de notas fiscais lidas: {len(notas)}")
    print("=" * 60)
    
    if len(notas) > 0:
        exportar_excel(notas)
    else:
        print("Nenhuma nota fiscal foi encontrada para exportar.")