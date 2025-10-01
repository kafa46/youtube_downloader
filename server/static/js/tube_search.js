// File: server/static/js/tube_search.js

"use strict";

export function initTubeSearch() {
  document.addEventListener("DOMContentLoaded", () => {
    const tubeSearchBox = document.querySelector("#tube-search-box");
    const tubeUrlSearchForm = document.querySelector("#tube-url-search-form");
    const searchBtn = document.querySelector("#search-btn");
    const searchInput = document.querySelector("#search-query");
    const orLine = document.querySelector("#or-line");
    const toggleBtn = document.querySelector("#toggle-url-form-btn");
    const toggleIcon = document.querySelector("#toggle-icon");
    const toggleText = document.querySelector("#toggle-text");
    const clearBtn = document.querySelector("#search-clear-btn");

    const showMsg = "유튜브 주소로 다운로드 펼치기";
    const hideMsg = "유튜브 주소로 다운로드 숨기기";

    // 검색 버튼 클릭
    if (searchBtn) {
      searchBtn.addEventListener("click", handleSearch);
    }

    // 엔터 키 검색
    if (searchInput) {
      searchInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") {
          e.preventDefault();
          handleSearch();
        }
      });
    }

    // 토글 버튼
    if (toggleBtn && tubeUrlSearchForm && toggleIcon && toggleText) {
      toggleBtn.addEventListener("click", () => {
        const isHidden = tubeUrlSearchForm.hidden;
        tubeUrlSearchForm.hidden = !isHidden;
        orLine.hidden = !isHidden;
        toggleIcon.classList.toggle("fa-angle-up", isHidden);
        toggleIcon.classList.toggle("fa-angle-down", !isHidden);
        toggleText.innerText = isHidden ? hideMsg : showMsg;
      });
    }

    // 초기화 버튼
    if (clearBtn) {
      clearBtn.addEventListener("click", () => {
        document.querySelector("#search-query").value = "";
        document.querySelector("#search-results").innerHTML = "";
      });
    }

  });
}

// 📌 공통 검색 실행 함수
function handleSearch() {
  const searchInput = document.querySelector("#search-query");
  const query = searchInput.value.trim();

  if (!query) {
    showAlertModal("검색어를 입력해 주세요.");
    return;
  }

  const tubeUrlSearchForm = document.querySelector("#tube-url-search-form");
  const orLine = document.querySelector("#or-line");
  const toggleIcon = document.querySelector("#toggle-icon");
  const toggleText = document.querySelector("#toggle-text");

  tubeUrlSearchForm.hidden = true;
  orLine.hidden = true;
  toggleIcon.classList.remove("fa-angle-up");
  toggleIcon.classList.add("fa-angle-down");
  toggleText.innerText = "유튜브 주소로 다운로드 펼치기";

  // socket.id 읽기
  const socketId = window.socket?.id;

  fetch(`/search/search?query=${encodeURIComponent(query)}&socket_id=${socketId}`)
    .then(response => response.json())
    .then(data => {
      if (data.code === 200) {
        renderSearchResults(data.videos);
      } else {
        showAlertModal(data.message || "검색에 실패했습니다.");
      }
    })
    .catch(error => {
      console.error("검색 오류:", error);
      showAlertModal("서버 오류가 발생했습니다.");
    });
}

// 📢 경고 모달 표시
function showAlertModal(message) {
  const modalBody = document.querySelector("#alertModalBody");
  if (modalBody) modalBody.innerHTML = message;
  const modal = new bootstrap.Modal(document.getElementById("alertModal"));
  modal.show();
}

