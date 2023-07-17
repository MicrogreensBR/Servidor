const btnMobile = document.getElementById("btnMobile");

function openMenu(){
  const content = document.getElementsByClassName('main')[0];
  const nav = document.getElementById("menu_lateral_mobile");
  nav.classList.toggle('active');
  
  if (document.getElementsByClassName("active").length){      
    content.style.display = 'none';  
    document.body.style.overflow = 'hidden';
  }
  else{
    content.style.display = 'block';  
    document.body.style.overflow = 'visible';
  }
}

btnMobile.addEventListener('click', openMenu);