document.addEventListener("DOMContentLoaded", function () {

    // ── Upload form ──────────────────────────────────────────────
    const form        = document.getElementById("upload-form");
    const loading     = document.getElementById("loading");
    const analyzeBtn  = document.getElementById("analyze-btn");
    const fileInput   = document.getElementById("pdf");
    const fileLabelText = document.getElementById("file-label-text");
    const dropZone    = document.getElementById("file-drop-zone");
    const levelSelect = document.getElementById("level");
    const levelHint   = document.getElementById("level-hint");
    const loadingSubText = document.getElementById("loading-sub-text");

    const levelHints = {
        "Beginner":     "Content will use simple language, real-world examples, and avoid jargon.",
        "Intermediate": "Content will use clear terminology with explanations and helpful examples.",
        "Advanced":     "Content will use professional terminology and expand on deeper concepts.",
        "Expert":       "Content will use precise academic language with graduate-level depth."
    };

    // Update level hint on change
    if (levelSelect && levelHint) {
        levelSelect.addEventListener("change", function () {
            levelHint.textContent = levelHints[this.value] || "";
        });
    }

    // File input — show filename
    if (fileInput && fileLabelText && dropZone) {
        fileInput.addEventListener("change", function () {
            if (this.files && this.files[0]) {
                fileLabelText.textContent = "📄 " + this.files[0].name;
                dropZone.classList.add("has-file");
            } else {
                fileLabelText.textContent = "Click to browse or drag & drop a PDF";
                dropZone.classList.remove("has-file");
            }
        });

        // Drag-over visual feedback
        dropZone.addEventListener("dragover", function (e) {
            e.preventDefault();
            dropZone.classList.add("drag-over");
        });
        dropZone.addEventListener("dragleave", function () {
            dropZone.classList.remove("drag-over");
        });
        dropZone.addEventListener("drop", function () {
            dropZone.classList.remove("drag-over");
        });
    }

    // Form submit — show loading
    if (form) {
        form.addEventListener("submit", function () {
            if (loading) loading.style.display = "block";
            if (analyzeBtn) {
                analyzeBtn.disabled = true;
                analyzeBtn.innerHTML = '<span class="btn-icon">⏳</span> Processing…';
            }
            if (loadingSubText) {
                const level = levelSelect ? levelSelect.value : "your";
                loadingSubText.textContent =
                    "Simplifying for " + level + " level — this may take a moment for longer documents.";
            }
        });
    }

    // Scroll result into view after page reload
    const notesOutput = document.getElementById("notes-output");
    if (notesOutput) {
        setTimeout(function () {
            notesOutput.closest(".results-section").scrollIntoView({ behavior: "smooth", block: "start" });
        }, 200);
    }

    // ── Quiz modal ───────────────────────────────────────────────
    const quizBtn       = document.getElementById("quiz-btn");
    const quizModal     = document.getElementById("quiz-modal");
    const modalCloseBtn = document.getElementById("modal-close-btn");
    const quizLoading   = document.getElementById("quiz-loading");
    const quizContent   = document.getElementById("quiz-content");
    const quizError     = document.getElementById("quiz-error");
    const modalLevelRow = document.getElementById("modal-level-row");
    const modalLevelBadge = document.getElementById("modal-level-badge");

    function openModal() {
        if (quizModal) {
            quizModal.style.display = "flex";
            document.body.style.overflow = "hidden";
        }
    }

    function closeModal() {
        if (quizModal) {
            quizModal.style.display = "none";
            document.body.style.overflow = "";
        }
    }

    // Close on backdrop click
    if (quizModal) {
        quizModal.addEventListener("click", function (e) {
            if (e.target === quizModal) closeModal();
        });
    }

    // Close on Escape
    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape") closeModal();
    });

    if (modalCloseBtn) {
        modalCloseBtn.addEventListener("click", closeModal);
    }

    if (quizBtn) {
        quizBtn.addEventListener("click", function () {
            // Reset modal state
            if (quizContent) { quizContent.innerHTML = ""; quizContent.style.display = "none"; }
            if (quizError)   { quizError.textContent = ""; quizError.style.display = "none"; }
            if (quizLoading)  quizLoading.style.display = "block";
            if (modalLevelRow) modalLevelRow.style.display = "none";

            openModal();

            // Fetch quiz from server
            fetch("/quiz", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({})   // server reads level from session
            })
            .then(function (res) { return res.json(); })
            .then(function (data) {
                if (quizLoading) quizLoading.style.display = "none";

                if (data.error) {
                    if (quizError) {
                        quizError.textContent = data.error;
                        quizError.style.display = "block";
                    }
                    return;
                }

                if (quizContent && data.html) {
                    quizContent.innerHTML = data.html;
                    quizContent.style.display = "block";
                }

                if (modalLevelRow && modalLevelBadge && data.level) {
                    modalLevelBadge.textContent = data.level;
                    modalLevelRow.style.display = "flex";
                }
            })
            .catch(function (err) {
                if (quizLoading) quizLoading.style.display = "none";
                if (quizError) {
                    quizError.textContent = "Network error: " + err.message;
                    quizError.style.display = "block";
                }
            });
        });
    }

});
