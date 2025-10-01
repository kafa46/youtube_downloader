// server/static/js/tube/utils/showAlertModal.js
// 모달 알림 처리

"use strict";

export function showAlertModal(message) {
    const modalBody = document.querySelector("#alertModalBody");
    modalBody.innerHTML = message;
    new bootstrap.Modal(document.getElementById("alertModal")).show();
}
