const form = document.getElementById("form");

form.addEventListener("submit", function(event) {
    let userId = form.elements["login_id"].value;
    let userPw1 = form.elements["password"].value;
    let userPw2 = form.elements["password2"].value;
    let userPhone = form.elements["phone"].value.trim();
    let userEmail = form.elements["email"].value.trim();
    let valid = true;

    if (userId.length < 6) {
        event.preventDefault(); 
        alert("아이디가 너무 짧습니다. 6자 이상 입력해주세요.");
        return;
    }

    if (userPw1 !== userPw2) {
        event.preventDefault(); 
        alert("비밀번호가 일치하지 않습니다.");
        return;
    }
    const phoneRegex = /^\d{3}-\d{3,4}-\d{4}$/; 
    if (!phoneRegex.test(userPhone)) { document.getElementById('phoneError').style.display = 'block'; 
        valid = false; 
    } else { 
        document.getElementById('phoneError').style.display = 'none'; 
    }
    
    
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(userEmail)) {
        event.preventDefault();
        alert("유효한 이메일 주소를 입력해주세요.");
        return;
    }

});