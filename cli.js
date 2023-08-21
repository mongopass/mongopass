const terminalContent = document.getElementById("terminal-content");
const terminalInput = document.getElementById("terminal-input");

const commands = [
    "Do you want to register (r) or check a password (c)?",
    "Enter username:",
    "Enter password:",
    "Registration successful!"
];

let currentCommand = 0;

terminalInput.addEventListener("keydown", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        
        const userText = terminalInput.value;
        terminalContent.innerHTML += "<br/>" + userText;

        if (currentCommand < commands.length) {
            if (currentCommand === 0 && userText !== 'r') {
                terminalContent.innerHTML += "<br/>Invalid option. Try again.";
                terminalInput.value = "";
                return;
            }
            terminalContent.innerHTML += "<br/>" + commands[currentCommand];
            currentCommand++;
        } else {
            terminalContent.innerHTML += "<br/>Invalid command.";
        }

        terminalInput.value = "";
    }
});

// Initial prompt
terminalContent.innerHTML = commands[0];
currentCommand++;
