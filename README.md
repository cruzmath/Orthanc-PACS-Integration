<h1> Orthanc-PACS-Integration </h1>

<h2> Tecnologias utilizadas </h2>
<ol>
  <li> Docker.</li>
  <li> Bibliotecas Python:</li> 
  <ul> 
    <li> requests &#8594; Fazer a comunicação com o servidor por meio de solicitações HTTP.</li> 
    <li> zipfile &#8594; Ler arquivos zip sem precisar extraí-los.</li>
    <li> io &#8594; Ler os arquivos DICOM como bytes.</li>
    <li> torchxrayvision &#8594; Possibilitar a utilização de modelos pré-treinados de <i> Machine Learning</i>.</li>
    <li> pydicom &#8594; Realizar a leitura e escrita de arquivos DICOM.</li>
    <li> pathlib &#8594; Possibilitar a criação e a leitura de frases como caminhos no diretório.</li>
    <li> json &#8594; Criar e ler arquivos .json.</li>
    <li> re &#8594; Extrair informações de strings de maneira mais descomplicada.</li>
    <li> datetime &#8594; Mostrar informações sobre o dia e hora atuais para colocar no DICOM SR.</li>
  </ul>
</ol> 

<h2> ⚠️Problemas encontrados </h2>
<ol> 
  <li> A biblioteca Torch não estava sendo lida no meu desktop.</li>
  <li> Meu desktop pessoal está no limite das configurações necessárias para rodar o Docker, então foi complicado conseguir encontrar uma versão que funcionava.</li>
  <li> O upload dos arquivos ao servidor não estava sendo persistido para outra inicialização.</li>
  <li> Mesmo tenho conseguido usar o volume para persistir os dados, não estava conseguindo acessar os arquivos dentro desse volume com outro imagem.</li>
  <li> Ao carregar os arquivos .dcm no modelo, metade deles estava com o dobro da intensidade máxima aguentada pela função de leitura xrv.utils.read_xray_dcm.</li>
  <li> Pouca informação sobre a criação de arquivos DICOM SR.</li>
  <li> .</li>
  <li> .</li>
</ol>
<h2> Aprendizado obtido </h2>

<p> Com esse projeto, pude aprender a configurar contêiners, imagens e volumes no docker, bem como entender os benefícios de se utilizar esse software, como:
  <li> Isolar um ambiente virtual com apenas as dependências necessárias e impedir a interferência de outras bibliotecas.</li>
  <li> Poupar memória do computador usando o armazenamento em nuvem.</li>
  Além disso, também consegui experenciar uma boa maneira de se usar modelos prontos de IA para ajudar no diagnóstico de pacientes por meio de arquivos .dcm; <br>
  Outro ponto importante foi que aprendi como ler esses arquivos .dcm, como também escrevê-los; <br>
  Ademais, pude melhorar meu entendimento sobre servidores e sua comunicação via API rest; <br>
</p>

<h2> Primeira parte - Criar e rodar um servidor PACs OrthanC no Docker </h2>

<p> Nesta primeira etapa do projeto, mostrou-se necessário aprender como criar um servidor no Docker e como se dava a sua comunicação com PACs Orthanc. Após algumas pesquisas, consegui descobrir como esses fatos aconteciam e como configurar alguns elementos, o arquivo "orthanc.json" traz a configuração de um usuário qualquer com uma senha e acesso remoto autorizado para o servidor funcionando</p>

<p> Para o bom funcionamento do servidor, é necessário seguir os seguintes passos:</p>
<li> Baixar o Docker e seguir todos os passos para a sua instalação;</li>

<li> Criar um arquivo docker-compose.yml e um orthanc.json em um mesmo diretório de sua escolha para configurar o servidor e os usuários, se necessário, respectivamente;</li>

<li> No terminal de comando do seu desktop, escrever a seguinte linha de código:</li>

```
docker-compose up -d
```

