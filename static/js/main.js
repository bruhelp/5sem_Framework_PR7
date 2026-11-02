"use strict";

document.addEventListener("DOMContentLoaded", () => {
    const currentYear = new Date().getFullYear();
    document.documentElement.dataset.currentYear = String(currentYear);
});
