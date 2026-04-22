document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll("[data-scroll-target]").forEach((trigger) => {
        trigger.addEventListener("click", (event) => {
            const target = document.querySelector(trigger.dataset.scrollTarget);
            if (!target) {
                return;
            }

            event.preventDefault();
            target.scrollIntoView({ behavior: "smooth", block: "start" });
        });
    });
});
