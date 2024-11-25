FIAP - Global Solution 1º Semestre - FASE 4 - Statistical Computing with R (SCR) 


# Carregando bibliotecas necessárias
library(tidyverse)
library(stats)
library(ggplot2)
library(scales)
install.packages("gridExtra")
library(gridExtra)
install.packages("corrplot")
library(corrplot)
library(lubridate)

#Import 
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))
file_path <- file.path(getwd(), "SIGA-empreendimentos-geracao.csv")
siga_data <- read.csv(file_path, sep = ";", dec = ".", stringsAsFactors = FALSE, encoding = "UTF-8")

# Verificar os primeiros registros
head(siga_data)
names(siga_data)
colnames(siga_data)


# Verificar estrutura dos dados
str(siga_data)
print("Colunas disponíveis:")
print(names(siga_data))


# Convertendo os tipos de variáveis
siga_data <- siga_data %>%
  mutate(
    # Converter colunas numéricas armazenadas como texto
    MdaPotenciaOutorgadaKw = as.numeric(gsub(",", ".", MdaPotenciaOutorgadaKw)),
    MdaGarantiaFisicaKw = as.numeric(gsub(",", ".", MdaGarantiaFisicaKw)),
    
    # Converter colunas de coordenadas (latitude/longitude)
    NumCoordNEmpreendimento = as.numeric(gsub(",", ".", NumCoordNEmpreendimento)),
    NumCoordEEmpreendimento = as.numeric(gsub(",", ".", NumCoordEEmpreendimento)),
    
    # Converter colunas de data
    DatEntradaOperacao = as.Date(DatEntradaOperacao, format = "%Y-%m-%d"),
    DatInicioVigencia = as.Date(DatInicioVigencia, format = "%Y-%m-%d"),
    DatFimVigencia = as.Date(DatFimVigencia, format = "%Y-%m-%d")
  )

str(siga_data)


# ESTAT DESCRITIVA

# Estatísticas descritivas para potência fiscalizada
estatisticas <- siga_data %>%
  summarise(
    MediaPotencia = mean(MdaPotenciaFiscalizadaKw, na.rm = TRUE),
    MedianaPotencia = median(MdaPotenciaFiscalizadaKw, na.rm = TRUE),
    DesvioPadrao = sd(MdaPotenciaFiscalizadaKw, na.rm = TRUE),
    Q1 = quantile(MdaPotenciaFiscalizadaKw, 0.25, na.rm = TRUE),
    Q3 = quantile(MdaPotenciaFiscalizadaKw, 0.75, na.rm = TRUE)
  )

print(estatisticas)


# Agregar potência por tipo de geração
potencia_por_tipo <- siga_data %>%
  group_by(SigTipoGeracao) %>%
  summarise(TotalPotenciaFiscalizada = sum(MdaPotenciaFiscalizadaKw, na.rm = TRUE))

# Visualizar distribuição
print(potencia_por_tipo)

# Gráfico de barras 1
ggplot(potencia_por_tipo, aes(x = SigTipoGeracao, y = TotalPotenciaFiscalizada, fill = SigTipoGeracao)) +
  geom_bar(stat = "identity") +
  labs(title = "Distribuição de Potência Fiscalizada por Tipo de Geração",
       x = "Tipo de Geração", y = "Potência Fiscalizada (kW)") +
  theme_minimal()

potencia_por_tipo_ordenado <- potencia_por_tipo[order(potencia_por_tipo$TotalPotenciaFiscalizada), ]
print(potencia_por_tipo_ordenado)


# Agregar por ano de operação
evolucao_temporal <- siga_data %>%
  mutate(AnoOperacao = year(DatEntradaOperacao)) %>%
  group_by(AnoOperacao) %>%
  summarise(TotalPotenciaFiscalizada = sum(MdaPotenciaFiscalizadaKw, na.rm = TRUE))

print(evolucao_temporal)

# Gráfico de linha 2
ggplot(evolucao_temporal, aes(x = AnoOperacao, y = TotalPotenciaFiscalizada)) +
  geom_line(color = "blue") +
  labs(title = "Evolução da Potência Fiscalizada ao Longo do Tempo",
       x = "Ano de Operação", y = "Potência Fiscalizada (kW)") +
  theme_minimal()


# Gráfico boxplot para verificar outliers
ggplot(siga_data, aes(y = MdaPotenciaFiscalizadaKw)) +
  geom_boxplot(fill = "lightblue") +
  labs(title = "Distribuição de Potência Fiscalizada (kW)", y = "Potência Fiscalizada (kW)") +
  theme_minimal()

