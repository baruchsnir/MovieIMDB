function fnChangeBorder(){
      var imgElement = document.getElementById("img1");
      var attr = imgElement.getAttribute("class");
      console.log("This is attr - "+attr)
      if (attr == "click0")
      {
         imgElement.className="click1";
         imgElement.style.height = '200px';
         imgElement.style.width = '200px';
      }
      if (attr == "click1")
      {
         imgElement.className="click2";
         imgElement.style.height = '300px';
         imgElement.style.width = '300px';
      }
      if (attr == "click2")
      {
         imgElement.className="click0";
         imgElement.style.height = '100px';
         imgElement.style.width = '100px';
      }
 }