// server/static/js/tube/utils/formatDate.js
// 날짜 포맷 함수

"use strict";

export function formatDate(isoString) {
    if (!isoString) return "날짜 없음";
    return new Date(isoString).toLocaleDateString("ko-KR", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit"
    });
}
