const API = "https://your-backend.onrender.com";

function login() {
 fetch(API+"/login",{method:"POST",
 headers:{"Content-Type":"application/json"},
 body:JSON.stringify({
 email:email.value,password:password.value})
 }).then(r=>r.json()).then(d=>{
  if(d.success) window.location="dashboard.html";
 });
}

function signup() {
 fetch(API+"/signup",{method:"POST",
 headers:{"Content-Type":"application/json"},
 body:JSON.stringify({
 email:email.value,password:password.value})
 });
}

function studyPlan(){
 fetch(API+"/study-plan",{method:"POST",
 body:JSON.stringify({subject:"Math",hours:10}),
 headers:{"Content-Type":"application/json"}})
 .then(r=>r.json()).then(d=>output.innerText=JSON.stringify(d,null,2));
}