# Filtrar valores extremos (excluir acima de um limite, ex.: 99º percentil)
limite_superior <- quantile(siga_data$MdaPotenciaFiscalizadaKw, 0.99, na.rm = TRUE)

siga_data_filtrada <- siga_data %>%
  filter(MdaPotenciaFiscalizadaKw <= limite_superior)
#Estatísticas sem Outliers
estatisticas_filtradas <- siga_data_filtrada %>%
  summarise(
    MediaPotencia = mean(MdaPotenciaFiscalizadaKw, na.rm = TRUE),
    MedianaPotencia = median(MdaPotenciaFiscalizadaKw, na.rm = TRUE),
    DesvioPadrao = sd(MdaPotenciaFiscalizadaKw, na.rm = TRUE),
    Q1 = quantile(MdaPotenciaFiscalizadaKw, 0.25, na.rm = TRUE),
    Q3 = quantile(MdaPotenciaFiscalizadaKw, 0.75, na.rm = TRUE)
  )

print(estatisticas_filtradas)

# Criar categorias de potência
siga_data <- siga_data %>%
  mutate(CategoriaPotencia = cut(
    MdaPotenciaFiscalizadaKw,
    breaks = c(-Inf, 10, 100, 1000, 10000, Inf),
    labels = c("0-10 kW", "10-100 kW", "100-1.000 kW", "1.000-10.000 kW", ">10.000 kW")
  ))

# Contar registros por categoria
distribuicao_potencia <- siga_data %>%
  group_by(CategoriaPotencia) %>%
  summarise(Quantidade = n())

print(distribuicao_potencia)

# Gráfico de barras - 
ggplot(distribuicao_potencia, aes(x = CategoriaPotencia, y = Quantidade, fill = CategoriaPotencia)) +
  geom_bar(stat = "identity") +
  labs(title = "Distribuição de Potência Fiscalizada por Intervalos",
       x = "Intervalo de Potência", y = "Quantidade") +
  theme_minimal()


#### Filtrando valores muito baixos/0 na Potência gerada fiscalizada ####

options(encoding ="UTF-8")

# Filtrar removendo categoria 0-10 kW
siga_data_filtrado <- siga_data %>%
  filter(CategoriaPotencia != "0-10 kW")

# Recriar a análise com dados filtrados
distribuicao_potencia_filtrada <- siga_data_filtrado %>%
  group_by(CategoriaPotencia) %>%
  summarise(
    Quantidade = n(),
    PotenciaTotal = sum(MdaPotenciaFiscalizadaKw),
    PotenciaMedia = mean(MdaPotenciaFiscalizadaKw),
    PotenciaMediana = median(MdaPotenciaFiscalizadaKw)
  )

print(distribuicao_potencia_filtrada)

# Gráfico de barras - Distribuição de Potência Fiscalizada por Intervalos 3
ggplot(distribuicao_potencia_filtrada, aes(x = CategoriaPotencia, y = Quantidade, fill = CategoriaPotencia)) +
  geom_bar(stat = "identity") +
  labs(title = "Distribuição de Potência Fiscalizada por Intervalos",
       x = "Intervalo de Potência", y = "Quantidade") +
  theme_minimal()


#####################
# Corrigir encoding dos nomes
siga_data_filtrado$DscFonteCombustivel <- iconv(siga_data_filtrado$DscFonteCombustivel, 
                                                from = "latin1", 
                                                to = "UTF-8")

# Criar a análise novamente com nomes mais legíveis
analise_por_fonte <- siga_data_filtrado %>%
  group_by(DscFonteCombustivel) %>%
  summarise(
    Quantidade = n(),
    PotenciaTotal = sum(MdaPotenciaFiscalizadaKw),
    PotenciaMedia = mean(MdaPotenciaFiscalizadaKw)
  ) %>%
  arrange(desc(PotenciaTotal))

# Criar uma visualização mais informativa dos dados - Potência Total por Fonte de Energia 4
ggplot(analise_por_fonte, 
       aes(x = reorder(DscFonteCombustivel, -PotenciaTotal), 
           y = PotenciaTotal/1000000)) + # Convertendo para milhões
  geom_bar(stat = "identity", fill = "skyblue") +
  coord_flip() +
  labs(title = "Potência Total por Fonte de Energia",
       x = "Fonte de Energia",
       y = "Potência Total (MW)") +
  theme_minimal() +
  theme(
    axis.text.y = element_text(size = 10),
    plot.title = element_text(size = 14, face = "bold")
  )

