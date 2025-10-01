// server/static/js/tube/render/renderSearchResults.js
// 검색 결과 렌더링

"use strict";

import { handleDownloadEvents } from "../handlers/handleDownload.js";
import { handlePreviewEvents } from "../handlers/handlePreview.js";
import { formatDate } from "../utils/formatDate.js";

export function renderSearchResults(videos) {
    const resultsContainer = document.querySelector("#search-results");
    resultsContainer.innerHTML = "";
    if (!videos.length) return resultsContainer.innerHTML = "<p>검색 결과가 없습니다.</p>";

    const row = document.createElement("div");
    row.className = "row";

    videos.forEach(video => {
        const col = document.createElement("div");
        col.className = "col-sm-6 col-md-4 col-lg-3 mb-4";
        col.innerHTML = `
      <div class="card h-100 shadow-sm">
        <div class="video-preview-wrapper position-relative">
          <img src="${video.thumbnail}" class="card-img-top rounded-thumbnail preview-thumbnail"
               alt="Thumbnail" data-video-id="${video.video_id}">
        </div>
        <div class="card-body d-flex flex-column">
          <h6 class="card-title mb-3">${video.title}</h6>
          <p class="card-text text-muted small mb-2">
            <i class="fas fa-user me-1"></i>${video.channelTitle || "알 수 없음"}</p>
          <p class="card-text text-muted small mb-2">
            <i class="fas fa-calendar-alt me-1"></i>${formatDate(video.publishedAt)}</p>
          <div class="mt-auto d-flex justify-content-between pt-2">
            <button class="btn btn-sm btn-danger preview-btn" data-video-id="${video.video_id}" data-url="${video.url}">
              영상 보기
            </button>
            <button class="btn btn-sm btn-primary download-btn" data-url="${video.url}">다운로드</button>
          </div>
        </div>
      </div>`;
        row.appendChild(col);
    });

    resultsContainer.appendChild(row);
    handleDownloadEvents();
    handlePreviewEvents();
}

