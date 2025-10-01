// File: static/js/lib/socketProvider.js
"use strict";

// 동적으로 프로토콜/포트 구성 -> 자동 환경 감지 (로컬/운영 모두 대응)
const protocol = location.protocol === "https:" ? "wss" : "ws";
const host = location.hostname;
const port = location.port ? `:${location.port}` : "";
const socket = io(`${protocol}://${host}${port}`, {
  transports: ["websocket"]
});


// 전역 등록 (다른 모듈에서 접근 가능)
window.socket = socket;
