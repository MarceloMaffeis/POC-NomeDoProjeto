import streamlit as st
import ipaddress

# Configuração da página e aplicação de template visual
st.set_page_config(page_title="Calculadora de TI", page_icon="⚙️", layout="centered")

# CSS customizado injetado para padronização visual (botões em tom vermelho institucional)
st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #e3000f;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
    }
    div.stButton > button:hover {
        background-color: #cc0000;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚙️ Calculadora de TI")
st.markdown("Ferramenta prática para dimensionamento de redes e infraestrutura.")

# Organização da interface em abas para separar os escopos de cálculo
tab1, tab2 = st.tabs(["Transferência de Rede", "Sub-redes IPv4"])

# ABA 1: Cálculo de tempo de transferência de arquivos pela rede
with tab1:
    st.subheader("Tempo de Transferência de Arquivos")
    st.write("Estime o tempo necessário para mover dados com base na largura de banda.")
    
    col1, col2 = st.columns(2)
    with col1:
        tamanho = st.number_input("Tamanho do arquivo", min_value=0.1, value=1.0, step=0.5)
        unidade_tamanho = st.selectbox("Unidade", ["MB", "GB", "TB"])
    
    with col2:
        velocidade = st.number_input("Velocidade da rede (Mbps)", min_value=1.0, value=100.0, step=10.0)
        st.markdown("<br>", unsafe_allow_html=True) # Espaçamento
    
    if st.button("Calcular Tempo"):
        # Dicionário multiplicador para converter o tamanho selecionado em Megabits (Mbit)
        # 1 Byte = 8 bits. Portanto, 1 MB = 8 Mbits. 1 GB = 8192 Mbits.
        multiplicador = {"MB": 8, "GB": 8192, "TB": 8388608}
        tamanho_mbits = tamanho * multiplicador[unidade_tamanho]
        
        # O tempo em segundos é a quantidade total de bits dividida pela velocidade da rede
        segundos = tamanho_mbits / velocidade
        minutos = segundos / 60
        horas = minutos / 60
        
        # Exibição condicional dependendo do tempo resultante
        if horas > 1:
            st.success(f"Tempo estimado: **{horas:.2f} horas**.")
        elif minutos > 1:
            st.success(f"Tempo estimado: **{minutos:.2f} minutos**.")
        else:
            st.success(f"Tempo estimado: **{segundos:.0f} segundos**.")

# ABA 2: Análise de endereçamento IP e sub-redes
with tab2:
    st.subheader("Análise de Sub-rede")
    st.write("Validação e desmembramento de blocos CIDR.")
    
    ip_input = st.text_input("Endereço IP com máscara (ex: 192.168.1.0/24)", "192.168.1.0/24")
    
    if st.button("Analisar Rede"):
        try:
            # A biblioteca nativa ipaddress simplifica a validação e o cálculo de máscaras
            rede = ipaddress.IPv4Network(ip_input, strict=False)
            
            st.info(f"**Endereço da Rede:** {rede.network_address}")
            st.info(f"**Máscara de Sub-rede:** {rede.netmask}")
            # Subtrai 2 endereços (Rede e Broadcast) para encontrar os IPs disponíveis para hosts
            st.info(f"**Total de Hosts Úteis:** {rede.num_addresses - 2}")
            st.info(f"**Broadcast:** {rede.broadcast_address}")
        except ValueError:
            st.error("Formato de IP ou CIDR inválido. Verifique a sintaxe e tente novamente.")
