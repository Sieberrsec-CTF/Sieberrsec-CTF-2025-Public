document.addEventListener("DOMContentLoaded", function () {
    const uploadBtn = document.querySelector("#uploadForm button");
    const renderBtn = document.querySelector("#renderForm button");

    uploadBtn.addEventListener("click", function () {
        const filename = document.getElementById("filename").value.trim();

        if (!filename) {
            alert("Filename is required.");
            return;
        }

        const form = document.getElementById("uploadForm");
        form.action = `/upload/${encodeURIComponent(filename)}`;
        form.submit();
    });

    renderBtn.addEventListener("click", function () {
        const filename = document.getElementById("renderFilename").value.trim();
        if (!filename) {
            alert("Filename is required.");
            return;
        }

        window.location.href = `/render?filename=${encodeURIComponent(filename)}`;
    });
});
