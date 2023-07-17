var x = window.matchMedia("(max-width: 600px)")

function insertAfter(referenceNode, newNode) {
  referenceNode.parentNode.insertBefore(newNode, referenceNode.nextSibling);
}

function removeElementsByClass(className){
  const elements = document.getElementsByClassName(className);
  while(elements.length > 0){
      elements[0].parentNode.removeChild(elements[0]);
  }
}

function func() {
  const seed_id = document.getElementById("microgreens").value;
  let route = '/info/' + seed_id.toString()
  let imgdir = 'styles/imgs/' + seed_id.toString() + '.webp'

  fetch(route)
  .then(function (response) {
      return response.json();
  }).then(function (infos) {        
    // MOBILE
    if(x.matches){
      removeElementsByClass("infos_chart")   
      removeElementsByClass("menu_start") 

      const infos_chart = document.createElement("div");
      infos_chart.setAttribute('class', 'infos_chart');

      infos_chart.style.backgroundColor = "rgb(255, 246, 208)";
      infos_chart.style.color = "#552200";
      infos_chart.style.textAlign = "center";
      infos_chart.style.marginTop = "1.5rem";
      infos_chart.style.marginLeft = "0.8rem";
      infos_chart.style.marginRight = "0.8rem";
      infos_chart.style.border = "2px solid #552200"; 
      infos_chart.style.borderRadius= "5px";

      const info_title = document.createElement("div");
      info_title.setAttribute('class', 'info_title');
      info_title.style.fontSize = "1.3rem";
      info_title.style.marginLeft = "20px";
      info_title.style.textAlign = "center";
      info_title.style.fontWeight = "700";
      info_title.style.paddingTop = "1.5rem ";

      var newContent = document.createTextNode("Informações");
      info_title.appendChild(newContent);                
      infos_chart.appendChild(info_title);
      
      const container = document.createElement("div");
      container.setAttribute('class', 'container');
      container.style.display = "flex";
      container.style.flexDirection = "column";
      container.style.padding = "20px 20px 20px 20px";        

      const information = document.createElement("div");
      information.setAttribute('class', 'information');
      information.style.flex = "1";                 
      information.style.textAlign = "justify";

      const p1 = document.createElement("p");
      p1.setAttribute('class', 'p_info');
      p1.style.textAlign = "justify";        
      p1.style.paddingBottom = "0.6rem"; 

      newContent = document.createTextNode("𝗣𝗿𝗲𝗽𝗮𝗿𝗼: " + infos.soaking_time);
      p1.appendChild(newContent);  
      information.appendChild(p1);  

      const p2 = document.createElement("p");
      p2.setAttribute('class', 'p_info');
      p2.style.textAlign = "justify";    
      p2.style.paddingBottom = "0.6rem";     
      
      newContent = document.createTextNode("𝗤𝘂𝗮𝗻𝘁𝗶𝗱𝗮𝗱𝗲 𝗱𝗲 𝘀𝗲𝗺𝗲𝗻𝘁𝗲𝘀: " + infos.seed_quantity);
      p2.appendChild(newContent);  
      information.appendChild(p2);

      const p3 = document.createElement("p");
      p3.setAttribute('class', 'p_info');
      p3.style.textAlign = "justify";    
      p3.style.paddingBottom = "0.6rem";     
      
      newContent = document.createTextNode("𝗧𝗲𝗺𝗽𝗲𝗿𝗮𝘁𝘂𝗿𝗮 𝗺𝗲́𝗱𝗶𝗮: " + infos.avg_temperature + " C°");
      p3.appendChild(newContent);  
      information.appendChild(p3);  

      const p4 = document.createElement("p");
      p4.setAttribute('class', 'p_info');
      p4.style.textAlign = "justify";    
      p4.style.paddingBottom = "0.6rem";     
      
      newContent = document.createTextNode("𝗡𝗶́𝘃𝗲𝗹 𝗱𝗲 𝘂𝗺𝗶𝗱𝗮𝗱𝗲: " + infos.watering);
      p4.appendChild(newContent);  
      information.appendChild(p4);  

      const p5 = document.createElement("p");
      p5.setAttribute('class', 'p_info');
      p5.style.textAlign = "justify";    
      p5.style.paddingBottom = "0.6rem";     
      
      newContent = document.createTextNode("𝗔𝗹𝘁𝘂𝗿𝗮 𝗺𝗲́𝗱𝗶𝗮 𝗽𝗮𝗿𝗮 𝗰𝗼𝗹𝗲𝘁𝗮 : " + infos.avg_harvest_height + " cm");
      p5.appendChild(newContent);  
      information.appendChild(p5);  

      const p6 = document.createElement("p");
      p6.setAttribute('class', 'p_info');
      p6.style.textAlign = "justify";    
      p6.style.paddingBottom = "0.6rem";     
      
      newContent = document.createTextNode("𝗔𝗹𝘁𝘂𝗿𝗮 𝗺𝗲́𝗱𝗶𝗮 𝗽𝗮𝗿𝗮 𝗰𝗼𝗹𝗲𝘁𝗮 : " + infos.avg_harvest_height + " cm");
      p6.appendChild(newContent);  
      information.appendChild(p6);  
      
      if (infos.min_days_harvest == '0'){
        const p7 = document.createElement("p");
        p7.setAttribute('class', 'p_info');
        p7.style.textAlign = "justify";    
        p7.style.paddingBottom = "0.6rem";     
        
        newContent = document.createTextNode("𝗖𝗼𝗹𝗵𝗲𝗿 𝗰𝗼𝗺 : " + infos.max_days_harvest + " dias");
        p7.appendChild(newContent);  
        information.appendChild(p7);  
      }

      else{
        const p7 = document.createElement("p");
        p7.setAttribute('class', 'p_info');
        p7.style.textAlign = "justify";    
        p7.style.paddingBottom = "0.6rem";     
        
        newContent = document.createTextNode("𝗖𝗼𝗹𝗵𝗲𝗿 𝗮 𝗽𝗮𝗿𝘁𝗶𝗿 𝗱𝗲: " + infos.min_days_harvest + " dias");
        p7.appendChild(newContent);  
        information.appendChild(p7);  

        const p8 = document.createElement("p");
        p8.setAttribute('class', 'p_info');
        p8.style.textAlign = "justify";    
        p8.style.paddingBottom = "0.6rem";     
        
        newContent = document.createTextNode("𝗖𝗼𝗻𝘁𝗶𝗻𝘂𝗮𝗿 𝗰𝗼𝗹𝗵𝗲𝗻𝗱𝗼 𝗮𝘁𝗲́: " + infos.max_days_harvest + "º dia");
        p8.appendChild(newContent);  
        information.appendChild(p8);  
      }

      const figure = document.createElement("div");
      figure.setAttribute('class', 'figure');
      figure.style.flex = "1";
    
      const img = document.createElement("img");
      img.src = imgdir;       
      img.style.width = "90%";
      img.style.marginTop = "1.5rem";

      figure.appendChild(img);

      container.appendChild(information);
      container.appendChild(figure);
      infos_chart.appendChild(container);

      const currentDiv = document.getElementById("body1");
      insertAfter(currentDiv, infos_chart);

      const menu_start = document.createElement("div");
      menu_start.setAttribute('class', 'menu_start');
      menu_start.style.alignItems = "center";     
      menu_start.style.paddingTop = "30px"; 

      const revest = document.createElement("a");
      revest.href = "start?cod={{ cod_esp }}?seed_id=" + seed_id.toString();

      const botao = document.createElement("button");
      botao.setAttribute('class', 'botao');
      botao.setAttribute('id', 'botao');

      botao.style.fontWeight = "600"
      botao.style.backgroundColor = "rgba(221, 204, 128, 0.822)";
      botao.style.color = "#552200";
      botao.style.borderRadius = "50px";
      botao.style.border = "2px solid rgba(173, 158, 90, 0.822)";
      botao.style.cursor = "pointer";
      botao.style.fontSize = "20px";
      botao.style.transitionDuration = "0.4s";
      botao.style.width = "200px";
      botao.style.height = "50px";
      botao.style.marginBottom = "1.5rem"

      botao.onmouseover = function(){
        botao.style.opacity = '0.7';
      }

      botao.onmouseout = function(){
        botao.style.opacity = '1';
      }

      newContent = document.createTextNode("Iniciar cultivo");
      botao.appendChild(newContent);  
       
      revest.appendChild(botao);
      menu_start.appendChild(revest);
      insertAfter(infos_chart, menu_start);
    // DESKTOP  
    } else {
      removeElementsByClass("infos_chart")   
      removeElementsByClass("menu_start") 

      const infos_chart = document.createElement("div");
      infos_chart.setAttribute('class', 'infos_chart');

      infos_chart.style.backgroundColor = "rgb(255, 246, 208)";
      infos_chart.style.color = "#552200";
      infos_chart.style.marginTop = "20px";
      infos_chart.style.marginLeft = "50px";
      infos_chart.style.marginRight = "50px";
      infos_chart.style.border = "2px solid #552200"; 
      infos_chart.style.borderRadius= "5px";

      const info_title = document.createElement("div");
      info_title.setAttribute('class', 'info_title');
      info_title.style.fontSize = "20px";
      info_title.style.marginLeft = "20px";
      info_title.style.textAlign = "left";
      info_title.style.fontWeight = "700";
      info_title.style.paddingTop = "15px";

      var newContent = document.createTextNode("Informações");
      info_title.appendChild(newContent);                
      infos_chart.appendChild(info_title);
      
      const container = document.createElement("div");
      container.setAttribute('class', 'container');
      container.style.display = "flex";
      container.style.flexDirection = "row";
      container.style.padding = "20px 20px 20px 20px";        

      const information = document.createElement("div");
      information.setAttribute('class', 'information');
      information.style.flex = "1";        
      information.style.paddingRight = "10px";      
      information.style.textAlign = "left";

      const p1 = document.createElement("p");
      p1.setAttribute('class', 'p_info');
      p1.style.textAlign = "justify";        
      p1.style.paddingBottom = "4px"; 

      newContent = document.createTextNode("𝗣𝗿𝗲𝗽𝗮𝗿𝗼: " + infos.soaking_time);
      p1.appendChild(newContent);  
      information.appendChild(p1);  

      const p2 = document.createElement("p");
      p2.setAttribute('class', 'p_info');
      p2.style.textAlign = "justify";    
      p2.style.paddingBottom = "4px";     
      
      newContent = document.createTextNode("𝗤𝘂𝗮𝗻𝘁𝗶𝗱𝗮𝗱𝗲 𝗱𝗲 𝘀𝗲𝗺𝗲𝗻𝘁𝗲𝘀: " + infos.seed_quantity);
      p2.appendChild(newContent);  
      information.appendChild(p2);

      const p3 = document.createElement("p");
      p3.setAttribute('class', 'p_info');
      p3.style.textAlign = "justify";    
      p3.style.paddingBottom = "4px";     
      
      newContent = document.createTextNode("𝗧𝗲𝗺𝗽𝗲𝗿𝗮𝘁𝘂𝗿𝗮 𝗺𝗲́𝗱𝗶𝗮: " + infos.avg_temperature + " C°");
      p3.appendChild(newContent);  
      information.appendChild(p3);  

      const p4 = document.createElement("p");
      p4.setAttribute('class', 'p_info');
      p4.style.textAlign = "justify";    
      p4.style.paddingBottom = "4px";     
      
      newContent = document.createTextNode("𝗡𝗶́𝘃𝗲𝗹 𝗱𝗲 𝘂𝗺𝗶𝗱𝗮𝗱𝗲: " + infos.watering);
      p4.appendChild(newContent);  
      information.appendChild(p4);  

      const p5 = document.createElement("p");
      p5.setAttribute('class', 'p_info');
      p5.style.textAlign = "justify";    
      p5.style.paddingBottom = "4px";     
      
      newContent = document.createTextNode("𝗔𝗹𝘁𝘂𝗿𝗮 𝗺𝗲́𝗱𝗶𝗮 𝗽𝗮𝗿𝗮 𝗰𝗼𝗹𝗲𝘁𝗮 : " + infos.avg_harvest_height + " cm");
      p5.appendChild(newContent);  
      information.appendChild(p5);  

      const p6 = document.createElement("p");
      p6.setAttribute('class', 'p_info');
      p6.style.textAlign = "justify";    
      p6.style.paddingBottom = "4px";     
      
      newContent = document.createTextNode("𝗔𝗹𝘁𝘂𝗿𝗮 𝗺𝗲́𝗱𝗶𝗮 𝗽𝗮𝗿𝗮 𝗰𝗼𝗹𝗲𝘁𝗮 : " + infos.avg_harvest_height + " cm");
      p6.appendChild(newContent);  
      information.appendChild(p6);  
      
      if (infos.min_days_harvest == '0'){
        const p7 = document.createElement("p");
        p7.setAttribute('class', 'p_info');
        p7.style.textAlign = "justify";    
        p7.style.paddingBottom = "4px";     
        
        newContent = document.createTextNode("𝗖𝗼𝗹𝗵𝗲𝗿 𝗰𝗼𝗺 : " + infos.max_days_harvest + " dias");
        p7.appendChild(newContent);  
        information.appendChild(p7);  
      }

      else{
        const p7 = document.createElement("p");
        p7.setAttribute('class', 'p_info');
        p7.style.textAlign = "justify";    
        p7.style.paddingBottom = "4px";     
        
        newContent = document.createTextNode("𝗖𝗼𝗹𝗵𝗲𝗿 𝗮 𝗽𝗮𝗿𝘁𝗶𝗿 𝗱𝗲: " + infos.min_days_harvest + " dias");
        p7.appendChild(newContent);  
        information.appendChild(p7);  

        const p8 = document.createElement("p");
        p8.setAttribute('class', 'p_info');
        p8.style.textAlign = "justify";    
        p8.style.paddingBottom = "4px";     
        
        newContent = document.createTextNode("𝗖𝗼𝗻𝘁𝗶𝗻𝘂𝗮𝗿 𝗰𝗼𝗹𝗵𝗲𝗻𝗱𝗼 𝗮𝘁𝗲́: " + infos.max_days_harvest + "º dia");
        p8.appendChild(newContent);  
        information.appendChild(p8);  
      }

      const figure = document.createElement("div");
      figure.setAttribute('class', 'figure');
      figure.style.flex = "1";
    
      const img = document.createElement("img");
      img.src = imgdir;       
      img.style.height = "200px"

      figure.appendChild(img);

      container.appendChild(information);
      container.appendChild(figure);
      infos_chart.appendChild(container);

      const currentDiv = document.getElementById("body1");
      insertAfter(currentDiv, infos_chart);

      const menu_start = document.createElement("div");
      menu_start.setAttribute('class', 'menu_start');
      menu_start.style.alignItems = "center";     
      menu_start.style.paddingTop = "30px"; 

      const revest = document.createElement("a");
      revest.href = "start?cod={{ cod_esp }}?seed_id=" + seed_id.toString();

      const botao = document.createElement("button");
      botao.setAttribute('class', 'botao');
      botao.setAttribute('id', 'botao');

      botao.style.fontWeight = "600"
      botao.style.backgroundColor = "rgba(221, 204, 128, 0.822)";
      botao.style.color = "#552200";
      botao.style.borderRadius = "50px";
      botao.style.border = "2px solid rgba(173, 158, 90, 0.822)";
      botao.style.cursor = "pointer";
      botao.style.fontSize = "20px";
      botao.style.transitionDuration = "0.4s";
      botao.style.width = "200px";
      botao.style.height = "50px";
      
      botao.onmouseover = function(){
        botao.style.opacity = '0.7';
      }

      botao.onmouseout = function(){
        botao.style.opacity = '1';
      }

      newContent = document.createTextNode("Iniciar cultivo");
      botao.appendChild(newContent);  
       
      revest.appendChild(botao);
      menu_start.appendChild(revest);
      insertAfter(infos_chart, menu_start);

    }
  }); 
}