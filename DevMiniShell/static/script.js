document.addEventListener('DOMContentLoaded', () => {
    const output = document.getElementById('output');
    const commandInput = document.getElementById('command-input');

    commandInput.addEventListener('keydown', async (e) => {
        if (e.key === 'Enter') {
            const command = commandInput.value.trim();
            commandInput.value = '';

            if (command) {
                appendOutput(`> ${command}`);
                try {
                    const response = await fetch('/api/command', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ command }),
                    });
                    const data = await response.json();
                    appendOutput(data.output);
                } catch (error) {
                    appendOutput(`Error: ${error.message}`);
                }
            }
        }
    });

    function appendOutput(message) {
        output.innerHTML += `${message}\n`;
        output.scrollTop = output.scrollHeight;
    }
});
