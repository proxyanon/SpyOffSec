# SpyOffSec
SpyOffSec é um programa destinado ao controle e visualização remota de máquinas, com foco em segurança da informação. 

# Como usar ?
<ul>
  <li> 1. No arquivo <b>cliente.py</b> altere as variaveis <b><font color="red">ip</font></b> e <b><font color="red">port</font></b> para o que você vai ultilizar</li> 
  <li> 2. O <b>cliente.py</b> é a backdoor, o script que vai na máquina que vai ser visualizada/controlada</li>
  <li> 2. O <b>servidor.py</b> é o handler, o script que vai na máquina que vai visualizar/controlar</li>
</ul>

# Gerando um executável

<ul>
  <li> 1. Instale o pyinstaller : <b>$ pip install pyinstaller</b></li>
  <li> 2. Execute o comando : <b>$ pyinstaller --onefile cliente.py --noconsole</b></li>
  <li> 3. Serão criadas 2 pastas (<b>build/</b>, <b>dist/</b>) e o arquivo <b>cliente.spec</b></li>
  <li> 4. O executável está na pasta <b>dist/</b> o resto é descartável</li>
  <li> 5. Abra a pasta <b>dist/</b> e pronto somente executá-lo</li>
</ul>
