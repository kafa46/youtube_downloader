// server/static/js/tube/handlers/handleDownload.js
// 다운로드 처리 로직

"use strict";

export function handleDownloadEvents() {
    document.querySelectorAll(".download-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const url = btn.dataset.url;
            document.querySelector("#tube-url-search-form").hidden = false;
            document.querySelector("#or-line").hidden = false;
            document.querySelector("#toggle-icon").classList.replace("fa-angle-down", "fa-angle-up");
            document.querySelector("#toggle-text").innerText = "유튜브 주소로 다운로드 숨기기";
            document.querySelector("#url").value = url;
            document.querySelector("#submit-btn").click();
            document.querySelector("#move-to-top")?.scrollIntoView({ behavior: "smooth" });
        });
    });
}