# Análise adicional por tipo de fonte de energia
analise_por_fonte <- siga_data_filtrado %>%
  group_by(DscFonteCombustivel) %>%
  summarise(
    Quantidade = n(),
    PotenciaTotal = sum(MdaPotenciaFiscalizadaKw),
    PotenciaMedia = mean(MdaPotenciaFiscalizadaKw)
  ) %>%
  arrange(desc(PotenciaTotal))

print(analise_por_fonte)

######

# Visualização da distribuição por fonte
ggplot(siga_data_filtrado, aes(x = reorder(DscFonteCombustivel, MdaPotenciaFiscalizadaKw), 
                               y = MdaPotenciaFiscalizadaKw)) +
  geom_boxplot() +
  coord_flip() +
  labs(title = "Distribuição de Potência por Fonte de Energia",
       x = "Fonte de Energia",
       y = "Potência Fiscalizada (kW)") +
  theme_minimal()

######

# Melhorar a visualização com escala logarítmica para lidar com os outliers - Distribuição de Potência por Fonte de Energia 5
ggplot(siga_data_filtrado, aes(x = reorder(DscFonteCombustivel, MdaPotenciaFiscalizadaKw), 
                               y = MdaPotenciaFiscalizadaKw)) +
  geom_boxplot(fill = "lightblue", outlier.alpha = 0.5) +
  coord_flip() +
  scale_y_log10() +  # Escala logarítmica para melhor visualização
  labs(title = "Distribuição de Potência por Fonte de Energia",
       x = "Fonte de Energia",
       y = "Potência Fiscalizada (kW) - Escala Log") +
  theme_minimal() +
  theme(axis.text.y = element_text(size = 9))

# Análise específica das hidrelétricas
hidro_summary <- siga_data_filtrado %>%
  filter(DscFonteCombustivel == "Potencial hidráulico") %>%
  summarise(
    n = n(),
    media = mean(MdaPotenciaFiscalizadaKw),
    mediana = median(MdaPotenciaFiscalizadaKw),
    desvio_padrao = sd(MdaPotenciaFiscalizadaKw),
    min = min(MdaPotenciaFiscalizadaKw),
    max = max(MdaPotenciaFiscalizadaKw)
  )
print(hidro_summary)

# Filtrar apenas hidrelétricas
hidro_data <- siga_data_filtrado %>%
  filter(DscFonteCombustivel == "Potencial hidráulico")

# 1. Criar categorias de potência para hidrelétricas
hidro_data <- hidro_data %>%
  mutate(categoria_hidro = case_when(
    MdaPotenciaFiscalizadaKw <= 5000 ~ "CGH (até 5 MW)",
    MdaPotenciaFiscalizadaKw <= 30000 ~ "PCH (5-30 MW)",
    MdaPotenciaFiscalizadaKw <= 100000 ~ "Média (30-100 MW)",
    MdaPotenciaFiscalizadaKw <= 500000 ~ "Grande (100-500 MW)",
    TRUE ~ "UHE (>500 MW)"
  ))

print(hidro_data)

# 2. Análise estatística por categoria
analise_hidro <- hidro_data %>%
  group_by(categoria_hidro) %>%
  summarise(
    quantidade = n(),
    potencia_total = sum(MdaPotenciaFiscalizadaKw),
    potencia_media = mean(MdaPotenciaFiscalizadaKw),
    potencia_mediana = median(MdaPotenciaFiscalizadaKw)
  ) %>%
  mutate(
    percentual_quantidade = quantidade / sum(quantidade) * 100,
    percentual_potencia = potencia_total / sum(potencia_total) * 100
  )

print(analise_hidro)


# Distribuição de Potência por Categoria de Usina Hidrelétrica MW 6
ggplot(hidro_data, aes(x = categoria_hidro, y = MdaPotenciaFiscalizadaKw/1000)) +  # converter kW para MW
  geom_boxplot(fill = "lightblue") +
  scale_y_log10(
    labels = scales::label_number(big.mark = ".", decimal.mark = ","),
    breaks = c(0.1, 1, 10, 100, 1000, 10000)
  ) +
  labs(title = "Distribuição de Potência por Categoria de Usina Hidrelétrica",
       x = "Categoria",
       y = "Potência Fiscalizada (MW) - Escala Log") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Gráfico de barras Comparação: Quantidade de Usinas vs Potência Total 6.1
