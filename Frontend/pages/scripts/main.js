// Open and close the National ID registration form
function openForm() {
  document.getElementById("popup").style.display = "block";
  document.getElementById("overlay").style.display = "block";
}

function closeForm() {
  document.getElementById("popup").style.display = "none";
  document.getElementById("overlay").style.display = "none";
}

// Handle form submission for National ID registration
document.getElementById("nationalIdForm").addEventListener("submit", function(event) {
  event.preventDefault();
  
  const isSuccess = true; // Simulate form success/failure
  
  if (isSuccess) {
      window.location.href = './pages/Dashboard/dashboard.html'; // Redirect on form success
  } else {
      alert('Registration failed. Please try again.');
  }
});

// Google sign-in callback
function onSignIn(googleUser) {
  var profile = googleUser.getBasicProfile();
  console.log('ID: ' + profile.getId());
  console.log('Name: ' + profile.getName());
  console.log('Email: ' + profile.getEmail());

  const isGoogleSignInSuccess = true; // Simulate Google sign-in success/failure
  
  if (isGoogleSignInSuccess) {
      window.location.href = './pages/Dashboard/dashboard.html'; // Redirect on Google sign-in success
  } else {
      alert('Google sign-in failed. Please try again.');
  }
}

// Sign in with Google function
function signInWithGoogle() {
  gapi.auth2.getAuthInstance().signIn().then(onSignIn).catch(function(error) {
      alert('Google sign-in failed. Please try again.');
  });
}

// Initialize Google Auth API
function initGoogleAuth() {
  gapi.load('auth2', function() {
      gapi.auth2.init();
  });
}

window.onload = initGoogleAuth;
