import os
import random
from datetime import datetime, timedelta

# Create directory for test XMLs
output_dir = "xmls_teste"
os.makedirs(output_dir, exist_ok=True)

# Sample data pools for realistic variability
emitentes = [
    ("12345678000199", "Tech Solutions SP LTDA"),
    ("98765432000111", "Comercio de Eletronicos Paulista SA"),
    ("55443322000100", "Distribuidora de Suprimentos Campinas LTDA"),
    ("11223344000155", "Mega Informatica e Servicos EIRELI"),
]

clientes = [
    ("88776655000122", "Supermercado do Bairro LTDA"),
    ("33221100000144", "Escola e Faculdade Futuro SA"),
    ("99887766000133", "Hospital e Maternidade Central"),
    ("44556677000188", "Lojas de Departamentos Uniao"),
]

produtos_pool = [
    ("PROD001", "Notebook Core i5 16GB", "84713012", 3500.00),
    ("PROD002", "Monitor LED 24 Pulgadas", "85285120", 850.00),
    ("PROD003", "Teclado Mecanico USB", "84716052", 220.00),
    ("PROD004", "Mouse Optico Sem Fio", "84716053", 95.00),
    ("PROD005", "Cabo HDMI 2.0 2 Metros", "85444200", 35.00),
    ("PROD006", "Cadeira Ergonomica de Escritorio", "94013000", 1200.00),
    ("PROD007", "Impressora Multifuncional Laser", "84433111", 1850.00),
    ("PROD008", "SSD NVMe 1TB", "85235110", 480.00),
]

start_date = datetime(2026, 1, 1)

for i in range(1, 1001):
    n_nf = i
    cnpj_emit, nome_emit = random.choice(emitentes)
    cnpj_dest, nome_dest = random.choice(clientes)
    
    # Generate 1 to 4 random products per invoice
    num_items = random.randint(1, 4)
    selected_prods = random.sample(produtos_pool, num_items)
    
    items_xml = ""
    v_total_prod = 0.0
    
    for idx, (c_prod, x_prod, ncm, v_un) in enumerate(selected_prods, start=1):
        q_com = random.randint(1, 5)
        v_prod_item = q_com * v_un
        v_total_prod += v_prod_item
        
        items_xml += f"""
      <det nItem="{idx}">
        <prod>
          <cProd>{c_prod}</cProd>
          <xProd>{x_prod}</xProd>
          <NCM>{ncm}</NCM>
          <CFOP>5102</CFOP>
          <uCom>UN</uCom>
          <qCom>{q_com:.4f}</qCom>
          <vUnCom>{v_un:.2f}</vUnCom>
          <vProd>{v_prod_item:.2f}</vProd>
        </prod>
      </det>"""

    random_days = random.randint(0, 180)
    dh_emi = (start_date + timedelta(days=random_days)).strftime("%Y-%m-%dT%H:%M:%S-03:00")
    chave_access = f"35260{cnpj_emit}55001{str(n_nf).zfill(9)}100000000"

    xml_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<nfeProc xmlns="http://www.portalfiscal.inf.br/nfe" versao="4.00">
  <NFe>
    <infNFe Id="NFe{chave_access}" versao="4.00">
      <ide>
        <cUF>35</cUF>
        <cNF>{random.randint(10000000, 99999999)}</cNF>
        <natOp>VENDA DE MERCADORIA</natOp>
        <mod>55</mod>
        <serie>1</serie>
        <nNF>{n_nf}</nNF>
        <dhEmi>{dh_emi}</dhEmi>
        <tpNF>1</tpNF>
      </ide>
      <emit>
        <CNPJ>{cnpj_emit}</CNPJ>
        <xNome>{nome_emit}</xNome>
        <enderEmit>
          <xLgr>Avenida Paulista</xLgr>
          <nro>{random.randint(100, 3000)}</nro>
          <xBairro>Bela Vista</xBairro>
          <xMun>Sao Paulo</xMun>
          <UF>SP</UF>
        </enderEmit>
      </emit>
      <dest>
        <CNPJ>{cnpj_dest}</CNPJ>
        <xNome>{nome_dest}</xNome>
      </dest>{items_xml}
      <total>
        <ICMSTot>
          <vProd>{v_total_prod:.2f}</vProd>
          <vNF>{v_total_prod:.2f}</vNF>
        </ICMSTot>
      </total>
    </infNFe>
  </NFe>
</nfeProc>"""

    file_path = os.path.join(output_dir, f"nfe_{str(n_nf).zfill(4)}.xml")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(xml_content)

print(f"Sucesso: 1000 arquivos XML foram gerados na pasta '{output_dir}'.")

