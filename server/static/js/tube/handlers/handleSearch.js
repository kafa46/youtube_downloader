// server/static/js/tube/handlers/handleSearch.js
// 검색 처리 로직

"use strict";

import { renderSearchResults } from "../render/renderSearchResults.js";
import { showAlertModal } from "../utils/showAlertModal.js";

export function handleSearch() {
    const input = document.querySelector("#search-query");
    const query = input.value.trim();
    if (!query) return showAlertModal("검색어를 입력해 주세요.");

    fetch(`/search/search?query=${encodeURIComponent(query)}`)
        .then(res => res.json())
        .then(data => {
            if (data.code === 200) renderSearchResults(data.videos);
            else showAlertModal(data.message || "검색 실패");
        })
        .catch(() => showAlertModal("서버 오류 발생"));
}
