// server/static/js/tube/index.js
// 메인 진입점 (initTubeSearch)

import { handleSearch } from "./handlers/handleSearch.js";
import { handleDownloadEvents } from "./handlers/handleDownload.js";
import { handlePreviewEvents } from "./handlers/handlePreview.js";

export function initTubeSearch() {
  document.addEventListener("DOMContentLoaded", () => {
    const searchBtn = document.querySelector("#search-btn");
    const searchInput = document.querySelector("#search-query");
    const clearBtn = document.querySelector("#search-clear-btn");
    const toggleBtn = document.querySelector("#toggle-url-form-btn");

    // 검색 버튼
    searchBtn?.addEventListener("click", handleSearch);

    // 엔터 키 검색
    searchInput?.addEventListener("keydown", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        handleSearch();
      }
    });

    // 초기화
    clearBtn?.addEventListener("click", () => {
      searchInput.value = "";
      document.querySelector("#search-results").innerHTML = "";
    });

    // 토글
    toggleBtn?.addEventListener("click", () => {
      const form = document.querySelector("#tube-url-search-form");
      const orLine = document.querySelector("#or-line");
      const icon = document.querySelector("#toggle-icon");
      const text = document.querySelector("#toggle-text");
      const isHidden = form.hidden;
      form.hidden = !isHidden;
      orLine.hidden = !isHidden;
      icon.classList.toggle("fa-angle-up", isHidden);
      icon.classList.toggle("fa-angle-down", !isHidden);
      text.innerText = isHidden ? "유튜브 주소로 다운로드 숨기기" : "유튜브 주소로 다운로드 펼치기";
    });
  });
}
