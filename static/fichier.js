document.addEventListener("DOMContentLoaded", function () {

    var obj1 = document.getElementById("actselect");
    const radioButton = document.querySelector('input[name="forget"]');

    obj1.addEventListener("change", function () {
        document.getElementById("myform").submit();
        document.querySelector(".col.rigth-column").style.backgroundColor = "red";
    });

    radioButton.addEventListener('change', function (e) {
        if (radioButton.checked) {
            document.querySelector(".col.rigth-column").style.backgroundColor = "red";
        }
      });

});

