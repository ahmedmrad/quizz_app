function save_UserCode(){
    var data = document.getElementById('user_passcode').value;
    window.sessionStorage.setItem('user_passcode', data);
    console.log(data);
}


function get_ratings(){
    var  user_passcode = document.forms['final_part']['user_passcode'].value;
    var  difficulty_rating = document.forms['final_part']['difficulty_rating'].value;
    var  certainty_rating = document.forms['final_part']['certainty_rating'].value;
    if (final_part.difficulty_rating.value == ' ' || final_part.certainty_rating.value==' ' ) {
            errorAlert = 'Please rate your experience';
            document.getElementById('errorAlert').style.display='block';
            document.getElementById('errorAlert').innerHTML = errorAlert;
        }
    else{
        $.ajax({
            type: 'POST',
            url: '/get_ratings',
            data: {
                user_passcode : $('#user_passcode').val(),
                difficulty_rating : $('#difficulty_rating').val(),
                certainty_rating : $('#certainty_rating').val()
            },
            success : function(response){
                window.location.href = response.redirect;


            }
        })

    }
}


function get_Usercode(){
        var user_passcode = sessionStorage.getItem('user_passcode');
        console.log(user_passcode);
        document.getElementById('result').innerHTML = user_passcode;
}

function copyToClipboard(element) {
            var $temp = $("<input>");
            $("body").append($temp);
            $temp.val($(element).text()).select();
            document.execCommand("copy");
            $temp.remove();
        }

