window.onload = () => {
  const text = "Initializing WebCreep AI...";
  const typeTarget = document.getElementById("init-text");

  let index = 0;
  function typeWriter() {
    if (index < text.length) {
      typeTarget.innerHTML += text.charAt(index);
      index++;
      setTimeout(typeWriter, 60);
    } else {
      setTimeout(() => {
        document.getElementById("intro").style.display = "none";
        document.getElementById("main").classList.remove("hidden");
      }, 1200);
    }
  }

  typeWriter();
};
