$(function() {
  console.log("document ready");

  $("#image").on("change", function() {
    console.log(this.innerHTML);
  });

  $("#image-form").submit(function(e) {
    e.preventDefault();
    console.log("form about to be subitted");
    var form_data = new FormData($("#image-form")[0]);
    // console.log("formdata? ", fd);
    $.ajax({
      url: "http://127.0.0.1:5000/recognise",
      type: "POST",
      processData: false,
      contentType: false,
      data: form_data,
      cache: false,
      success: function(result) {
        console.log(result.key);
        // $("#image-render").text(result.key);
        base64 = result.key;
        // console.log(base64);
        var img = new Image();
        img.src = "data:image/jpg;base64," + base64;
        render = document.getElementById("image-render");

        while (render.firstChild) render.removeChild(render.firstChild);

        document.getElementById("image-render").appendChild(img);
      },
      error: function(error) {
        console.log(error);
      }
    });
    // return false;
  });
  // var submit = document.getElementById("submit"); myvar = 10; function
  // submit() { console.log(document.getElementById("image")); var xhttp = new
  // XMLHttpRequest(); xhttp.onreadystatechange = function() { console; if
  // (this.readyState == 4 && this.status == 200) console.log(this.responseText);
  // }; xhttp.open("POST", "http://127.0.0.1:5000/recognise", true);
  // xhttp.setRequestHeader("Content-type", "application/json"); json_object = {
  // // image: document.getElementById("image").value, hello: "hi" }; //
  // console.log(json_object); xhttp.send(JSON.stringify(json_object)); return
  // false; }
});
