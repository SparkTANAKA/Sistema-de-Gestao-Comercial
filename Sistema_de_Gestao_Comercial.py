import json
import os




PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_DADOS = os.path.join(PASTA_PROJETO, "dados_comerciais.json")


def carregar_dados():
    """Carrega os dados salvos, ou inicia estruturas vazias."""
    print("Procurando arquivo em:", os.path.abspath(ARQUIVO_DADOS))
    if os.path.exists(ARQUIVO_DADOS):
        try:
            with open(ARQUIVO_DADOS, "r", encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
                return dados.get("clientes", {}), dados.get("produtos", {}), dados.get("vendas", [])
        except (json.JSONDecodeError, OSError):
            print("Aviso: não foi possível ler o arquivo de dados. Iniciando vazio.")
    return {}, {}, []


def salvar_dados(clientes, produtos, vendas):
    """Salva clientes, produtos e vendas em um arquivo JSON."""
    dados = {"clientes": clientes, "produtos": produtos, "vendas": vendas}
    try:
        with open(ARQUIVO_DADOS, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)
    except OSError:
        print("Erro: não foi possível salvar os dados.")


def ordenar_produtos(produtos, criterio):
    """Ordena os produtos manualmente pelo nome ou preço usando Bubble Sort."""
    lista_produtos = list(produtos.items())

    for i in range(len(lista_produtos)):
        for j in range(0, len(lista_produtos) - i - 1):
            if criterio == "nome":
                valor_atual = lista_produtos[j][1]["nome"].casefold()
                proximo_valor = lista_produtos[j + 1][1]["nome"].casefold()
            else:
                valor_atual = lista_produtos[j][1]["preço"]
                proximo_valor = lista_produtos[j + 1][1]["preço"]

            if valor_atual > proximo_valor:
                lista_produtos[j], lista_produtos[j + 1] = lista_produtos[j + 1], lista_produtos[j]

    return lista_produtos


def exibir_relatorio_vendas(vendas):
    """Mostra faturamento, quantidade, média, maior e menor venda."""
    print("\n--- Relatório de Faturamento ---")
    if not vendas:
        print("Nenhum faturamento registrado até o momento.")
        return
    faturamento_total = sum(v["total"] for v in vendas)
    quantidade_vendas = len(vendas)
    ticket_medio = faturamento_total / quantidade_vendas
    maior_venda = max(vendas, key=lambda v: v["total"])
    menor_venda = min(vendas, key=lambda v: v["total"])
    print(f"Faturamento total acumulado: R$ {faturamento_total:.2f}")
    print(f"Total de vendas realizadas: {quantidade_vendas}")
    print(f"Ticket médio por venda: R$ {ticket_medio:.2f}")
    print(f"Maior venda: R$ {maior_venda['total']:.2f} (Venda #{maior_venda['codigo']})")
    print(f"Menor venda: R$ {menor_venda['total']:.2f} (Venda #{menor_venda['codigo']})")


def exibir_menu():
    print("\n=========================================")
    print("         Sistema de Gestão Comercial     ")
    print("=========================================")
    print("1 - Cadastrar cliente")
    print("2 - Lista de clientes")
    print("3 - Consultar cliente")
    print("4 - Cadastrar produto")
    print("5 - Lista de produtos")
    print("6 - Consultar produto")
    print("7 - Registrar nova venda")
    print("8 - Consultar venda por código")
    print("9 - Consultar histórico de vendas")
    print("10 - Ordenar produtos por nome ou preço")
    print("0 - Relatório de faturamento")
    print("ENTER - Sair")

def main():
    clientes, produtos, vendas = carregar_dados()
    
    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            print("\n--- Cadastro de Cliente ---")
            doc_entrada = input("Digite o CPF ou CNPJ: ").strip()
            documento = doc_entrada.replace(".", "").replace("-", "").replace("/", "")
            
            if not documento.isdigit() or len(documento) not in [11, 14]:
                print("O documento deve conter apenas números, 11 para CPF ou 14 para CNPJ).")
            elif documento in clientes:
                print("Este CPF/CNPJ já está cadastrado.")
            else:
                tipo_doc = "CPF" if len(documento) == 11 else "CNPJ"
                
                nome = input("Digite o nome/razão social do cliente: ").strip()

                inscricao_estadual = ""
                if tipo_doc == "CNPJ":
                    while True:
                        ie_entrada = input("Inscrição Estadual: ").strip()
                        ie_tratado = ie_entrada.replace(".", "").replace("-", "")
                        if ie_tratado.isdigit() and 8 <= len(ie_tratado) <= 11:
                            inscricao_estadual = ie_tratado
                            break
                        print("A Inscrição Estadual deve conter apenas números de 8 a 11 dígitos.")
                
                while True:
                    tel_entrada = input("Telefone: ").strip()
                    telefone = tel_entrada.replace(".", "").replace("-", "").replace(" ", "")
                    if telefone.isdigit():
                        break
                    print("O telefone deve conter apenas dígitos numéricos.")
                
                while True:
                    endereço = input("Endereço: ").strip()
                    if endereço.replace(" ", "").isalpha():
                        break
                    print("O endereço deve conter apenas letras.")

                while True:
                    num_entrada = input("Número da residência: ").strip()
                    número = num_entrada.replace(".", "").replace("-", "").replace(" ", "")
                    if número.isdigit():
                        break
                    print("O número deve conter apenas dígitos numéricos.")

                while True:
                    bairro = input("Bairro: ").strip()
                    if bairro.replace(" ", "").isalpha():
                        break
                    print("O bairro deve conter apenas letras.")

                complemento = input("Complemento: ").strip()
                
                clientes[documento] = {
                    "tipo": tipo_doc,
                    "nome": nome, 
                    "telefone": telefone, 
                    "inscricao_estadual": inscricao_estadual,
                    "endereço": endereço, 
                    "número": número, 
                    "bairro": bairro, 
                    "complemento": complemento
                }
                print(f"{tipo_doc} cadastrado com sucesso!")
                salvar_dados(clientes, produtos, vendas)
            
            input("\nPressione ENTER para voltar ao menu principal...")

        elif opcao == "2":
            print("\n--- Lista de Clientes ---")
            if not clientes:
                print("Nenhum cliente cadastrado até o momento.")
            else:
                for doc, cli in clientes.items():
                    print(f"Documento: {doc} | Tipo: {cli['tipo']} | Nome: {cli['nome']} | Telefone: {cli['telefone']}")
            
            input("\nPressione ENTER para voltar ao menu principal...")

        elif opcao == "3":
            print("\n--- Consultar e Alterar Cliente ---")
            doc_entrada = input("Digite o CPF ou CNPJ do cliente: ").strip()
            documento = doc_entrada.replace(".", "").replace("-", "").replace("/", "")
            
            cliente = clientes.get(documento)
            if cliente:
                print(f"\nCliente encontrado:")
                print(f"Tipo: {cliente['tipo']} | Documento: {documento}")
                print(f"Nome: {cliente['nome']}")
                print(f"Telefone: {cliente['telefone']}")
                if cliente['tipo'] == "CNPJ":
                    print(f"Inscrição Estadual: {cliente['inscricao_estadual']}")
                print(f"Endereço: {cliente['endereço']}, Nº {cliente['número']} - Bairro: {cliente['bairro']} (Complemento: {cliente['complemento']})")
                
                alterar = input("\nDeseja alterar as informações deste cliente? (1-Sim / 2-Não): ").strip()
                if alterar == "1":
                    novo_nome = input(f"Novo nome (atual: {cliente['nome']}): ").strip()
                    if novo_nome:
                        cliente['nome'] = novo_nome
                    
                    if cliente['tipo'] == "CNPJ":
                        nova_ie = input(f"Nova Inscrição Estadual (atual: {cliente['inscricao_estadual']}): ").strip().replace(".", "").replace("-", "")
                        if nova_ie:
                            if nova_ie.isdigit() and 8 <= len(nova_ie) <= 11:
                                cliente['inscricao_estadual'] = nova_ie
                            else:
                                print("Inscrição Estadual inválida. Mantida a anterior.")

                    novo_tel = input(f"Novo telefone (atual: {cliente['telefone']}): ").strip().replace(".", "").replace("-", "").replace(" ", "")
                    if novo_tel:
                        if novo_tel.isdigit():
                            cliente['telefone'] = novo_tel
                        else:
                            print("Telefone inválido. Mantido o anterior.")

                    novo_end = input(f"Novo endereço (atual: {cliente['endereço']}): ").strip()
                    if novo_end:
                        if novo_end.replace(" ", "").isalpha():
                            cliente['endereço'] = novo_end
                        else:
                            print("Endereço inválido. Mantido o anterior.")

                    novo_num = input(f"Novo número (atual: {cliente['número']}): ").strip().replace(".", "").replace("-", "").replace(" ", "")
                    if novo_num:
                        if novo_num.isdigit():
                            cliente['número'] = novo_num
                        else:
                            print("Número inválido. Mantido o anterior.")

                    novo_bairro = input(f"Novo bairro (atual: {cliente['bairro']}): ").strip()
                    if novo_bairro:
                        if novo_bairro.replace(" ", "").isalpha():
                            cliente['bairro'] = novo_bairro
                        else:
                            print("Bairro inválido. Mantido o anterior.")

                    novo_comp = input(f"Novo complemento (atual: {cliente['complemento']}): ").strip()
                    if novo_comp:
                        cliente['complemento'] = novo_comp

                    print("Informações do cliente atualizadas com sucesso!")
                    salvar_dados(clientes, produtos, vendas)
            else:
                print("Cliente não encontrado.")
            
            input("\nPressione ENTER para voltar ao menu principal...")

        elif opcao == "4":
            print("\n--- Cadastro de Produto ---")
            codigo = input("Código do produto: ").strip()
            if codigo in produtos:
                print("Código de produto já cadastrado.")
            else:
                try:
                    nome = input("Nome do produto: ").strip()
                    
                    entrada_preço = input("Preço unitário (R$): ").strip()
                    preço_tratado = entrada_preço.replace("R$", "").replace(".", "").replace(",", ".")
                    preço = float(preço_tratado)
                    
                    estoq_str = input("Quantidade em estoque: ").strip()
                    estoque = int(estoq_str)
                    
                    produtos[codigo] = {"nome": nome, "preço": preço, "estoque": estoque}
                    print("Produto cadastrado com sucesso!")
                    salvar_dados(clientes, produtos, vendas)
                except ValueError:
                    print("Erro ao cadastrar produto. Certifique-se de digitar valores válidos.")
            
            input("\nPressione ENTER para voltar ao menu principal...")

        elif opcao == "5":
            print("\n--- Lista de Produtos ---")
            if not produtos:
                print("Nenhum produto cadastrado até o momento.")
            else:
                for cod, prod in produtos.items():
                    print(f"Código: {cod} | Nome: {prod['nome']} | Preço: R$ {prod['preço']:.2f} | Estoque: {prod['estoque']}")
            
            input("\nPressione ENTER para voltar ao menu principal...")

        elif opcao == "6":
            print("\n--- Consultar e Alterar Produto ---")
            codigo = input("Digite o código do produto: ").strip()
            produto = produtos.get(codigo)
            
            if produto:
                print(f"\nProduto encontrado:")
                print(f"Nome: {produto['nome']} | Preço: R$ {produto['preço']:.2f} | Estoque: {produto['estoque']}")
                
                alterar = input("\nDeseja alterar o nome ou o valor deste produto? (1-Sim / 2-Não): ").strip()
                if alterar == "1":
                    novo_nome = input(f"Novo nome (atual: {produto['nome']}): ").strip()
                    if novo_nome:
                        produto['nome'] = novo_nome
                    
                    try:
                        entrada_novo_preco = input(f"Novo preço (atual: R$ {produto['preço']:.2f}): ").strip()
                        if entrada_novo_preco:
                            preco_tratado = entrada_novo_preco.replace("R$", "").replace(".", "").replace(",", ".")
                            produto['preço'] = float(preco_tratado)
                        print("Produto atualizado com sucesso!")
                        salvar_dados(clientes, produtos, vendas)
                    except ValueError:
                        print("Erro: O preço informado é inválido. A alteração do preço não foi aplicada.")
            else:
                print("Produto não encontrado.")
            
            input("\nPressione ENTER para voltar ao menu principal...")

        elif opcao == "7":
            print("\n--- Registrar Nova Venda ---")
            if not clientes or not produtos:
                print("É necessário cadastrar clientes e produtos antes de registrar uma venda.")
            else:
                doc_cli = input("CPF ou CNPJ do cliente: ").strip()
                doc_cliente = doc_cli.replace(".", "").replace("-", "").replace("/", "")
                
                if doc_cliente not in clientes:
                    print("Cliente não encontrado.")
                else:
                    carrinho = []
                    total_venda = 0.0
                    
                    while True:
                        cod_prod = input("\nCódigo do produto (ou digite 0 para finalizar/cancelar): ").strip()
                        if cod_prod == "0" or cod_prod == "":
                            break
                            
                        if cod_prod not in produtos:
                            print("Produto não encontrado.")
                            continue
                            
                        produto_atual = produtos[cod_prod]
                        print(f"Produto: {produto_atual['nome']} | Disponível em estoque: {produto_atual['estoque']}")
                        
                        try:
                            qtd_str = input("Quantidade desejada: ").strip()
                            qtd = int(qtd_str)
                            
                            if qtd <= 0:
                                print("A quantidade deve ser maior que zero.")
                                continue
                                
                            if qtd > produto_atual["estoque"]:
                                print(f"Estoque insuficiente! Disponível: {produto_atual['estoque']}")
                                continue
                                
                            produto_atual["estoque"] -= qtd
                            subtotal = qtd * produto_atual["preço"]
                            total_venda += subtotal
                            
                            carrinho.append({
                                "codigo_produto": cod_prod,
                                "produto": produto_atual['nome'],
                                "quantidade": qtd,
                                "subtotal": subtotal
                            })
                            print(f"Adicionado ao carrinho! Subtotal deste item: R$ {subtotal:.2f}")
                            
                            continuar = input("Deseja adicionar mais produtos? (1-Sim / 2-Não): ").strip()
                            if continuar != "1":
                                break
                                
                        except ValueError:
                            print("quantidade inválida.")
                    
                    if carrinho:
                        codigo_venda = str(len(vendas) + 1)
                        venda = {
                            "codigo": codigo_venda,
                            "cliente": clientes[doc_cliente]['nome'],
                            "itens": carrinho,
                            "total": total_venda
                        }
                        vendas.append(venda)
                        salvar_dados(clientes, produtos, vendas)
                        print(f"\nVenda #{codigo_venda} registrada com sucesso! Total geral: R$ {total_venda:.2f}")
                    else:
                        print("Aviso: Venda cancelada ou nenhum produto foi adicionado.")
            
            input("\nPressione ENTER para voltar ao menu principal...")

        elif opcao == "8":
            print("\n--- Consultar Venda por Código ---")
            cod_venda = input("Digite o código da venda: ").strip()
            venda_encontrada = None
            for v in vendas:
                if v['codigo'] == cod_venda:
                    venda_encontrada = v
                    break
            
            if venda_encontrada:
                print(f"Venda #{venda_encontrada['codigo']} | Cliente: {venda_encontrada['cliente']} | Total Geral: R$ {venda_encontrada['total']:.2f}")
                print("   Itens da Venda:")
                for item in venda_encontrada['itens']:
                    print(f"   - {item['produto']} | Qtd: {item['quantidade']} | Subtotal: R$ {item['subtotal']:.2f}")
            else:
                print("Venda não encontrada.")
            
            input("\nPressione ENTER para voltar ao menu principal...")

        elif opcao == "9":
            print("\n--- Histórico de Vendas ---")
            if not vendas:
                print("Nenhuma venda registrada até o momento.")
            else:
                for v in vendas:
                    print(f"\nVenda #{v['codigo']} | Cliente: {v['cliente']} | Total Geral: R$ {v['total']:.2f}")
                    print("   Itens da Venda:")
                    for item in v['itens']:
                        print(f"   - {item['produto']} | Qtd: {item['quantidade']} | Subtotal: R$ {item['subtotal']:.2f}")
            
            input("\nPressione ENTER para voltar ao menu principal...")

        elif opcao == "0":
            print("\n--- Relatório de Faturamento ---")
            if not vendas:
                print("Nenhum faturamento registrado até o momento.")
            else:
                exibir_relatorio_vendas(vendas)
            
            input("\nPressione ENTER para voltar ao menu principal...")

        elif opcao == "10":
            if not produtos:
                print("Nenhum produto cadastrado até o momento.")
            else:
                print("\n1 - Ordenar por nome\n2 - Ordenar por preço")
                criterio = input("Escolha uma opção: ").strip()
                if criterio == "1":
                    lista_ordenada = ordenar_produtos(produtos, "nome")
                elif criterio == "2":
                    lista_ordenada = ordenar_produtos(produtos, "preço")
                else:
                    print("Opção inválida!")
                    lista_ordenada = []
                for cod, prod in lista_ordenada:
                    print(f"Código: {cod} | Nome: {prod['nome']} | Preço: R$ {prod['preço']:.2f} | Estoque: {prod['estoque']}")

        elif opcao == "":
            salvar_dados(clientes, produtos, vendas)
            print("\nSaindo do programa. Dados salvos.")
            break
        else:
            print("Opção inválida!")
            input("\nPressione ENTER para voltar ao menu principal...")

if __name__ == "__main__":
    main()