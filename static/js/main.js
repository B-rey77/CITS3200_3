// For the login/signup page
// Hide and display register and login box onclick
$(document).ready(function () {
    $(".register-tab").click(function () {
        $(".register-box").show();
        $(".login-box").hide();
        $(".register-tab").addClass("login-regstr");
        $(".login-tab").removeClass("login-regstr");
        $(".close-x").css('margin-left', "460px");
    });
    $(".login-tab").click(function () {
        $(".login-box").show();
        $(".register-box").hide();
        $(".login-tab").addClass("login-regstr");
        $(".register-tab").removeClass("login-regstr");
        $(".close-x").css('margin-left', "10px");
    });
});


// The Login/Register page: 
// trigger selected age group to autofill out the drop down box
function handleAgeChng (el) {
    document.querySelector('.age-span').innerHTML = el.value;
}


// For the quiz page: when final submit button is clicked,
// show a warning message
function submitMarking () {
    var answers = window.confirm("Save Questions?");
    if (confirm('Are you sure you want to submit your answers?')) {
        // Save it!
        console.log('Your answers have been saved.');
    } else {
        // Do nothing!
        console.log('Your asnwers have not been submitted. Please continue answering the questions.');
    }
}
