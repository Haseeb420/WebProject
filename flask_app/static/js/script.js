

const updateProfile = () => {
    document.getElementById('profileData').style.display = "none";
    document.getElementById('updateProfile').style.display = "block";
}

const validateProfile = () => {
    let name = document.getElementById('user_name').value;
    let email = document.getElementById('user_email').value;
    let phone = document.getElementById('user_phone').value;
    name_pattern = /^[A-Z]{1}[a-z]{2,20} [A-Z]{1}[a-z]{2,20}$/
    email_pattern = /^[a-z][a-zA-Z0-9_]{2,}@[a-z]{2,10}[.]{1}[a-z.]{1,}$/;
    phone_pattern = /^[03]{2}[0-9]{9}$/;


    if (!(name_pattern.test(name))) {
        document.getElementById('name_error').innerHTML = "Name Can't be Empty";
        return false;
    }
    else if (!(email_pattern.test(email))) {
        document.getElementById('email_error').innerHTML = "Enter Valid email ";
        return false;
    }
    else if (!(phone_pattern.test(phone))) {
        document.getElementById('phone_error').innerHTML = "Enter Valid phone";
        return false;
    }

    return true;
}

function validatefname() {
    let fname = document.getElementById('fname').value
    pattern = /^[A-Z]{1}[a-z]{2,20}$/
    if (!(pattern.test(fname))) {
        document.getElementById('fname_error').innerHTML = "1)First name length should be between 3 to 20 <br>2)First letter should be capital"
    }
    else {
        document.getElementById('fname_error').innerHTML = "";
    }
}

function validatelname() {
    let lname = document.getElementById('lname').value;
    pattern = /^[A-Z]{1}[a-z]{2,20}$/
    if (!(pattern.test(lname))) {
        document.getElementById('lname_error').innerHTML = "1)Last name length should be between 3 to 20 <br>2)First letter should be capital"
    }
    else {
        document.getElementById('lname_error').innerHTML = "";
    }
}


function validateEmail() {
    let email = document.getElementById('email').value;

    pattern = /^[a-z][a-zA-Z0-9_]{2,}@[a-z]{2,10}[.]{1}[a-z.]{1,}$/;
    document.getElementById("unique_email_error").innerHTML = "";
    if (!(pattern.test(email))) {
        document.getElementById('email_error').innerHTML = "please write correct Email";
    }
    else {
        document.getElementById('email_error').innerHTML = "";
        check_email();
    }
}

function validatePhone() {
    let phone = document.getElementById('phone').value;

    pattern = /^[03]{2}[0-9]{9}$/;
    document.getElementById("unique_phone_error").innerHTML = "";
    if (!(pattern.test(phone))) {
        document.getElementById('phone_error').innerHTML = "please enter correct phone";
    }
    else {
        document.getElementById('phone_error').innerHTML = "";
        check_phone();
    }
}


function validatePassword() {
    let pattern = /^(?=.*[0-9])(?=.*[!@#$%&*.,])[a-zA-Z0-9!@#$%&*.,]{8,16}$/
    let password = document.getElementById('password').value;
    if (!(pattern.test(password))) {
        document.getElementById('password_error').innerHTML = "1)password Length should be between 8-16<br>2) password should contain aleast 1 digit and special character";
    }
    else {
        document.getElementById('password_error').innerHTML = "";
    }

}

function confirmPassword() {
    let password = document.getElementById('password').value;
    console.log(password)
    let confirm_password = document.getElementById('confirm_password').value;
    if (password == confirm_password) {
        document.getElementById('confirm_password_error').innerHTML = ""
    }
    else {
        document.getElementById('confirm_password_error').innerHTML = "You should confirm your password...."
    }
}


function check_email() {
    document.getElementById("unique_email_error").innerHTML = "";
    let email = document.getElementById('email').value;
    console.log("current_password :" + email)
    d = {
        "email": email
    }
    console.log(d["email"])
    dataString = JSON.stringify(d)
    console.log(dataString)
    req = new XMLHttpRequest();
    req.open("POST", "/check_email");
    req.setRequestHeader("Content-Type", "application/json");
    req.send(dataString)
    req.onreadystatechange = function () {
        if (req.readyState == 4 && req.status == 200) {
            response = req.responseText;
            console.log(response);
            responseJson = JSON.parse(response);
            console.log(responseJson["not_unique"]);
            if (responseJson["not_unique"]) {
                document.getElementById("unique_email_error").innerHTML = "Email already Exist";

            }
        }
    }
}
function check_phone() {
    document.getElementById("unique_email_error").innerHTML = "";
    let phone = document.getElementById('phone').value;
    console.log("phone :" + phone)
    d = {
        "phone": phone
    }
    console.log(d["phone"])
    dataString = JSON.stringify(d)
    console.log(dataString)
    req = new XMLHttpRequest();
    req.open("POST", "/check_phone");
    req.setRequestHeader("Content-Type", "application/json");
    req.send(dataString)
    req.onreadystatechange = function () {
        if (req.readyState == 4 && req.status == 200) {
            response = req.responseText;
            console.log(response);
            
        }
    }
}
