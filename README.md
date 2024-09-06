<h1> Orthanc-PACS-Integration </h1>

<h2> Tecnologias utilizadas </h2>
<ol>
  <li> Docker.</li>
  <li> Bibliotecas Python:</li> 
  <ul> 
    <li> requests &#8594; Fazer a comunicação com o servidor por meio de solicitações HTTP.</li> 
    <li> zipfile &#8594; Ler arquivos <i>zip</i> sem precisar extraí-los.</li>
    <li> io &#8594; Ler os arquivos DICOM como <i>bytes</i>.</li>
    <li> torchxrayvision &#8594; Possibilitar a utilização de modelos pré-treinados de <i> Machine Learning</i>.</li>
    <li> pydicom &#8594; Realizar a leitura e escrita de arquivos DICOM.</li>
    <li> pathlib &#8594; Possibilitar a criação e a leitura de frases como caminhos no diretório.</li>
    <li> json &#8594; Criar e ler arquivos .json.</li>
    <li> re &#8594; Extrair informações de <i>strings</i> de maneira mais descomplicada.</li>
    <li> datetime &#8594; Mostrar informações sobre o dia e hora atuais para colocar no DICOM SR.</li>
  </ul>
</ol> 

<h2> ⚠️Problemas encontrados </h2>
<ol> 
  <li> A biblioteca <i>Torch</i> não estava sendo lida no meu <i>desktop</i>.</li>
  <li> Meu <i>desktop</i> pessoal está no limite das configurações necessárias para executar o Docker, então foi complicado conseguir encontrar uma versão que funcionava.</li>
  <li> O <i>upload</i> dos arquivos ao servidor não estava sendo persistido para outra inicialização.</li>
  <li> Apesar de ter conseguido usar o volume para persistir os dados, não estava conseguindo acessar os arquivos dentro desse volume com outra imagem.</li>
  <li> Ao carregar os arquivos .dcm no modelo, metade deles estava com o dobro da intensidade máxima suportada pela função de leitura xrv.utils.read_xray_dcm.</li>
  <li> Pouca informação sobre a criação de arquivos DICOM SR.</li>
  <li> Na criação do DICOM SR:</li>
   <p align=justify> <i>: UserWarning: Invalid value for VR UI: '72682317.56696215.32367375.69516389.09416010'. Please see "https://dicom.nema.org/medical/dicom/current/output/html/part05.html#table_6.2-1" for allowed values for each VR.</i> Não consegui descobrir o que ocasiona esse erro dado que a informação aponta ser devido ao VR UI estar inválido porém, no site indicado há a informação que essa sequÊncia deve ser de apenas números e pontos com até 64 caracteres, o que está sendo obedecido. </p>
</ol>
<h2> Conhecimentos adquiridos </h2>

<p align=justify> Com esse projeto, pude aprender a configurar contêiners, imagens e volumes no Docker, bem como entender os benefícios de se utilizar esse <i>software</i>, como:
  <li> Isolar um ambiente virtual com apenas as dependências necessárias e impedir a interferência de outras bibliotecas.</li>
  <li> Poupar armazenamento do computador usando o armazenamento em nuvem.</li>
 <p align=justify> Além disso, também consegui experenciar uma boa maneira de se usar modelos prontos de IA para ajudar no diagnóstico de pacientes por meio de arquivos .dcm; </p>
  
  <p align=justify>Outro ponto importante foi que aprendi como ler esses arquivos .dcm, assim como escrevê-los; </p>
  
  <p align=justify>Ademais, pude melhorar meu entendimento sobre servidores e sua comunicação via <i>API rest</i>; </p>
</p>

<h2> Primeira parte - Criação e execução de um servidor PACs OrthanC no Docker </h2>

<p align=justify> Nesta primeira etapa do projeto, mostrou-se necessário aprender como criar um servidor no Docker e como se dava a sua comunicação com PACs Orthanc. Após algumas pesquisas, consegui descobrir como esses fatos aconteciam e como configurar alguns elementos. O arquivo "orthanc.json" traz a configuração de um usuário qualquer com uma senha e acesso remoto autorizado para o servidor funcionando.</p>

<p align=justify> Para o bom funcionamento do servidor, é necessário seguir os seguintes passos:</p>
<li> Baixar o Docker e seguir todos o algoritmo de sua instalação;</li>

<li> Criar um arquivo docker-compose.yml e um orthanc.json em um único diretório de sua escolha para configurar o servidor e usuários, se necessário, respectivamente;</li>

<li> No terminal de comando do seu <i>desktop</i>, escrever a linha de código abaixo:</li>

```
docker-compose up -d
```
<p align=justify> A instrução acima é composta por 3 partes a primeira "docker-compose" se refere ao método para gerenciar os arquivos docker-compose.yml, a segunda "up" tem como objetivo criar e/ou inicializar o contêiner e a última "-d" é uma <i> flag </i> usada para executar o contêiner em segundo plano. </p>
<h2> Segunda parte - Adição de arquivos DICOM ao servidor usando Python. </h2>

