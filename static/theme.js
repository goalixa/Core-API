(() => {
  const storageKey = "theme";
  const root = document.documentElement;
  const openDropdowns = () => {
    document.querySelectorAll(".timer-dropdown").forEach((dropdown) => {
      dropdown.classList.add("is-open");
    });
  };
  const toggle = () => {
    const current = root.getAttribute("data-theme") || "light";
    const next = current === "dark" ? "light" : "dark";
    root.setAttribute("data-theme", next);
    localStorage.setItem(storageKey, next);
  };

  const saved = localStorage.getItem(storageKey);
  if (saved) {
    root.setAttribute("data-theme", saved);
  }

  document.addEventListener("click", (event) => {
    const target = event.target;
    if (!(target instanceof HTMLElement)) {
      return;
    }
    const button = target.closest("[data-theme-toggle]");
    if (button) {
      toggle();
    }
    if (target.closest(".timer-select")) {
      openDropdowns();
    }
    if (target.closest(".timer-list button")) {
      const input = target.closest(".timer-select")?.querySelector("#task-picker");
      if (input) {
        input.value = target.textContent || "";
      }
      document.querySelectorAll(".timer-dropdown").forEach((dropdown) => {
        dropdown.classList.remove("is-open");
      });
    }
    if (target.closest(".timer-dropdown") === null && !target.closest(".timer-select")) {
      document.querySelectorAll(".timer-dropdown").forEach((dropdown) => {
        dropdown.classList.remove("is-open");
      });
    }
  });
})();
