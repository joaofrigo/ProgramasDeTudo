# Caminho para o diretório de outputs
$HistoricoPath = "C:\historico\historico.txt"
$PrimeiraDescobertaPath = "C:\historico\primeira_descoberta.txt"
$DispositivosPath = "C:\historico\dispositivos.txt"

# Criar os diretórios se não existirem (evitar erros caso não existam)
$HistoricoDirectory = [System.IO.Path]::GetDirectoryName($HistoricoPath)
$PrimeiraDescobertaDirectory = [System.IO.Path]::GetDirectoryName($PrimeiraDescobertaPath)
if (-not (Test-Path $HistoricoDirectory)) {
    New-Item -ItemType Directory -Force -Path $HistoricoDirectory
}
if (-not (Test-Path $PrimeiraDescobertaDirectory)) {
    New-Item -ItemType Directory -Force -Path $PrimeiraDescobertaDirectory
}

# lista de endereços MAC já registrados
$EnderecosMACRegistrados = @()

# Executar arp para obter mapeamento entre IP e MAC
$arpResult = arp -a

# função para processar o resultado do arp
function Get-ArpInfo($arpResult) {
    foreach ($linha in $arpResult) {
        # Procura por linhas contendo IP e MAC. A lógica é criar uma lógica igual a IPS/MACS e comparar se encontra números
        # que sigam a mesma lógica desse match. Cada caractere e sua lógica:
        #\s+: um ou mais caracteres de espaço em branco.
        #(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}): um padrão de endereço IP IPv4, onde \d representa dígitos e {1,3} indica que pode haver de 1 a 3 dígitos em cada parte do endereço (por exemplo, 192.168.1.1).
        #\s+: Mais espaços em branco.
        #(\S{17}): Corresponde a 17 caracteres não brancos consecutivos, que é o padrão MAC. O \S representa qualquer caractere que não seja um espaço em branco.
        if ($linha -match "\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\S{17})") {
            $ip = $matches[1]
            $mac = $matches[2]

            # verifica se o endereço MAC já está no histórico
            if (-not $EnderecosMACRegistrados.Contains($mac)) {
                # Obtém o horário da primeira descoberta
                $horarioPrimeiraDescoberta = Get-Content $PrimeiraDescobertaPath -ErrorAction SilentlyContinue | Where-Object {$_ -match "IP: $ip"} | ForEach-Object {$_ -replace 'IP:.*?, Data e Hora: ', ''}

                # Se não encontrou o horário, é a primeira descoberta
                if (-not $horarioPrimeiraDescoberta) {
                    $horarioPrimeiraDescoberta = Get-Date
                    Add-Content -Path $PrimeiraDescobertaPath -Value "IP: $ip, Data e Hora: $horarioPrimeiraDescoberta"
                }

                # adiciona ao histórico
                Add-Content -Path $HistoricoPath -Value "IP: $ip, MAC: $mac"
                
                # Adiciona o endereço MAC à lista de registrados
                $EnderecosMACRegistrados += $mac
                
                # Exibe IP e MAC
                Write-Host "IP: $ip, MAC: $mac"

                # Verifica se o dispositivo está online. O ip é adquirido anteriormente e se verifica se esse IP responde aos
                # 2 pacotes lançados para ele
                $online = Test-Connection -ComputerName $ip -Count 2 -Quiet

                # Adiciona ao arquivo de dispositivos
                if ($ip -notin @('224.0.0.252', '239.255.255.250', '224.0.0.0', '224.0.1.0', '224.0.0.1', '224.0.0.22')) {
                    # em multicasts, o serviço macvendors não funciona neles. Não achei outra maneira de verificar 
                    # dinamicamente outros multicasts, então generalizei IPS comuns de multicast para a verificação razoavalmente precisa
                    try {
                        # Tenta obter informações do fabricante usando o serviço online (precisa de internet) "macvendors.com"
                        # não acha informações de dispositivo de multicast porém, além de não acertar sempre.
                        $fabricante = Invoke-RestMethod -Uri "https://api.macvendors.com/$mac" -Method Get -ErrorAction Stop
                    } catch {
                        # Em caso de erro, é inserida uma string mostrando que o fabricante não foi encontrado
                        $fabricante = "Fabricante não encontrado"
                    }

                    # adiciona informações ao arquivo de dispositivos
                    Add-Content -Path $DispositivosPath -Value "IP: $ip, MAC: $mac, Online: $online, Fabricante: $fabricante"
                } else {
                    # adiciona informações ao arquivo de dispositivos, mostrando que é um endereço de multicast
                    Add-Content -Path $DispositivosPath -Value "IP: $ip, MAC: $mac, Tipo: Multicast"
                }
            }
        }
    }
}

# processar o resultado do arp
Get-ArpInfo -arpResult $arpResult

# adicionar uma barra de separação no final da execução nos arquivos de histórico e dispositivos para melhorar visiblidade
Add-Content -Path $HistoricoPath -Value "_____________"
Add-Content -Path $DispositivosPath -Value "_____________"


# Não consegui implementar a parte da diferenciação de roteador e hosts no código. Se precisar de um teste ao vivo
# (jã que não consegui ir na aula de demonstração do código), posso gravar um vídeo e lhe mandar. Mas o código deve funcionar
# Em qualquer dispositivo sem problemas, afinal, só uso a internet e o powershell para isso, então pode ver em ação pessoalmente.