<h2> Segunda parte - Adicionar arquivos DICOM ao servidor usando Python. </h2>

<p>Para essa etapa do projeto foi necessário escolher e coletar os <a href="https://drive.google.com/file/d/1Decc3rX_5oxF-4VvQxtWVqkV91O_Auf9/view">dados</a> para que pudessem ser enviados ao servidor.</p>
<p> Em sequência, foi preciso descobrir como os arquivos são formatados, como o servidor recebe dados e qual era a melhor maneira de enviá-los.</p>
<p> Assim, cheguei à conclusão.</p>
<li> Arquivos DICOM são binários e devem ser lidos como bytes para garantir que sejam enviados corretamente.</li>
<li> APIs REST, como a do Orthanc, esperam que arquivos sejam transferidos como dados binários em um formulário HTTP.</li>
<li> Ler como bytes preserva a integridade do arquivo, evitando perdas ou alterações indesejadas.</li>

<p> E, por isso, o código foi estruturado para que fosse possível ler os arquivos direto da pasta zip e enviá-los de forma binária. Esse código em questão foi nomeado como enviar_arquivos.py e, para que funcione corretamente basta executá-lo quando o servidor, ou o contêiner, estiver em operação.</p>

<h2> Terceira parte - Classificar os dados usando um modelo pré-treinado de <i>Machine Learning</i> </h2>

<p> Para essa etapa, desenvolvi o código chamado de classificar.py. Esse código coleta os arquivos do volume Docker, os lê como .dcm e usa o modelo "densenet121-res224-all" para diagnosticar o paciente e então montar um .json com o resultado obtido. Observe que o arquivo docker-compose possui uma configuração de volume para a imagem a ser criada a seguir, usando o mesmo volume da imagem do servidor, isso é o que tornou possível a utilização dessa memória.</p>

<p> Para que esse script funcione corretamente é necessário criar um arquivo Dockerfile com as bibliotecas e arquivos necessário por ele. Além disso, é preciso criar uma imagem no docker usando esse arquivo e depois executá-la com os seguintes comandos:</p>

```
docker build -t teste_xray_imagem .
```
<p>Comando para criar a imagem com o nome de teste_xray_imagem.</p>

```
docker run -it --rm -v docker_teste_orthanc_db:/var/lib/orthanc/db  teste_xray_imagem
```
<p> Nesse comando se pode observar o volume criado no docker (docker_teste_orthanc_db), sua localização (/var/lib/orthanc/db) e a imagem que estamos executando (teste_xray_imagem).</p> 

<p> Esse comando irá printar um dicionário no terminal, para transformar esse dicionário em arquivo .json, usei o código abaixo, preferi fazer desse jeito manual por ainda não entender completamente como salvar os arquivos da imagem diretamente no desktop local para facilitar o acesso.</p>

```python
import json
dict = {dicionario_printado}
# Nome do arquivo JSON que será salvo
nome_do_arquivo = "resultados.json"

# Escrevendo os dados no arquivo JSON
with open(nome_do_arquivo, 'w') as arquivo_json:
    json.dump(dict, arquivo_json, indent=4)
```
  
<p> obs: no código (classificar.py) há uma função para coletar esses arquivos por meio da API rest do servidor que foi o primeiro método que pensei para realizar essa tarefa, mas como era necessário baixar os arquivos novamente, pensei ser melhor encontrar uma forma de usar os arquivos do próprio volume. É por esse motivo que o docker-compose foi atualizado para construir uma mesma network para ambas as imagens, possibilitar a conexão via API.</p>

<h2> Quarta parte - Criar um arquivo DICOM SR <i> (Structured Report) </i> para cada arquivo DICOM </h2>

<p> Essa foi a parte mais difícil desse projeto por conta da falta de informação encontrada na internet sobre como criar esse tipo de arquivo. A parte de os enviar para a mesma pasta que os respectivos pacientes já foi mais tranquila usando o método de envio pela API rest.</p>