<p align=justify>Para esta etapa do projeto, foi necessário escolher e coletar os <a href="https://drive.google.com/file/d/1Decc3rX_5oxF-4VvQxtWVqkV91O_Auf9/view">dados</a> que pudessem ser enviados ao servidor.</p>
<p align=justify> Em sequência, foi preciso descobrir como os arquivos são formatados, como o servidor recebe dados e qual era a melhor maneira de enviá-los.</p>
<p align=justify> Assim, cheguei às conclusões.</p>
<li> Arquivos DICOM são binários e devem ser lidos como <i>bytes</i> para garantir que sejam enviados corretamente.</li>
<li> <i>APIs rest</i>, como a do Orthanc, esperam que arquivos sejam transferidos como dados binários em um formulário HTTP.</li>
<li> Ler como <i>bytes</i> preserva a integridade do arquivo, evitando perdas e/ou alterações indesejadas.</li>

<p align=justify> E, por isso, o código foi estruturado para que fosse possível ler os arquivos direto da pasta <i>zip</i> e enviá-los de forma binária. Ele foi nomeado como enviar_arquivos.py e, para que funcione corretamente, basta executá-lo quando o servidor, ou o contêiner, estiver em operação.</p>

<h2> Terceira parte - Classificação dos dados usando um modelo pré-treinado de <i>Machine Learning</i> </h2>

<p align=justify> Para esta etapa, desenvolvi o código chamado de classificar.py. Esse programa coleta os arquivos do volume Docker, os lê como .dcm e usa o modelo "densenet121-res224-all" para diagnosticar o paciente e, então, montar um .json com o resultado obtido. Assim, observe que o arquivo docker-compose possui uma configuração de volume para a imagem a ser criada a seguir, usando o volume da imagem do servidor, tornando possível a utilização dessa memória.</p>

<p align=justify> Para que esse script funcione corretamente é necessário criar um arquivo Dockerfile com as bibliotecas e os arquivos necessários por ele. Além disso, é preciso criar uma imagem no Docker usando esse arquivo e depois executá-la com os seguintes comandos:</p>

```
docker build -t teste_xray_imagem .
```
<p align=justify>Comando para criar a imagem, usando "docker build" com o nome de "teste_xray_imagem". A <i>flag</i> "-t" se refere as <i>tags</i> e é usada para nomear imagens, enquanto "docker build" usa as configurações escritas no Dockerfile.</p>

```
docker run --rm -v docker_teste_orthanc_db:/var/lib/orthanc/db  teste_xray_imagem
```
<p align=justify> Nesse comando se pode observar a criação e inicialização de um conteiner com "docker run", a <i>flags</i> "--rm" e "-v" servindo para remover o contêiner após seu encerramento e especificar o volume criado no Docker (docker_teste_orthanc_db) e sua localização (/var/lib/orthanc/db), respectivamente.</p> 

<p align=justify> Ao final, o programa irá <i>printar</i> um dicionário no terminal e, para transformar esse dicionário em arquivo .json, usei o código abaixo. Por preferência, optei por fazer desse jeito manual visto que ainda não entendo completamente como salvar os arquivos da imagem diretamente no <i>desktop</i> local.</p>

```python
import json
dict = {dicionario_printado}
# Nome do arquivo JSON que será salvo
nome_do_arquivo = "resultados.json"

# Escrevendo os dados no arquivo JSON
with open(nome_do_arquivo, 'w') as arquivo_json:
    json.dump(dict, arquivo_json, indent=4)
```
  
<p align=justify> Obs: no código (classificar.py) há uma função para coletar esses arquivos por meio da <i>API rest</i> do servidor que foi o primeiro método que pensei para realizar essa tarefa, mas como era necessário baixar os arquivos novamente, acreditei ser mais conveniente encontrar uma forma de usar os arquivos do próprio volume. É por esse motivo que o docker-compose foi atualizado para construir uma <i>network</i> para ambas as imagens.</p>

<h2> Quarta parte - Criação de um arquivo DICOM SR <i> (Structured Report) </i> para cada arquivo DICOM </h2>

<p align=justify> Esta foi a parte mais difícil desse projeto por conta da falta de informação encontrada na internet sobre como criar arquivos DICOM SR. A parte de enviá-los para a devida pasta, que se refere aos respectivos laudos dos pacientes, não ocasionou problemas, uma vez que os servidores PACs não organizam seus arquivos pela estrutura hierárquica apresentada em seus nomes, mas sim pelo seus metadados, então bastou criar os documentos corretamente e enviá-los pela <i>API rest</i>.</p>

<p align=justify> Assim, desenvolvi o programa criar_dicomsr.py, que tem por finalidade criar os arquivos SR com todos os atributos essenciais, salvá-los em uma pasta que nomeei "SR" (também fiz o <i>upload</i> dessa pasta nesse repositório, caso seja de interesse verificá-la) e, por fim, mandá-los ao servidor Orthanc por meio de sua API. </p>

<p align=justify> Para o bom funcionamento desse código, se deve colocá-lo no diretório que foi salvo o resultados.json, uma vez que é por meio dele que todas as informações precisas são extraídas e executá-lo enquanto o servidor estiver operando.</p>
