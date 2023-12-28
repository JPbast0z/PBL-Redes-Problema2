<div align="center">
  <h1>
      Relatório do problema 2: ZapsZap
  </h1>

  <h3>
    João Pedro da Silva Bastos
  </h3>

  <p>
    Engenharia de Computação – Universidade Estadual de Feira de Santana (UEFS)
    Av. Transnordestina, s/n, Novo Horizonte
    Feira de Santana – BA, Brasil – 44036-900
  </p>

  <center>joaopedro.silvabastos.splash@gmail.com</center>

</div>

# 1. Introdução

Ao longo da evolução da humanidade os meios de comunicação tem se mostrado uma chave crucial para a colaboração e o bom convívio da sociedade. Cartas, telefonemas, e-mails, todos tiveram o seu auge, mas o meio de comunicação mais utilizado atualmente são os aplicativos de trocas de mensagens rápidas. 

Pensando nisso, foi proposto aos membros de uma startup que desenvolvessem um aplicativo de trocas de mensagens instantâneas baseado no modelo peer-to-peer (P2P). O software deve ser descentralizado, e permitir uma troca de mensagens seguras entre os membros do grupo da empresa. O programa deve ser implementado utilizando sockets UDP e garantir que as mensagens sejam exibidas igualmente para todos os membros do grupo.

A solução do problema se deu utilizando a linguagem de programação Python na versão 3.11 e algumas de suas bibliotecas padrões como Json, Socket, threading, uuid, OS e time. Para garantir a segurança das mensagens foi realizada uma criptografia baseada nos membros presentes no grupo e a para a troca de mensagens foi utilizada a arquitetura de rede UDP.

# 2. Metodologia

# 2.1. Threads

Threads são linhas de execução dentro de um processo maior em um programa de computador. Elas permitem que múltiplas partes do código funcionem simultaneamente, permitindo um uso mais eficiente de recursos e realizando operações mais eficientes. 
Neste programa foram utilizadas 3 threads:
- thread_receber: Responsável por receber todos os pacotes enviados por outros usuários
- thread_triagem: Responsável por realizar uma triagem dos pacotes recebidos (mensagens ou pacotes de sincronização)
- thread_sinc: Responsável por sincronizar o histórico de conversas a cada intervalo de tempo específico (atualmente está definido como 5 segundos, mas pode ser alterado em código)

# 2.2. Sincronização

Diante da necessidade de manter as mensagens atualizadas entre todos os usuários, implementou-se a sincronização como solução. Para isso, optou-se pelo uso do Relógio de Lamport, uma técnica proposta por Leslie Lamport para marcar eventos em sistemas distribuídos. Essa abordagem permite ordenar eventos em diferentes nós, mesmo em situações assíncronas.

Vale ressaltar que a classe do Relógio de Lamport utilizada no programa foi obtida da internet, visto que este algoritmo já existe e funciona de maneira eficiente, simplificando sua implementação e adaptação como um contador de mensagens.

O relógio de cada usuário é atualizado durante o envio ou recebimento de mensagens, garantindo a consistência entre todos os relógios. Ao iniciar o sistema, o relógio do usuário é ajustado com base nos relógios dos usuários "online".

Além do contador no relógio, é crucial realizar a sincronização das mensagens. Ao iniciar o programa, o usuário sincroniza seu relógio e solicita a sincronização das mensagens, requisitando todas as mensagens em posse de outros usuários. Esse processo é repetido em intervalos de cinco segundos por meio de uma das threads mencionadas, garantindo a atualização contínua das conversas entre os usuários.

Graças ao "id" único em todas as mensagens, mesmo com valores de relógio repetidos, as mensagens permanecem únicas, garantindo uma ordenação única e correta para todos os usuários.

# 2.3. Pacotes

Para garantir uma troca eficiente de pacotes, foram definidos cinco tipos distintos, divididos entre pacotes de mensagem e pacotes de sincronização.

Os pacotes de mensagem convencionais são enviados aos destinatários contendo os seguintes atributos:
- "time": valor marcado no relógio lógico no momento do envio da mensagem.
- "type": identifica o tipo de pacote enviado.
- "conteudo": o próprio conteúdo da mensagem.
- "remetente": o endereço de quem enviou a mensagem.
- "id": uma identificação única para diferenciar cada pacote.

Os pacotes de sincronização podem ser subdivididos em sincronização de relógio e sincronização de mensagens.

Existem dois tipos de pacotes para sincronização de relógio:
1. clockSync: solicita o contador atual do relógio dos outros usuários (contendo apenas o seu tipo e o endereço do solicitante).
2. updateClock: Envia o valor do seu relógio para um usuário que fez uma solicitação (contém o tipo e o valor atual do relógio). 

