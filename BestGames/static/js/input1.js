const wrapper = document.querySelector(".input-wrapper"),
      textInput = document.querySelector("input[type='text']");
        
textInput.addEventListener("keyup", event => {
  wrapper.setAttribute("data-text", event.target.value);
});