ggplot(analise_hidro) +
  geom_bar(aes(x = categoria_hidro, y = percentual_quantidade), 
           stat = "identity", fill = "lightblue", alpha = 0.7) +
  geom_line(aes(x = categoria_hidro, y = percentual_potencia, group = 1), 
            color = "red", size = 1) +
  geom_point(aes(x = categoria_hidro, y = percentual_potencia), 
             color = "red", size = 3) +
  labs(title = "Comparação: Quantidade de Usinas vs Potência Total",
       x = "Categoria",
       y = "Percentual (%)") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Imprimir a análise 
print(analise_hidro)
#########################

# Calcular estatísticas descritivas gerais
estatisticas_gerais <- siga_data_filtrado %>%
  summarise(
    Media = mean(MdaPotenciaFiscalizadaKw),
    Mediana = median(MdaPotenciaFiscalizadaKw),
    DesvioPadrao = sd(MdaPotenciaFiscalizadaKw),
    Q1 = quantile(MdaPotenciaFiscalizadaKw, 0.25),
    Q3 = quantile(MdaPotenciaFiscalizadaKw, 0.75),
    IQR = Q3 - Q1
  )
print(estatisticas_gerais)

##########################

#Exibindo colunas 
names(siga_data_filtrado)

# Análise básica por estado
analise_por_uf <- siga_data_filtrado %>%
  group_by(SigUFPrincipal) %>%
  summarise(
    quantidade_usinas = n(),
    potencia_total = sum(MdaPotenciaFiscalizadaKw),
    potencia_media = mean(MdaPotenciaFiscalizadaKw)
  ) %>%
  arrange(desc(potencia_total))

print(analise_por_uf)

# Gráfico de barras com quantidade de usinas por estado 7
ggplot(analise_por_uf, 
       aes(x = reorder(SigUFPrincipal, -quantidade_usinas), 
           y = quantidade_usinas)) +
  geom_bar(stat = "identity", fill = "skyblue") +
  labs(title = "Quantidade de Usinas por Estado",
       x = "Estado",
       y = "Número de Usinas") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))

# Gráfico de barras Potência Total Instalada por Estado 7.1
ggplot(analise_por_uf, 
       aes(x = reorder(SigUFPrincipal, -potencia_total), 
           y = potencia_total/1000000)) +  # Convertendo para GW
  geom_bar(stat = "identity", fill = "lightgreen") +
  labs(title = "Potência Total Instalada por Estado",
       x = "Estado",
       y = "Potência Total (GW)") +
  theme_minimal() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1))


# Comparação: Número de Usinas vs Potência Total por Estado 7.2
ggplot(analise_por_uf) +
  geom_bar(aes(x = reorder(SigUFPrincipal, -potencia_total), 
               y = quantidade_usinas), 
           stat = "identity", fill = "skyblue", alpha = 0.7) +
  geom_line(aes(x = reorder(SigUFPrincipal, -potencia_total), 
                y = potencia_total/max(potencia_total)*max(quantidade_usinas), 
                group = 1), 
            color = "red", size = 1) +
  scale_y_continuous(
    name = "Número de Usinas",
    sec.axis = sec_axis(
      ~.*max(analise_por_uf$potencia_total)/max(analise_por_uf$quantidade_usinas),
      name = "Potência Total (GW)",
      labels = function(x) format(x/1e6, big.mark = ".", decimal.mark = ",")
    )
  ) +
  labs(title = "Comparação: Número de Usinas vs Potência Total por Estado",
       x = "Estado") +
  theme_minimal() +
  theme(
    axis.text.x = element_text(angle = 45, hjust = 1),
    axis.title.y.right = element_text(color = "red"),
    axis.text.y.right = element_text(color = "red")
  )

# Análise adicional por tipo de fonte em cada estado
analise_fonte_uf <- siga_data_filtrado %>%
  group_by(SigUFPrincipal, DscFonteCombustivel) %>%
  summarise(
    quantidade = n(),
    potencia_total = sum(MdaPotenciaFiscalizadaKw)
  ) %>%
  ungroup()

print(analise_fonte_uf)



# Gráfico de barras empilhadas Distribuição de Potência por Fonte em cada Estado 7.3
ggplot(analise_fonte_uf, 
       aes(x = reorder(SigUFPrincipal, -potencia_total), 
           y = potencia_total/1000000, 
           fill = DscFonteCombustivel)) +
  geom_bar(stat = "identity") +
  labs(title = "Distribuição de Potência por Fonte em cada Estado",
       x = "Estado",
       y = "Potência Total (GW)",
       fill = "Fonte") +
  theme_grey() +
  theme(axis.text.x = element_text(angle = 45, hjust = 1),
        legend.position = "bottom")

# Imprimir resumo estatístico
print(analise_por_uf)
print(analise_por_uf, n=27)
##########################