// 📢 검색 결과 렌더링
function renderSearchResults(videos) {
  const resultsContainer = document.querySelector("#search-results");
  resultsContainer.innerHTML = "";

  if (videos.length === 0) {
    resultsContainer.innerHTML = "<p>검색 결과가 없습니다.</p>";
    return;
  }

  const row = document.createElement("div");
  row.className = "row";

  videos.forEach(video => {
    const col = document.createElement("div");
    col.className = "col-sm-6 col-md-4 col-lg-3 mb-4";
    col.innerHTML = `
      <div class="card h-100 shadow-sm">
        <div class="video-preview-wrapper position-relative">
          <img src="${video.thumbnail}"
              class="card-img-top rounded-thumbnail preview-thumbnail"
              alt="Thumbnail"
              data-video-id="${video.video_id}">
        </div>
        <div class="card-body d-flex flex-column">
          <h6 class="card-title mb-3">${video.title}</h6>
          <p class="card-text text-muted small mb-2">
            <i class="fas fa-user me-1"></i>${video.channelTitle || "알 수 없음"}
          </p>
          <p class="card-text text-muted small mb-2">
            <i class="fas fa-calendar-alt me-1"></i>${formatDate(video.publishedAt)}
          </p>

          <div class="mt-auto d-flex justify-content-between pt-2">
            <button class="btn btn-sm btn-danger preview-btn"
              data-video-id="${video.video_id}"
              data-url="${video.url}"
              data-title="${video.title}">
              영상 보기
            </button>
            <button class="btn btn-sm btn-primary download-btn"
              data-url="${video.url}"
              data-title="${video.title}">
              다운로드
            </button>
          </div>
        </div>
      </div>`;
    row.appendChild(col);
  });

  resultsContainer.appendChild(row);


  setTimeout(() => {
    // ✅ 다운로드 버튼 이벤트 리스너 등록
    document.querySelectorAll(".download-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const url = btn.dataset.url;

        const form = document.querySelector("#tube-url-search-form");
        const orLine = document.querySelector("#or-line");
        const toggleIcon = document.querySelector("#toggle-icon");
        const toggleText = document.querySelector("#toggle-text");
        const input = document.querySelector("#url");
        const submitBtn = document.querySelector("#submit-btn");

        form.hidden = false;
        orLine.hidden = false;

        // 🔽 부드러운 이동
        document.querySelector("#move-to-top")?.scrollIntoView({
          behavior: "smooth",
          block: "start"
        });

        toggleIcon.classList.remove("fa-angle-down");
        toggleIcon.classList.add("fa-angle-up");
        toggleText.innerText = "유튜브 주소로 다운로드 숨기기";

        input.value = url;
        submitBtn.click();
      });
    });

    // ✅ 카드 내부의 썸네일 클릭 시 해당 썸네일 자리에 iframe 교체
    document.querySelectorAll(".preview-thumbnail").forEach(img => {
      img.addEventListener("click", () => {
        const videoId = img.dataset.videoId;

        // 모든 썸네일 보이도록 (숨긴 거 복구)
        document.querySelectorAll(".preview-thumbnail").forEach(thumbnail => {
          // 바로 block 처리하지 않고 opacity를 부드럽게 전환
          thumbnail.style.display = "block";
        });


        // 기존 iframe 모두 제거
        document.querySelectorAll(".video-preview-wrapper iframe").forEach(iframe => {
          iframe.remove();
        });

        const wrapper = img.parentElement;

        // 자신이 이미 iframe을 가지고 있었으면 클릭으로 복원하는 의미이므로 종료
        if (wrapper.querySelector("iframe")) {
          return;
        }

        // 썸네일 숨기기
        img.style.display = "none";

        // ✅ 외부 미리보기 제거
        const externalPreview = document.querySelector("#youtube-preview-container");
        if (externalPreview) {
          externalPreview.innerHTML = "";
        }

        // 새 iframe 생성
        const iframe = document.createElement("iframe");
        iframe.src = `https://www.youtube.com/embed/${videoId}?autoplay=1`;
        iframe.allow = "accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture";
        iframe.allowFullscreen = true;
        iframe.className = "rounded-2";
        iframe.style.width = "100%";
        iframe.style.aspectRatio = "16/9";
        iframe.style.border = "none";

        wrapper.appendChild(iframe);
      });
    });



    // ✅ 영상 보기 버튼 이벤트 (iframe 미리보기 삽입)
    document.querySelectorAll(".preview-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const videoId = btn.dataset.videoId;
        const url = btn.dataset.url;
        const previewContainer = document.querySelector("#youtube-preview-container");

        // ✅ 1. 카드 내부에서 재생 중인 영상이 있다면 모두 제거하고 썸네일 복원
        document.querySelectorAll(".video-preview-wrapper iframe").forEach(iframe => {
          const wrapper = iframe.parentElement;
          const thumbnail = wrapper.querySelector(".preview-thumbnail");
          iframe.remove();
          if (thumbnail) thumbnail.style.display = "block";
        });

        // ✅ 2. preview 영역이 이미 해당 videoId면 닫기 (토글)
        if (previewContainer.innerHTML.includes(videoId)) {
          previewContainer.innerHTML = "";
          return;
        }

        // ✅ 3. 새 iframe 삽입
        previewContainer.innerHTML = `
          <div id="iframe-wrapper" class="row preview-iframe-row justify-content-center mb-3">
            <div class="col-11 col-md-10 col-lg-8">
              <div class="ratio ratio-16x9 rounded-2 overflow-hidden">
                <iframe
                  src="https://www.youtube.com/embed/${videoId}?autoplay=1"
                  title="YouTube preview"
                  allowfullscreen
                  allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture">
                </iframe>
              </div>
              <div class="text-end mt-2">
                <button class="btn btn-sm btn-outline-primary" id="preview-close-btn">닫기</button>
                <button class="btn btn-sm btn-outline-primary" id="preview-download-btn"
                  data-url="${btn.dataset.url}"
                  data-title="${btn.title}">직접 다운로드</button>
              </div>
            </div>
          </div>
        `;


        // 📌 iframe wrapper로 부드러운 스크롤
        const wrapper = document.getElementById("iframe-wrapper");
        wrapper?.scrollIntoView({
          behavior: "smooth",
          block: "center"
        });


        // 미리보기 닫기
        previewContainer.querySelector("#preview-close-btn").addEventListener("click", () => {
          previewContainer.innerHTML = "";
        });

        // 다운로드
        previewContainer.querySelector("#preview-download-btn").addEventListener("click", () => {
          // 📌 주소 입력창 활성화 및 값 설정
          document.querySelector("#tube-url-search-form").hidden = false;
          document.querySelector("#or-line").hidden = false;
          document.querySelector("#toggle-icon").classList.remove("fa-angle-down");
          document.querySelector("#toggle-icon").classList.add("fa-angle-up");
          document.querySelector("#toggle-text").innerText = "유튜브 주소로 다운로드 숨기기";
          const input = document.querySelector("#url");
          const submitBtn = document.querySelector("#submit-btn");
          input.value = url;
          submitBtn.click();
        });
      });
    },

      0);
  });
}

// 📢 날짜 포맷 함수
function formatDate(isoString) {
  if (!isoString) return "날짜 없음";
  const date = new Date(isoString);
  return date.toLocaleDateString("ko-KR", {
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
  });
}
