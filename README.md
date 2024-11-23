# FIAP - Faculdade de Informática e Administração Paulista

<p align="center">
<a href= "https://www.fiap.com.br/"><img src="assets/images/logo-fiap.png" alt="FIAP - Faculdade de Informática e Admnistração Paulista" border="0" width=40% height=40%></a>
</p>

<br>

# Energy-DOS - Energia Limpa

## 👨‍👩 Grupo

Grupo de número <b>24</b> formado pelos integrantes mencionados abaixo.

## 👨‍🎓 Integrantes: 
- <a href="https://www.linkedin.com/in/cirohenrique/">Ciro Henrique</a> ( <i>RM559040</i> )
- <a href="javascript:void(0)">Enyd Bentivoglio</a> ( <i>RM560234</i> )
- <a href="https://www.linkedin.com/in/marcofranzoi/">Marco Franzoi</a> ( <i>RM559468</i> )
- <a href="https://www.linkedin.com/in/rodrigo-mazuco-16749b37/">Rodrigo Mazuco</a> ( <i>RM559712</i> )

## 👩‍🏫 Professores:

### Tutor(a) 
- <a href="https://www.linkedin.com/in/lucas-gomes-moreira-15a8452a/">Lucas Gomes Moreira</a>

### Coordenador(a)
- <a href="https://www.linkedin.com/in/profandregodoi/">André Godoi</a>

## 📜 Descrição

<b>Referência</b>: https://on.fiap.com.br/mod/assign/view.php?id=445641

Essa versão possui funcionalidades que auxiliam na administração de energia limpa gerada.

Algumas informações sobre os módulos dessa versão:

- <strong>Módulo "Localização"</strong>: Permite que sejam cadastradas as localizações que deverão ser administradas, como por exemplo residências, hotéis, prédios comerciais, empresas, etc. Dessa forma, será possível administrar a energia limpa gerada em diferentes localizações conforme necessidade do usuário (<i>Computational Thinking with Python (CTWP)</i>).
- <strong>Módulo "Energia Limpa"</strong>: Permite que sejam visualizadas informações referentes à geração de energia limpa das localizações cadastradas. O usuário consegue visualizar relatórios e gráficos com informações como <i>logs</i> de data e quantidade de energia gerada, quantidade de energia gerada por mês e ano, saldo de energia versus a quantidade de energia consumida por mês e ano e saldo total de energia gerada versus a quantidade de energia consumida (<i>Computational Thinking with Python (CTWP)</i>).
- <strong>Módulo "Consumo de Energia"</strong>: Permite que sejam visualizadas informações referentes ao consumo de energia das localizações cadastradas. O usuário consegue visualizar relatórios e gráficos com informações como <i>logs</i> de data e quantidade de energia consumida e quantidade de energia consumida por mês e ano (<i>Computational Thinking with Python (CTWP)</i>).
- <strong>Módulo "Estatísticas de Consumo de Energia"</strong>: Permite que o relatório de estatísticas de consumo de energia seja executado (<i>Statistical Computing with R (SCR)</i>).
- <strong>Módulo "Sensores"</strong>: Permite que sejam cadastrados diferentes sensores com seus códigos de série e associados aos possíveis tipos "Sensor de Presença" e "Sensor de Luminosidade" (<i>Artificial Intelligence with Computer Systems and Sensors (AICSS)</i>).
- <strong>Módulo "Log de Execução de Sensores"</strong>: Permite que sejam visualizadas informações referentes à execução dos sensores. O usuário consegue visualizar relatórios e gráficos com informações como <i>logs</i> de quantidade de execuções e quantidade de energia consumida por dia, mês e ano (<i>Artificial Intelligence with Computer Systems and Sensors (AICSS)</i>).

## 📁 Estrutura de pastas

Dentre os arquivos e pastas presentes na raiz do projeto, definem-se:

1. <b>assets</b>: Diretório para armazenamento de arquivos complementares da estrutura do sistema.
    - Diretório "images": Diretório para armazenamento de imagens.

2. <b>config</b>: Diretório para armazenamento de arquivos em formato <i>json</i> contendo configurações.
    - Arquivo "db.json": Configurações destinadadas à conexão com banco de dados.
    - Arquivo "params.json": Configurações do sistema em geral.

3. <b>document</b>: Diretório para armazenamento de documentos relacionados ao sistema.
    - Diretório "AIC": <i>Pendente</i>

4. <b>scripts</b>: Diretório para armazenamento de scripts.
    - Diretório "CDS": Diretório para armazenamento de scripts relacionados às tabelas contendo dados de consumo de energia nos últimos anos (<i>Cognitive Data Science (CDS)</i>).
    - Diretório "oracle": Diretório para armazenamento de scripts do banco de dados Oracle.
    - Diretório "SCR": Diretório para armazenamento do relatório de consumo de energia (<i>Statistical Computing with R (SCR)</i>);
    - Diretório "sensors": Diretório para armazenamento dos conteúdos relacionados aos sensores do sistema conforme exemplificado na plataforma Wokwi.
        - Diretório "AICSS": <i>Pendente</i>

5. <b>src</b>: Diretório para armazenamento de código fonte do sistema em Python.
    - Diretório "custom": Diretório para armazenamento <i>classes/componentes</i> auxiliares do sistema.
    - Diretório "models": Diretório para armazenamento <i>classes/componentes</i> relacionados ao banco de dados.
    - Diretório "prompt": Diretório para armazenamento arquivos de inicialização do sistema em formato <i>prompt</i>.

6. <b>README.md</b>: Documentação do sistema em formato markdown.

## 🔧 Como executar o código

Como se trata de uma versão em formato <i>prompt</i>, para execução das funcionalidades, os seguintes passos devem ser seguidos:

1. Utilizando algum editor de código compatível com a linguagem de programação Python (<i>VsCode, PyCharm, etc.</i>), acesse o diretório "./src/prompt".
2. Neste diretório, basta abrir o arquivo "main.py" e executá-lo.

Para essa versão não são solicitados parâmetros para acesso como por exemplo <i>username</i>, <i>password</i>, <i>token access</i>, etc.

## 🗃 Histórico de lançamentos

* 1.0.0 - 25/11/2024

## 📋 Licença

Desenvolvido pelo Grupo 24 para o projeto da fase 4 (<i>Global Solution - 1º Semestre</i>) da <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://fiap.com.br">Fiap</a>. Está licenciado sobre <a href="http://creativecommons.org/licenses/by/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">Attribution 4.0 International</a>.</p>