/* server/static/js/check_downloadable.js */

"use strict";

// 유튜브 주소 확인 및 다운로드 가능 목록 조회
document.addEventListener("DOMContentLoaded", () => {
    const submitBtn = document.getElementById("submit-btn");
    const clearBtn = document.getElementById("clear-btn");
    const csrfToken = document.getElementById("csrf_token")?.value;

    if (submitBtn) {
        submitBtn.addEventListener("click", async () => {
            const urlInput = document.getElementById("url").value.trim();
            if (!urlInput) {
                alert("유튜브 주소를 입력해 주세요.");
                return;
            }

            clearTable();
            toggleElement("table-area", false);
            hideYouTubeInfo();
            showLoading("서버 🔥 엔진에서<br>가능한 목록을<br>조회 중입니다👊<br>잠시만 기다려<br>주세요😁^^<br>");

            try {
                const response = await fetch(submitBtn.dataset.url, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        ...(csrfToken && { "X-CSRFToken": csrfToken })
                    },
                    body: JSON.stringify({ url: urlInput })
                });

                // ✅ JSON 응답인지 확인
                const contentType = response.headers.get("content-type");
                if (!contentType || !contentType.includes("application/json")) {
                    const errorText = await response.text(); // HTML 본문 보기
                    // console.error("❌ 서버 응답이 JSON이 아님:", errorText);
                    alert(`다운로드 가능성을 검사하던 중\n서버 오류가 발생했습니다.\n이 동영상은 다운로드 할 수 없어요 ㅠ`);
                    return;
                }

                const data = await response.json();

                if (data.code === "200") {
                    renderVideoList(data.files, urlInput);
                    showYouTubeInfo(data.thumbnail_url, data.title, data.duration);
                    clearBtn.hidden = false;
                } else {
                    alert("에러가 발생했습니다. 유튜브 주소를 확인해 주세요.");
                }
            } catch (err) {
                console.error("요청 중 오류 발생:", err);
                alert(`다운로드 가능성을 검사하던 중\n서버 오류가 발생했습니다.\n이 동영상은 다운로드 할 수 없어요 ㅠ\n오류내용: ${err}`);
            } finally {
                hideLoading();
            }
        });
    }

    if (clearBtn) {
        clearBtn.addEventListener("click", () => {
            document.getElementById("url").value = "";
            clearTable();
            hideYouTubeInfo();
            hideLoading();
            toggleElement("table-area", false);
            clearBtn.hidden = true;
        });
    }
});


// 개별 선택 아이템을 다운로드 하는 함수
async function download_tube(index, video_idx, file_size, type, socket_id) {
    const send_url = document.getElementById('downloading').dataset.downloadUrl;
    const youtube_url = document.getElementById('url').value;
    const csrf_token = document.getElementById('csrf_token')?.value;

    // m4a/mp3/mp4 사용자 안내
    if (type === 3 && !confirm("mp3 파일은 서버에서 추가 변환 작업을 해야 합니다.\n변환 시간이 오래 걸릴 수 있습니다.\n진행할까요?")) return;
    if (type === 1 && !confirm(`${file_size} MB 동영상을 다운받습니다.\n서버 처리 시간이 길어질 수 있습니다.\n진행할까요 ^^?`)) return;

    // 로딩 메시지 및 스피너 표시
    document.getElementById('loading-message').innerHTML =
        '<div class="scan-icon">👀</div><br>영상 검사 중...<br>메시지가 사라지면<br>진행상태 표시됨.<br>기다려 주세요^^';

    document.getElementById('overlay')?.classList.remove('hidden');
    document.querySelector('.loading')?.removeAttribute('hidden');

    const payload = {
        index,
        video_idx,
        url: youtube_url,
        type,
        file_size,
        socket_id
    };

    try {
        const response = await fetch(send_url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                ...(csrf_token && { 'X-CSRFToken': csrf_token })
            },
            body: JSON.stringify(payload)
        });

        const result = await response.json();

        // console.log('다운로드 요청 결과:', result);

        if (result.code !== '200') {
            alert('파일 생성에 실패했습니다.');
        }
    } catch (error) {
        console.error('다운로드 중 오류 발생:', error);
        alert('서버 오류가 발생했습니다.');
    } finally {
        document.getElementById('overlay')?.classList.add('hidden');
        document.querySelector('.loading')?.setAttribute('hidden', true);
    }
}

// 유틸 함수
function toggleElement(id, show = true) {
    document.getElementById(id).hidden = !show;
}

function showLoading(message = "") {
    document.querySelector(".loading").hidden = false;
    const loadingMsg = document.getElementById("loading-message");
    if (loadingMsg) {
        loadingMsg.innerHTML = message;
        loadingMsg.classList.remove("text-danger");
        loadingMsg.classList.add("text-primary");
    }
}

function hideLoading() {
    document.querySelector(".loading").hidden = true;
    const loadingMsg = document.getElementById("loading-message");
    if (loadingMsg) {
        loadingMsg.innerText = "";
        loadingMsg.classList.remove("text-danger", "text-primary");
    }
}

function showYouTubeInfo(thumbnailUrl, title, duration) {
    toggleElement("tube-info-area", true);
    document.getElementById("tube-thumbnail").src = thumbnailUrl;
    document.getElementById("tube-title").innerText = `${title} (재생시간: ${duration})`;
    document.getElementById("tumnail-link").href = document.getElementById("url").value;
}

function hideYouTubeInfo() {
    toggleElement("tube-info-area", false);
    document.getElementById("tumnail-link").href = "";
}


function clearTable() {
    const list = document.querySelectorAll(".file-list");
    list.forEach(el => el.remove());
}


function deleteTableElement() {
    // 기존에 있던 테이블 목록 삭제
    let table_list = $('.file-list')
    for (let i = 0; i < table_list.length; i++) {
        table_list[i].remove()
    }
}

// 비디오 목록 테이블 구성
function renderVideoList(files, youtubeUrl) {
    const table = document.getElementById("video-list");
    const socketId = document.getElementById("socket-id")?.textContent || "";

    let mp4Count = 0;

    files.forEach((file, index) => {
        if (file.type === 'mp4') {
            if (mp4Count >= 5) return; // mp4는 최대 5개까지만 추가
            mp4Count++;
        }

        const row = document.createElement("tr");
        row.className = "file-list";

        const sizeMB = Math.round(file.size_mb * 10) / 10;
        const columns = [
            `<th>${file.type === 'mp4' ? '비디오' : '오디오'}</th>`,
            `<td>${file.type}</td>`,
            `<td>${sizeMB.toLocaleString()} MB</td>`,
            `<td>${file.resolution}</td>`,
            `<td>
                <a href="#"
                    class="btn btn-outline-primary download-item"
                    onclick="download_tube(${index}, '${file.id}', ${sizeMB}, ${typeMap(file.type)}, '${socketId}')">
                    받기
                </a>
            </td>`
        ];

        row.innerHTML = columns.join("\n");
        table.appendChild(row);
    });

    // MP3 항목 추가
    const mp3Row = document.createElement("tr");
    mp3Row.className = "file-list";
    mp3Row.innerHTML = `
      <th>MP3 파일</th>
      <td>mp3</td>
      <td>서버 변환 후 다운</td>
      <td>해당없음</td>
      <td>
        <a href="#" class="btn btn-outline-primary"
           onclick="download_tube(0, 0, 0, 3, '${socketId}')">받기</a>
      </td>
    `;
    table.appendChild(mp3Row);

    toggleElement("table-area", true);
}


function typeMap(type) {
    return { mp4: 1, m4a: 2, mp3: 3, optimal: 4 }[type] || 0;
}