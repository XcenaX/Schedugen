function checkAllCheckboxes(){
    checkboxes = document.querySelectorAll('input[type=checkbox]');
    for(var i = 0; i < checkboxes.length; i++){
        checkboxes[i].checked = true;
    }
}

function switchAllCheckboxes(){
    var checkboxes = document.querySelectorAll('input[type=checkbox]');
    for(var i = 1; i < checkboxes.length; i++){
        checkboxes[i].checked = checkboxes[0].checked;
    }
}

function activateSVIN(){
    var svin = document.getElementById("SVIN");
    svin.classList.add("active");
}