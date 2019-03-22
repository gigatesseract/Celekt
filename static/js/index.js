function readURL(input) {
  console.log(input.files[0]);
  if (input.files && input.files[0]) {
    var reader = new FileReader();
    reader.onload = function(e) {
      var img = document.getElementById("image-render-before");
      console.log("read?");

      img.src = e.target.result;
      img.height = 300;
      img.width = 400;
      // document.getElementById("image-render-before").appendChild(img);
      //   $("#image-render-before")
      //     .attr("src", e.target.result)
      //     .width(150)
      //     .height(200);
    };
    reader.readAsDataURL(input.files[0]);
  }
}

$(function() {
  $(".body")
    .children()
    .each(function() {
      $(this).hide();
    });
  $("#photo").show();
  $("li").on("click", function() {
    $("ul.navbar-nav li").each(function() {
      $(this).removeClass("active");

      $(
        "#" +
          $(this)
            .text()
            .toLowerCase()
            .split(" ")
            .join("-")
      ).hide();
    });
    $(this).addClass("active");

    $(
      "#" +
        $(this)
          .text()
          .toLowerCase()
          .split(" ")
          .join("-")
    ).show();
  });

  $("#image-form").submit(function(e) {
    e.preventDefault();

    var form_data = new FormData($("#image-form")[0]);
    form_data.append("download", $("#download").is(":checked"));
    // console.log("formdata? ", fd);
    $.ajax({
      url: "http://127.0.0.1:5000/recognise",
      type: "POST",
      processData: false,
      contentType: false,
      data: form_data,
      cache: false,
      success: function(result) {
        // $("#image-render").text(result.key);
        base64 = result.key;
        // // console.log(base64);
        var img = document.getElementById("image-render-after");
        img.src = "data:image/jpg;base64," + base64;
        img.width = 400;
        img.height = 300;
        console.log("success");
        document.getElementById("download-link").href = img.src;

        // while (render.children.length > 1)
        //   render.removeChild(render.children[1]);
        // console.log(render.children);

        // document.getElementById("image-render").appendChild(img);
      },
      error: function(error) {
        console.log(error);
      }
    });
  });
});
