# Case HapVida


 <h2>Problema:</h2>
 <p>A má conexão entre médicos e pacientes pode resultar em atrasos no atendimento, falta de coordenação de cuidados, dificuldade no compartilhamento de informações, perda de dados cruciais e ineficiência na gestão de ocorrências. O HealthConnect surge como uma solução para esses problemas, proporcionando uma conexão eficiente que agiliza o atendimento, melhora a coordenação de cuidados e facilita o compartilhamento de informações, contribuindo para uma prestação de serviços de saúde mais eficaz e ágil.</p>


<h2>Solução:</h2>
 
  <p>O HealthConnect veio com uma solução abrangente que utiliza o ESP32, sensores de pulso, temperatura e acelerômetro para fornecer monitoramento contínuo e em tempo real. Este dispositivo compacto e portátil é capaz de medir os batimentos cardíacos, a temperatura corporal, proporcionando informações cruciais para intervenções médicas oportunas.</p>


 <h3>Componentes</h3>
    <p>Para implementar a solução você precisará dos seguintes componentes que estão distribuídos em duas etapas, são elas a etapa física e virtual. Para a etapa física, será necessário:</p>
    
  | Componente                                              
  |---------------------------------------------------------|
  | Pulse Generator                                  
  | MP6050 - Acelerometro que mede Temepratura                                          
  | Display SSD1306                                                  
  | Real Time Clocker (RTC)                                            
  | ESP32                                                   
  | Fio microUSB para ligar o ESP                            
  | Protoboard                                              
   
 
 <h2>Tecnologia usada e como iniciar o projeto</h2>
   
   <p>Para esse projeto, utilizamos a IDE do arduino para programar o ESP32, desse modo, toda a linguagem é em c++. Entretanto, primeiramente é preciso instalar o pacote do ESP32 da espressif. Agora para a aplicação do Fiware, ela é toda configurada em python para enviar os dados para o banco de dados;</p>
   <p>Para toda a configuração da Tela OLED e acelerômetro, utilizamos as bibliotecas disponíveis na IDE do arduino, como: Adafruit GFX Library, Adafruit SSD1306 e Adafruit MPU6050, já para configurar o sistema a internet e protocolo mqtt utilizamos a biblioteca PubSubClient(by nick o'lary). Terminado isso basta utilizar o códigos que disponibilizamos e gravar o código no ESP32.</p>
 
  <h2>Simulação no WOKWI</h2>
    <p>Wokwi é uma plataforma online que oferece simuladores de hardware para desenvolvimento e teste de projetos eletrônicos. Pensando nisso, foi realizado o mesmo projeto no WOKWI, para facilitar a compreensão e caso não seja possível a reprodução física.</p>
    <p>Caso queira verificar a simulação acesse esse link https://wokwi.com/projects/382307797964312577 ou Clique <a href="https://wokwi.com/projects/382307797964312577">aqui </a> 
  
  
  <h3>Referências</h3>
 <p>Buscando mais informações e aprimoramento, nossas referências foram:</p>
     <ol><li>Link: https://github.com/fabiocabrini/fiware</li>
         <li>Link: https://www.hapvida.com.br/site/</li>
   

       
