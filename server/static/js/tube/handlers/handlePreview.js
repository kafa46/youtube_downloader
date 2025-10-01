// server/static/js/handlers/handlePreview.js
// 미리보기 iframe 처리

"use strict";

export function handlePreviewEvents() {
    document.querySelectorAll(".preview-btn").forEach(btn => {
        btn.addEventListener("click", () => {
            const videoId = btn.dataset.videoId;
            const url = btn.dataset.url;
            const container = document.querySelector("#youtube-preview-container");

            document.querySelectorAll(".video-preview-wrapper iframe").forEach(iframe => {
                const thumb = iframe.parentElement.querySelector(".preview-thumbnail");
                iframe.remove();
                if (thumb) thumb.style.display = "block";
            });

            if (container.innerHTML.includes(videoId)) {
                container.innerHTML = "";
                return;
            }

            container.innerHTML = `
          <div id="iframe-wrapper" class="row preview-iframe-row justify-content-center mb-3">
            <div class="col-11 col-md-10 col-lg-8">
              <div class="ratio ratio-16x9 rounded-2 overflow-hidden">
                <iframe src="https://www.youtube.com/embed/${videoId}?autoplay=1" allowfullscreen
                        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture">
                </iframe>
              </div>
              <div class="text-end mt-2">
                <button class="btn btn-sm btn-outline-primary" id="preview-close-btn">닫기</button>
                <button class="btn btn-sm btn-outline-primary" id="preview-download-btn"
                        data-url="${url}">직접 다운로드</button>
              </div>
            </div>
          </div>`;

            container.querySelector("#preview-close-btn").addEventListener("click", () => {
                container.innerHTML = "";
            });

            container.querySelector("#preview-download-btn").addEventListener("click", () => {
                document.querySelector("#tube-url-search-form").hidden = false;
                document.querySelector("#or-line").hidden = false;
                document.querySelector("#toggle-icon").classList.replace("fa-angle-down", "fa-angle-up");
                document.querySelector("#toggle-text").innerText = "유튜브 주소로 다운로드 숨기기";
                document.querySelector("#url").value = url;
                document.querySelector("#submit-btn").click();
                document.getElementById("iframe-wrapper")?.scrollIntoView({ behavior: "smooth", block: "center" });
            });
        });
    });
}
