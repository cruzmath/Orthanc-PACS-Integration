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
  </ul>
</ol> 

<h2> ⚠️Problemas encontrados </h2>
1. Meu desktop pessoal está no limite das configurações necessárias para rodar o Docker, então foi complicado conseguir encontrar a versão que funcionava.

<h2> Aprendizado obtido </h2>

<h2> Primeira parte - Criar e rodar um servidor PACs OrthanC no Docker </h2>

<p> Nesta primeira etapa do projeto, mostrou-se necessário aprender como criar um servidor no Docker e como se dava a sua comunicação com PACs Orthanc. Após algumas pesquisas, consegui descobrir como esses fatos aconteciam e como configurar alguns elementos, o arquivo "orthanc.json" traz a configuração de um usuário qualquer com uma senha e acesso remoto autorizado para o servidor funcionando</p>

<p> Para o bom funcionamento do servidor, é necessário seguir os seguintes passos:</p>
<li> Baixar o Docker e seguir todos os passos para a sua instalação;</li>

<li> Criar um arquivo docker-compose.yml e um orthanc.json em um mesmo diretório de sua escolha para configurar o servidor e os usuários, se necessário, respectivamente;</li>

<li> No terminal de comando do seu desktop, escrever a seguinte linha de código:</li>

```
docker-compose up -d
```

<h2> Segunda parte - Adicionar arquivos DICOM ao servidor usando Python </h2>

<p>Para essa etapa do projeto foi necessário escolher e coletar os <a href="https://drive.google.com/file/d/1Decc3rX_5oxF-4VvQxtWVqkV91O_Auf9/view">dados</a> para que pudessem ser enviados ao servidor.</p>
<p> Em sequência, foi preciso descobrir como os arquivos são formatados, como o servidor recebe dados e qual era a melhor maneira de enviá-los.</p>
<p> Assim, cheguei a conclusão.</p>
<li> Arquivos DICOM são binários e devem ser lidos como bytes para garantir que sejam enviados corretamente.</li>
<li> APIs REST, como a do Orthanc, esperam que arquivos sejam transferidos como dados binários em um formulário HTTP.</li>
<li> Ler como bytes preserva a integridade do arquivo, evitando perdas ou alterações indesejadas.</li>

<p> E, por isso, o código foi estruturado para que fosse possível ler os arquivos direto da pasta zip e enviá-los de forma binária.</p>

<h2> Terceira parte - Classificar os dados usando um modelo pré treinado de <i>Machine Learning</i> </h2>

<h2> Quarta parte - Criar um arquivo DICOM SR <i> (Structured Report) </i> para cada arquivo DICOM </h2>


