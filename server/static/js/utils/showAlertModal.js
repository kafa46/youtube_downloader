// static/js/utils/showAlertModal.js

export function showAlertModal(message) {
    const modalBody = document.querySelector("#alertModalBody");
    const modalEl = document.querySelector("#alertModal");

    if (modalBody && modalEl) {
      modalBody.innerText = message;

      const modal = new bootstrap.Modal(modalEl);
      modal.show();
    }
  }
