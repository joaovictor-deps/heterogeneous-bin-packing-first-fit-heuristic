import os
from operator import itemgetter

# Lê os dados de uma única instância e retorna uma lista de listas com as informações
# dos itens e a capacidade da mochila na instância
def le_dados_instancia(arq_instancia):
    with open(arq_instancia, "r", encoding="utf8") as f:
        linhas = f.readlines()
        # Lê a quantidade de itens e a capacidade
        v_linha = linhas[0].strip().split(";")
        qtd_caixas = int(v_linha[1])
        v_linha = linhas[1].strip().split(";")
        qtd_itens = int(v_linha[1])
        # Apaga os valores já lidos
        del linhas[:3]
        # Lê os dados de todos os itens
        
        dados_itens = list()
        dados_caixa = list()
        for i in range(qtd_caixas):
            v_linha = linhas[i].strip().split(";")
            id_caixa= int(v_linha[0])
            capacidade_caixa = int(v_linha[1])
            valor_caixa = int(v_linha[2])
            dados_caixa.append([id_caixa, capacidade_caixa, valor_caixa])
        del linhas[:qtd_caixas + 1]
        for i in range(qtd_itens):
            v_linha = linhas[i].strip().split(";")
            id_item = int(v_linha[0])
            peso_item = int(v_linha[1])
            dados_itens.append([id_item, peso_item])
    # Retorna os dados lidos
    return dados_caixa, dados_itens

def algoritmo(dados_caixa, dados_itens):
    
    solucao = list()
    linha = list()
    
    # Ordena as caixas por capacidade/valor
    dados_caixa.sort(key=lambda x: x[1]/x[2], reverse=True)
    
    # Ordena os itens pelo peso
    # Adicionei o reverse=True aqui na correção, agora as soluções estão muito melhores
    dados_itens.sort(key=itemgetter(1), reverse=True)
    
    for caixa in dados_caixa:
        capacidade_caixa = caixa[1]
        custo_caixa = caixa[2]
        
        capacidade_usada = 0
        itens_caixa = []
        
        for item in dados_itens:
            id_item = item[0]
            peso_item = item[1]
            
            if capacidade_usada + peso_item <= capacidade_caixa:
                capacidade_usada += peso_item
                itens_caixa.append(id_item)
        
        if itens_caixa:
            linha.append(caixa[0])
            linha.append(capacidade_usada)
            linha.append(capacidade_caixa)
            linha.append(custo_caixa)
            linha.append(';'.join(map(str, itens_caixa)))
            
            solucao.append(linha)
            linha = []
        
        # Remove os itens já alocados
        dados_itens = [item for item in dados_itens if item[0] not in itens_caixa]
    
    qtd_caixas = len(solucao)
    valor_total = sum([caixa[3] for caixa in solucao])

    return solucao, valor_total, qtd_caixas


# Salva uma solução em um arquivo CSV
def salva_solucao(arq_solucao, solucao, valor_total, qtd_caixas):
    with open(arq_solucao, "w+", encoding="utf8") as f:
        f.write(f"VALOR_TOTAL;{valor_total}\n")
        f.write(f"QTD_CAIXA;{qtd_caixas}\n")
        f.write("CAIXA;PESO;CAPACIDADE;VALOR;ITENS\n")
        for caixa in solucao:
            i = 0
            for item in caixa:
                if i < len(caixa)-1:
                    f.write(f"{item};")
                    i += 1
                else:
                    f.write(f"{item}\n")

# Este método lê resolve uma única instância do arquivo arq_instancia
# e salva a solução encontrada no arquivo arq_solucao
def resolve_instancia(arq_instancia, arq_solucao):
    dados_caixa, dados_itens = le_dados_instancia(arq_instancia)
    solucao, valor_total, qtd_caixas = algoritmo (dados_caixa, dados_itens)
    salva_solucao(arq_solucao, solucao, valor_total, qtd_caixas)

# Resolve todas as instâncias em uma pasta informada (pasta_instancias)
# e salva as soluções na pasta pasta_solucoes
def resolve_todas_instancias(pasta_instancias, pasta_solucoes):
    # Lista de arquivos de instância
    instancias = os.listdir(pasta_instancias)
    instancias.sort()
    # Processa todas as instâncias
    for instancia in instancias:
        arq_instancia = os.path.join(pasta_instancias, instancia)
        arq_solucao = os.path.join(pasta_solucoes, instancia)
        resolve_instancia(arq_instancia, arq_solucao)

def main():
    resolve_todas_instancias("Instancias", "Solucoes")

if __name__ == '__main__':
    main()
