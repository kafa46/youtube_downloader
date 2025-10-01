// static/js/progressbar.js

"use strict";

// WebSocket 연결 설정 방법
// const socket = io("wss://tube.acin.kr", {
//     transports: ["websocket"],
// });

// 개발 시 로컬 테스트용으로 연결 설정 방법
// const socket = io("ws://localhost:5050", {
//     transports: ["websocket"]
//   });


// 자동 환경 감지 (로컬/운영 모두 대응)
// const protocol = location.protocol === "https:" ? "wss" : "ws";
// const host = location.hostname;
// const port = location.port ? `:${location.port}` : "";
// const socket = io(`${protocol}://${host}${port}`, {
//   transports: ["websocket"]
// });

// File: static/js/lib/socketProvider.js에서 전역으로 등록한 socket 사용
// 위에서 작성한 코드는 주석 처리함

import { showAlertModal } from "/static/js/utils/showAlertModal.js";

// 소켓 ID 저장
socket.on("connect", () => {
    const socketIdDiv = document.createElement("div");
    socketIdDiv.id = "socket-id";
    socketIdDiv.hidden = true;
    socketIdDiv.textContent = `${socket.id}`;
    document.body.appendChild(socketIdDiv);
});

// DOM 요소 참조
const progressBar = document.getElementById("serverProgressbar");
const progressWrapper = document.getElementById("progress-wrapper");
const loadingDiv = document.querySelector(".loading");
const downloadBtn = document.getElementById("request-file-btn");
const progressMsg = document.querySelector("#progress-msg")

let downloadStarted = false;

// 진행률 이벤트 수신
socket.on("progress", (data) => {
    if (!downloadStarted) {
        loadingDiv.hidden = true;
        progressWrapper.hidden = false;
        progressMsg.hidden = false;
        downloadStarted = true;
    }

    const percent = parseFloat(data.progress);
    progressBar.style.width = `${percent}%`;
    progressBar.setAttribute("aria-valuenow", percent);
    progressBar.innerText = `${percent}%`;
});

// 유튜브 직접 검색 후 다운로드 요청이 있을 경우 상태 확인
// 유튜브 API quota 초과 -> yt-dlp로 다운로드하는 경우 확인
window.socket.on("yt_status", (data) => {
    if (data.status === "info") {
        showAlertModal(data.message);  // 또는 custom modal/alert
    } else if (data.status === "done") {
        console.log("📦 다운로드 준비 완료!");
    }
});

// 다운로드 완료 이벤트 수신
socket.on("complete", (data) => {
    if (data.status === "completed") {
        const requestUrl = `/download/request_file?file=${data.file_name}`;
        downloadBtn.href = requestUrl;
        // downloadBtn.hidden = false;
        downloadBtn.click();

        progressBar.innerText = "다운로드 완료!";
        progressBar.classList.remove("bg-danger");
        progressBar.classList.add("bg-info");
        progressMsg.hidden = true;

        setTimeout(() => {
            progressWrapper.hidden = true;
            progressBar.style.width = "0%";
            progressBar.innerText = "0%";
            downloadStarted = false;
        }, 3000);
    } else {
        progressBar.innerText = "오류 발생";
        progressBar.classList.remove("bg-info");
        progressBar.classList.add("bg-danger");
        progressMsg.hidden = true;
        alert("다운로드 중 오류가 발생했습니다. 다시 시도해 주세요.");
        setTimeout(() => {
            progressWrapper.hidden = true;
            progressBar.classList.remove("bg-danger");
            progressBar.classList.remove("bg-info");
            progressBar.style.width = "0%";
            progressBar.innerText = "0%";
            downloadStarted = false;
        }, 3000);
    }
});
