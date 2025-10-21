import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns

print("Iniciando processo de consolidação e geração de gráficos...")

# 1. DEFINIR CAMINHOS
current_directory = os.getcwd()
results_folder = os.path.join(current_directory, 'results')

if not os.path.isdir(results_folder):
    print(f"Erro: A pasta '{results_folder}' não foi encontrada.")
    # Modificado para procurar na pasta 'locust-scripts' como discutimos
    print("Certifique-se de que este script está na pasta 'locust-scripts' (junto com a pasta 'results').")
    exit()

print(f"Lendo arquivos da pasta: {results_folder}")

# Lista para armazenar todos os dados
all_data = []

# 2. PADRÃO REGEX PARA O NOME DOS ARQUIVOS
# Ex: sc1_1inst_10usr.csv
file_pattern = re.compile(r'(sc\d)_(\d+)inst.*?_(\d+)usr\.csv')

# 3. LER E CONSOLIDAR OS DADOS
for filename in os.listdir(results_folder):
    if filename.endswith('.csv') and file_pattern.match(filename):
        match = file_pattern.match(filename)
        
        if match:
            # Extrair metadados do nome do arquivo
            cenario = match.group(1).replace('sc1', 'Cenário 1 (1MB)').replace('sc2', 'Cenário 2 (400KB)').replace('sc3', 'Cenário 3 (300KB)')
            instancias = int(match.group(2))
            usuarios = int(match.group(3))
            
            try:
                # Carregar o CSV
                df = pd.read_csv(os.path.join(results_folder, filename))
                
                # Encontrar a linha 'Aggregated' (baseado no seu CSV de exemplo)
                total_row = df[df['Name'] == 'Aggregated']
                
                if not total_row.empty:
                    # Extrair os dados da linha
                    rps = total_row['Requests/s'].values[0]
                    tempo_resposta = total_row['Average Response Time'].values[0]
                    
                    # Adicionar à lista
                    all_data.append({
                        'Cenario': cenario,
                        'Instancias': instancias,
                        'Usuarios': usuarios,
                        'RPS': rps,
                        'TempoResposta (ms)': tempo_resposta
                    })
                    print(f"Processado: {filename}")
                else:
                    print(f"Aviso: Linha 'Aggregated' não encontrada em {filename}")
                    
            except Exception as e:
                print(f"Erro ao processar o arquivo {filename}: {e}")

if not all_data:
    print("Nenhum dado foi coletado. Verifique se os arquivos CSV estão na pasta 'results'.")
    exit()

# 4. CRIAR O DATAFRAME CONSOLIDADO
df_consolidado = pd.DataFrame(all_data)
df_consolidado.to_csv("resultados_consolidados.csv", index=False)
print(f"\nDados consolidados salvos em 'resultados_consolidados.csv' com {len(df_consolidado)} linhas.")

# 5. GERAR OS GRÁFICOS
print("Gerando gráficos...")
sns.set_theme(style="whitegrid") # Define um estilo bonito

# --- MUDANÇA AQUI ---
# Define a sua paleta de cores personalizada em tons pastel
# (Azul, Laranja, Vermelho em tons suaves)
my_palette = ["#a6cee3", "#fdbf6f", "#fb9a99"]
# --------------------

# Gráfico 1: Tempo de Resposta vs. Usuários 
try:
    g1 = sns.catplot(
        data=df_consolidado,
        x='Usuarios',            # Eixo X: Número de usuários
        y='TempoResposta (ms)',  # Eixo Y: Tempo de resposta
        hue='Instancias',        # Agrupamento: 1, 2, ou 3 instâncias
        col='Cenario',           # Um gráfico para cada cenário
        kind='bar',
        palette=my_palette,      # <--- MUDANÇA AQUI
        height=5,
        aspect=1,
        legend_out=True
    )
    g1.fig.suptitle('Tempo de Resposta Médio vs. Número de Usuários', y=1.05)
    g1.set_axis_labels('Número de Usuários', 'Tempo de Resposta (ms)')
    g1.set_titles("{col_name}")
    g1._legend.set_title('Instâncias')
    
    plt.savefig("grafico_tempo_resposta.png", bbox_inches='tight')
    print("Gráfico 'grafico_tempo_resposta.png' salvo com sucesso.")
    plt.close()

except Exception as e:
    print(f"Erro ao gerar o Gráfico 1: {e}")

# Gráfico 2: RPS vs. Instâncias 
try:
    g2 = sns.catplot(
        data=df_consolidado,
        x='Instancias',          # Eixo X: Número de instâncias
        y='RPS',                 # Eixo Y: Requisições por segundo
        hue='Usuarios',          # Agrupamento: 10, 100, ou 1000 usuários
        col='Cenario',           # Um gráfico para cada cenário
        kind='bar',
        palette=my_palette,      # <--- MUDANÇA AQUI
        height=5,
        aspect=1,
        legend_out=True
    )
    g2.fig.suptitle('Requisições por Segundo (RPS) vs. Número de Instâncias', y=1.05)
    g2.set_axis_labels('Número de Instâncias', 'Requisições por Segundo (RPS)')
    g2.set_titles("{col_name}")
    g2._legend.set_title('Usuários')
    
    plt.savefig("grafico_rps.png", bbox_inches='tight')
    print("Gráfico 'grafico_rps.png' salvo com sucesso.")
    plt.close()

except Exception as e:
    print(f"Erro ao gerar o Gráfico 2: {e}")

print("\nProcesso concluído.")