Os pacotes de sincronização de mensagens também têm dois tipos distintos, e funcionam de forma semelhante aos pacotes de sincronização de relógio:
1. sendMsgSync: Faz um pedido do histórico completo de mensagens de outros usuários (contendo apenas o tipo e o endereço do solicitante).
2. recvMsgSync: Envia as mensagens solicitadas para o usuário que fez o pedido (contendo o tipo e a mensagem).

# 2.4. Criptografia

A criptografia é essencial para garantir a segurança na troca de mensagens. Neste programa, utilizamos uma técnica baseada em cifras de substituição, na qual cada caractere ou bit é deslocado por um número fixo de posições durante os processos de cifragem e decifragem.

Especificamente, empregamos a função 'ord', que retorna o valor ASCII dos caracteres da mensagem. Esse valor é somado ao resto da divisão entre uma variável 'A' e uma variável 'B'. Em seguida, utilizamos a função 'chr' para converter o resultado dessa soma de volta para o caractere correspondente ao valor ASCII obtido.

Para assegurar a segurança da chave criptográfica, as variáveis 'A' e 'B' variam dinamicamente de acordo com os membros presentes no grupo. A variável 'A' representa a soma das 'portas' dos endereços de cada membro do grupo (exemplo: 123.0.0.3:1111 e 321.0.0.4:2222; a chave 'A' seria 4444), enquanto a variável 'B' é a soma dos caracteres dos endereços IP (ignorando a 'porta') dos membros do grupo (exemplo: 123.0.0.1 e 321.0.0.2; a chave 'B' seria 15).

Este processo é aplicado a cada caractere da mensagem individualmente, mas os resultados são concatenados para manter a integridade da mensagem completa. Para descriptografar, basta realizar o processo inverso, substituindo a soma pela subtração ao utilizar o valor obtido por 'ord' e o resto da divisão entre 'A' e 'B'.

# 3. Resultados 

A primeira ação que deve ser realizada ao iniciar o programa é selecionar em qual computador o usuário está, visto que a lista de membros de grupos presente no código está definida com endereços IP e portas para os computadores do laboratório (deve ser inserido um número entre 1 e 14, correspondente ao computador que está sendo utilizado). Para que o programa seja testado fora do laboratório, é preciso alterar as informações do dicionário que contém os membros do grupo (membros_grupo), adicionando o endereço IP e porta convenientes para o computador em que está sendo feito o uso. Vale ressaltar que em caso de testes onde o programa é executado várias vezes no mesmo computador, o endereço IP vai ser o mesmo para todos os usuários, porém deve ser utilizado uma porta diferente. O padrão em que os endereços estão sendo registrados é "IP:PORTA", exemplo: "123.0.0.1:1111".

Uma vez selecionado o computador, torna-se possível enviar mensagens para outros usuários online. Caso as mensagens sejam enviadas enquanto os destinatários estão offline, elas serão sincronizadas assim que os usuários iniciarem o programa, graças às funções de sincronização. Vale ressaltar que, em casos onde todos os usuários se desconectem, as mensagens serão perdidas, pois o programa não visa armazenamento não volátil.

Devido à sincronização a cada cinco segundos, e considerando que todos os usuários enviam suas mensagens, a perda de mensagens é rara. Mesmo se uma mensagem não chegar no envio padrão, ela será sincronizada a cada cinco segundos. Em um caso hipotético onde isso falhe, a mensagem não será perdida, pois o remetente e os destinatários ainda terão a mensagem. Esta será enviada aos outros usuários sempre que houver um pedido de sincronização.
Vale ressaltar que visando a portabilidade do programa ele também foi adicionado no docker. Podendo ser baixado via terminal utilizando o comando: "docker pull bast0z/pbl2_zapzap" e após ser baixado pode ser executado via docker com o comando: "docker run -it --network host bast0z/pbl2_zapzap".

# 4. Conclusão

Portanto, é possível notar que os objetivos propostos pelo problema foram alcançados com sucesso, empregando conceitos avançados tanto de concorrência quanto de conectividade. A construção do aplicativo de troca de mensagens via socket UDP, utilizando a arquitetura Peer to Peer, permitiu a sincronização eficiente e a organização criptografada das mensagens, garantindo a segurança das informações. Além disso, as mensagens são recuperadas de forma eficaz sempre que um usuário se reconecta. O Docker também foi implementado com êxito para assegurar maior portabilidade em diferentes sistemas.

Em futuras atualizações deste projeto, uma funcionalidade pode ser implementada para verificar quais usuários estão online e se todos eles receberam as mensagens antes de exibi-las, evitando qualquer inconveniente de mensagens não visualizadas por algum usuário, mesmo que por um breve período de tempo. Além disso, considerando a constante evolução das práticas de segurança, pode-se explorar a implementação de métodos de criptografia mais avançados, visto que o método atual é bastante simples.

# 4. Referências
