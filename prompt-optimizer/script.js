document.addEventListener('DOMContentLoaded', () => {

    const userPromptInput = document.getElementById('userPrompt');
    const optimizeBtn = document.getElementById('optimizeBtn');
    const btnText = document.querySelector('.btn-text');
    const loader = document.querySelector('.loader');
    const errorMessage = document.getElementById('errorMessage');
    const outputContent = document.getElementById('outputContent');
    const copyBtn = document.getElementById('copyBtn');

    // Copy button
    copyBtn.addEventListener('click', async () => {
        const textToCopy = outputContent.innerText;
        if (!textToCopy) return;

        await navigator.clipboard.writeText(textToCopy);
        copyBtn.innerText = "Copied!";
        setTimeout(() => copyBtn.innerText = "Copy", 2000);
    });

    optimizeBtn.addEventListener('click', async () => {

        const promptText = userPromptInput.value.trim();

        if (!promptText) {
            showError("Enter a prompt");
            return;
        }

        setLoading(true);
        hideError();

        try {
            const response = await fetch("http://127.0.0.1:8000/optimize", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    prompt: promptText
                })
            });

            const data = await response.json();
            console.log("Backend:", data);

            if (data.result) {
                outputContent.textContent = data.result;
            } else {
                outputContent.textContent = "No result";
            }

        } catch (err) {
            console.error(err);
            showError("Backend not connected");
        }

        setLoading(false);
    });

    function setLoading(state) {
        if (state) {
            optimizeBtn.disabled = true;
            btnText.style.display = "none";
            loader.classList.remove('hidden');
        } else {
            optimizeBtn.disabled = false;
            btnText.style.display = "inline";
            loader.classList.add('hidden');
        }
    }

    function showError(msg) {
        errorMessage.innerText = msg;
        errorMessage.classList.remove('hidden');
    }

    function hideError() {
        errorMessage.classList.add('hidden');
    }
});