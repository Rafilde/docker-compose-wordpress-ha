import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import seaborn as sns

print("Iniciando processo de consolidação e geração de gráficos...")

current_directory = os.getcwd()
results_folder = os.path.join(current_directory, 'results')

if not os.path.isdir(results_folder):
    print(f"Erro: A pasta '{results_folder}' não foi encontrada.")
    print("Certifique-se de que este script está na pasta 'locust-scripts' (junto com a pasta 'results').")
    exit()

print(f"Lendo arquivos da pasta: {results_folder}")

all_data = []


file_pattern = re.compile(r'(sc\d)_(\d+)inst.*?_(\d+)usr.*?\.csv')

for filename in os.listdir(results_folder):
    match = file_pattern.match(filename)
    
    if match:
        cenario = match.group(1).replace('sc1', 'Cenário 1 (1MB)').replace('sc2', 'Cenário 2 (400KB)').replace('sc3', 'Cenário 3 (300KB)')
        instancias = int(match.group(2))
        usuarios = int(match.group(3))
        
        try:
            df = pd.read_csv(os.path.join(results_folder, filename))
            

            total_row = df[df['Name'] == 'Aggregated']
            
            if not total_row.empty:

                rps = total_row['Requests/s'].values[0]
                tempo_resposta = total_row['Average Response Time'].values[0]
                

                failure_count = total_row['Failure Count'].values[0]
                request_count = total_row['Request Count'].values[0]
                avg_size = total_row['Average Content Size'].values[0]

                taxa_falha = 0.0
                if request_count > 0:
                    taxa_falha = (failure_count / request_count) * 100

                
                all_data.append({
                    'Cenario': cenario,
                    'Instancias': instancias,
                    'Usuarios': usuarios,
                    'RPS': rps,
                    'TempoResposta (ms)': tempo_resposta,
                    
                    'TaxaDeFalha (%)': taxa_falha,
                    'TamanhoResposta (bytes)': avg_size
                })
                print(f"Processado: {filename}")
            else:
                print(f"Aviso: Linha 'Aggregated' não encontrada em {filename}")
                
        except Exception as e:
            print(f"Erro ao processar o arquivo {filename}: {e}")

if not all_data:
    print("Nenhum dado foi coletado. Verifique se os arquivos CSV estão na pasta 'results'.")
    exit()

df_consolidado = pd.DataFrame(all_data)
df_consolidado.to_csv("resultados_consolidados.csv", index=False)
print(f"\nDados consolidados salvos em 'resultados_consolidados.csv' com {len(df_consolidado)} linhas.")


print("Gerando gráficos...")
sns.set_theme(style="whitegrid") 


my_palette = ["#a6cee3", "#fdbf6f", "#fb9a99"] 


try:
    g1 = sns.catplot(
        data=df_consolidado,
        x='Usuarios',
        y='TempoResposta (ms)', 
        hue='Instancias',
        col='Cenario',
        kind='bar',
        palette=my_palette,
        height=5,
        aspect=1,
        legend_out=True,
        sharey=False 
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


try:
    g2 = sns.catplot(
        data=df_consolidado,
        x='Usuarios', 
        y='TaxaDeFalha (%)', 
        hue='Instancias',
        col='Cenario',
        kind='bar',
        palette=my_palette,
        height=5,
        aspect=1,
        legend_out=True,
        sharey=False
    )
    g2.fig.suptitle('Taxa de Falha (%) vs. Número de Usuários', y=1.05)
    g2.set_axis_labels('Número de Usuários', 'Taxa de Falha (%)')
    g2.set_titles("{col_name}")
    g2._legend.set_title('Instâncias')
    
 
    g2.set(ylim=(0, None)) 
    
    plt.savefig("grafico_taxa_falha.png", bbox_inches='tight')
    print("Gráfico 'grafico_taxa_falha.png' salvo com sucesso.")
    plt.close()

except Exception as e:
    print(f"Erro ao gerar o Gráfico 2: {e}")


try:
    g3 = sns.catplot(
        data=df_consolidado,
        x='Usuarios', 
        y='TamanhoResposta (bytes)',
        hue='Instancias',
        col='Cenario',
        kind='bar',
        palette=my_palette,
        height=5,
        aspect=1,
        legend_out=True,
        sharey=False
    )
    g3.fig.suptitle('Tamanho Médio da Resposta vs. Número de Usuários', y=1.05)
    g3.set_axis_labels('Número de Usuários', 'Tamanho Médio (bytes)')
    g3.set_titles("{col_name}")
    g3._legend.set_title('Instâncias')
    
    plt.savefig("grafico_tamanho_resposta.png", bbox_inches='tight')
    print("Gráfico 'grafico_tamanho_resposta.png' salvo com sucesso.")
    plt.close()

except Exception as e:
    print(f"Erro ao gerar o Gráfico 3: {e}")

print("\nProcesso concluído.")