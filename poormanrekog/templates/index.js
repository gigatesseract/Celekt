var width, height;

function readURL(input) {
  var c = document.getElementById("imagecanvas");
  var ctx = c.getContext("2d");
  ctx.clearRect(0, 0, c.width, c.height);

  console.log(input.files[0]);
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    var img = new Image();
    reader.onload = function(e) {
      img.onload = function() {
        console.log("read?");
        console.log(img.width);
        width = img.width;
        height = img.height;
        ctx.drawImage(img, 0, 0, c.width, c.height);
      };

      img.src = e.target.result;
    };
    reader.readAsDataURL(input.files[0]);
  }
}

$(function() {
  $("li").on("click", function() {
    console.log("clicked");
    $("ul.navbar-nav li").each(function() {
      $(this).removeClass("active");
    });
    $(this).addClass("active");
  });

  $("#image-form").submit(function(e) {
    e.preventDefault();
    e.stopPropagation();
    var form_data = new FormData($("#image-form")[0]);
    form_data.append("image", true);
    console.log("submitted");
    $.ajax({
      url: "http://127.0.0.1:8765/recogniseFaces",
      type: "POST",
      processData: false,
      contentType: false,
      data: form_data,
      cache: false,
      success: function(result) {
        console.log(result);

        console.log(result.likeliness);
        console.log(typeof result.coordinates);
        var c = document.getElementById("imagecanvas");
        var ctx = c.getContext("2d");
        var wscale = c.width / width;
        var hscale = c.height / height;
        console.log(hscale);
        result.coordinates.forEach(function(element, index) {
          console.log("elelele");
          ctx.strokeStyle = "yellow";
          ctx.beginPath();
          ctx.moveTo(element["left"] * wscale, element["top"] * hscale);
          ctx.lineTo(element["right"] * wscale, element["top"] * hscale);
          ctx.lineTo(element["right"] * wscale, element["bottom"] * hscale);
          ctx.lineTo(element["left"] * wscale, element["bottom"] * hscale);
          ctx.lineTo(element["left"] * wscale, element["top"] * hscale);
          ctx.closePath();
          ctx.stroke();
          ctx.moveTo(element["left"] * wscale, element["top"] * hscale - 5);
          ctx.font = "12px Arial";
          ctx.fillStyle = "yellow";
          ctx.fillText(
            index,
            element["left"] * wscale,
            element["top"] * hscale
          );
          console.log(index);
        });
        likeliness_string = "";
        result.likeliness.forEach(function(element, index) {
          likeliness_string += `
          <div class="card">

          <div class="card-body">
            <h5 class="card-title">Face ${index}:</h5>`;
          element.forEach(function(element) {
            likeliness_string += `<span class="card-text">${element.name}: ${
              element.likeliness
            }</span><br>`;
          });

          likeliness_string += `  </div>
            </div>
            `;
        });
        $("#image-likeliness").html(likeliness_string);
        console.log(likeliness_string);
        if (result.coordinates.length == 0) {
          $("#image-likeliness").html("<p>No faces found </p>");
        }
      },
      error: function(error) {
        console.log(error);
      }
    });

    return false;
  });
  $("#video-form").submit(function(e) {
    e.preventDefault();
    e.stopPropagation();
    var form_data = new FormData($("#video-form")[0]);
    console.log("submitted");
    $.ajax({
      url: "http://127.0.0.1:8765/recogniseFaces",
      type: "POST",
      processData: false,
      contentType: false,
      data: form_data,
      cache: false,
      success: function(result) {
        console.log(result);
      },
      error: function(error) {
        console.log(error);
      }
    });

    return false;
  });
});
